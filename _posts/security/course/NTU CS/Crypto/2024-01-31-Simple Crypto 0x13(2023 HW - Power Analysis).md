---
title: Simple Crypto 0x13(2023 HW - Power Analysis)
tags: [eductf, CTF, Crypto]

category: "Security > Course > NTU CS > Crypto"
---

# Simple Crypto 0x13(2023 HW - Power Analysis)
## Background
[ [edu-ctf 2023] week04 - crypto3 [1:30:36]](https://www.youtube.com/live/Q-gaGLJpJHc?si=DZgJm62AnoPHWiZF&t=5433)
## Source code
json file recorded by TA
## Recon
這一題全部都是刻出來的，也包含算correlation coefficient，後面才知道numpy有這東西，但反正根據老師上課的作法一步一步跟著做是絕對沒有問題的，包含以下步驟:
1. Preprocessing
    也就是把pt, ct, pm都按照簡報上的方式排列(各個trace的第一個byte都蒐集在一起，第二個byte都蒐集再一起...)
2. 計算和sbox key XOR的結果
3. 查表sbox
4. 計算hamming weight model
5. 計算和trace的correlation coefficient
6. 看哪一個結果的數值最大，並把index結果記錄下來算它的ascii
7. repeat以上操作後共可得16 bytes的flag
* 加速的方法:
    可以把整個trace的圖片plot出來看看，會發現題目給的json file是把整段加密的過程記錄下來，所以我們可以只取前一兩百個point就可以完成key的還原
    
## Exploit
```python=
import json
from tqdm import trange
import numpy as np
import copy
from string import ascii_letters, digits
from numpy import corrcoef

jsonFile = open('./Crypto/HW3/traces.json', 'r')
j = json.load(jsonFile)

s_box = [
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
]

def data_preprocess(json_data):
    pt_col = []
    ct_col = []
    trace_col = []
    for bytes in range(16):
        tmp_pt_col = []
        tmp_ct_col = []
        for trace_idx in range(len(json_data)):
            tmp_pt_col.append(json_data[trace_idx]['pt'][bytes])
            tmp_ct_col.append(json_data[trace_idx]['ct'][bytes])
        pt_col.append(tmp_pt_col)
        ct_col.append(tmp_ct_col)
    for point in range(len(json_data[0]['pm'])):
        tmp_trace_col = []
        for trace_idx in range(len(json_data)):
            tmp_trace_col.append(json_data[trace_idx]['pm'][point])
        trace_col.append(tmp_trace_col)
    
    return pt_col, ct_col, trace_col

def sbox_preprocess(pt_col):
    sbox_result_tmp = []
    for sbox_key in range(256): # 總共有256個sbox key
        tmp = []
        for trace in range(len(pt_col)): # 有50個trace
            tmp.append(pt_col[trace] ^ sbox_key)
        sbox_result_tmp.append(tmp)
    return sbox_result_tmp

def choose_sbox(sbox_result_tmp):
    sbox_result = copy.deepcopy(sbox_result_tmp)
    for sbox_key in range(256):
        for trace in range(50):
            hex_value = '{0:0>2x}'.format(sbox_result_tmp[sbox_key][trace])
            x, y = hex_value[0], hex_value[1]
            sbox_result[sbox_key][trace] = s_box[int(x, 16)][int(y, 16)]
    
    return sbox_result

def cal_hamming_weight(sbox_result_col):
    hw_model = copy.deepcopy(sbox_result_col)
    for i in range(len(sbox_result_col)):   # 256
        for j in range(len(sbox_result_col[i])):    # 50
            hw_model[i][j] = bin(sbox_result_col[i][j]).count('1')
    
    return hw_model

def cal_correlation(hw_model_col_result, trace_col):
    correlation_result = []
    for i in (ascii_letters + digits).encode():#trange(len(hw_model_col_result)): <- 加速的部分
        for j in range(biggest_length):
            correlation_result.append(corrcoef(hw_model_col_result[i], trace_col[j])[0, -1])
    return correlation_result
            
def run_pearson_correlation(x, y):
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    covariance = np.sum((x - mean_x) * (y - mean_y))
    
    std_dev_x = np.sqrt(np.sum((x - mean_x)**2))
    std_dev_y = np.sqrt(np.sum((y - mean_y)**2))
    
    correlation = covariance / (std_dev_x * std_dev_y)
    
    return correlation

def display_pt(offset:int, data_offset = (0, len(j[0]["pm"]))):
    plt.plot(range(data_offset[0], data_offset[1]), j[offset]["pm"][data_offset[0]:data_offset[1]])
    plt.savefig(fname="pt_" + str(offset) + ".jpg")
    plt.clf()

# display_pt(0, (0, 95))
# display_pt(0)
pt_col, ct_col, trace_col = data_preprocess(j)
flag = ''
biggest_length = 95# len(trace_col)
for idx in trange(16):
    sbox_preprocess_result = sbox_preprocess(pt_col[idx])
    choose_sbox_result = choose_sbox(sbox_preprocess_result)
    hw_model_col_result = cal_hamming_weight(choose_sbox_result)
    correlation_result = cal_correlation(hw_model_col_result, trace_col)
    key_idx = correlation_result.index(max(correlation_result))
    flag += (ascii_letters + digits)[key_idx // biggest_length]
    # from Crypto.Util.number import long_to_bytes
    # flag += long_to_bytes(key_idx // biggest_length).decode("cp437")

print('The key of AES is: FLAG{' + flag + '}')
```
有嘗試過只選擇常見可使用的字元也就是`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`，以及trace只選擇前95個data，也可以正常解析出AES key並且算的更快(大約快77倍左右)

Flag: `FLAG{W0ckAwocKaWoCka1}`
## Reference
[NTU Computer Security HW1 - AES](https://hackmd.io/@asef18766/NTU-CS-2022-hw1#AES)