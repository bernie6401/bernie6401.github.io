---
title: PicoCTF - PowerAnalysis Part 1 / Part 2
tags: [PicoCTF, CTF, Crypto]

category: "Security Practice｜PicoCTF｜Crypto｜SideChannel"
date: 2024-01-31
---

# PicoCTF - PowerAnalysis Part 1 / Part 2
<!-- more -->

## Background
[Simple Welcome 0x13(2023 HW - Power Analysis):two:](https://hackmd.io/@SBK6401/HJNScTc-T)

## Recon
這一題幾乎就和上課教的差不多，只是因為有雜訊，所以要慎選trace point，我是直接看第一個trace的分布，決定採用300~400的point，而不管是利用自己刻的correlation coefficient還是用scipy的pearsonr都一樣可以順利解出key但是如果像homework一樣用numpy的corrcoef會有兩個bytes和正解不一樣，超哭，找超久(10/18更新，如果用自己刻的也是要碰用氣，所以如果可以的話，多送幾個trace，或者多用幾個算correlation coefficient的library)
![](https://hackmd.io/_uploads/SJ4YLRnZT.jpg)

* Part 2的部分幾乎一模一樣，就只是他先幫你紀錄好所有的trace，再讓我們做後續的分析

## Exploit
* 首先先把資料從server拉下來，在存成json
    ```python
    from pwn import *
    from string import ascii_letters, digits
    import json
    from tqdm import trange


    def gen_plaintext(length):
        return ''.join(random.choice(ascii_letters + digits) for _ in range(length))


    pt = [gen_plaintext(16) for _ in range(50)]
    print(pt)
    json_file = [None] * len(pt)

    for i in trange(len(pt)):
        r = remote('saturn.picoctf.net', 52339)
        r.sendlineafter(b'hex: ', pt[i].encode('utf-8').hex().encode())
        r.recvuntil(b'power measurement result:  ')
        pm = r.recvline().decode().strip()
        json_file[i] = {}
        json_file[i]["pt"] = [ord(digit) for digit in pt[i]]
        json_file[i]["pm"] = pm

        r.close()

    json_object = json.dumps(json_file)
    with open("./Crypto/PowerAnalysis- Part 1/trace.json", 'w') as outfile:
        outfile.write(json_object)
    ```
* 然後再去解析AES key
    ```python
    import json
    from tqdm import trange
    import numpy as np
    import copy
    from string import ascii_letters, digits
    from numpy import corrcoef
    import matplotlib.pyplot as plt
    from scipy.stats import pearsonr

    jsonFile = open('./PicoCTF/Crypto/PowerAnalysis- Part 1/trace.json', 'r')
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
        # ct_col = []
        trace_col = []
        for bytes in range(16):
            tmp_pt_col = []
            # tmp_ct_col = []
            for trace_idx in range(len(json_data)):
                tmp_pt_col.append(json_data[trace_idx]['pt'][bytes])
                # tmp_ct_col.append(json_data[trace_idx]['ct'][bytes])
            pt_col.append(tmp_pt_col)
            # ct_col.append(tmp_ct_col)
        for point in range(300, 400):#len(json_data[0]['pm'])
            tmp_trace_col = []
            for trace_idx in range(len(json_data)):
                tmp_trace_col.append(json_data[trace_idx]['pm'][point])
            trace_col.append(tmp_trace_col)

        return pt_col, trace_col

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
        for i in trange(len(hw_model_col_result)):#(ascii_letters + digits).encode():
            for j in range(biggest_length):#len(trace_col)
                # correlation_result.append(corrcoef(hw_model_col_result[i], trace_col[j])[0, -1])
                # correlation_result.append(pearsonr(hw_model_col_result[i], trace_col[j])[0])
                correlation_result.append(run_pearson_correlation(hw_model_col_result[i], trace_col[j]))
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
        plt.savefig(fname="./PicoCTF/Crypto/PowerAnalysis- Part 1/pt_" + str(offset) + ".jpg")
        plt.clf()

    # display_pt(1, (0, 700))
    # display_pt(1)
    pt_col, trace_col = data_preprocess(j)
    flag = ''
    biggest_length = 100#len(trace_col)
    for idx in trange(16):
        sbox_preprocess_result = sbox_preprocess(pt_col[idx])
        choose_sbox_result = choose_sbox(sbox_preprocess_result)
        hw_model_col_result = cal_hamming_weight(choose_sbox_result)
        correlation_result = cal_correlation(hw_model_col_result, trace_col)
        key_idx = correlation_result.index(max(correlation_result))
        # flag += (ascii_letters + digits)[key_idx // biggest_length]
        from Crypto.Util.number import long_to_bytes
        flag += long_to_bytes(key_idx // biggest_length).hex()


    print('The key of AES is: ' + flag )
    ```

Flag: `picoCTF{4999139026d84bf20427eb48d4edec53}`

---

### Exploit Part 2
為了不要讓主程式的變化太大，因此我有調整了一下data preprocessing的部分，還找到了一個bug，
:::spoiler Exp
```python
import json
from tqdm import trange
import numpy as np
import copy
from pathlib import Path
from numpy import corrcoef
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import ast

# root = "./PicoCTF/Crypto/PowerAnalysis- Part 1/"
# jsonFile = open(root + 'traces.json', 'r')
# j = json.load(jsonFile)

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

def data_prepreprocess():
    pts = []
    traces = []
    for f in Path("./PicoCTF/Crypto/PowerAnalysis- Part 2/traces").iterdir():
        l = f.read_text().splitlines()
        pt = bytes.fromhex(l[0].split(": ")[1])
        trace = ast.literal_eval(l[1].split(": ")[1])
        pts.append(pt.hex())
        traces.append(trace)
    return pts, traces

def data_preprocess(pts, traces):
    pt_col = []
    trace_col = []
    for bytes in range(16):
        tmp_pt_col = []
        for trace_idx in range(len(pts)):
            tmp_pt_col.append(int(pts[trace_idx][bytes*2:(bytes*2)+2], 16))
        pt_col.append(tmp_pt_col)
    for point in range(300, 400):#len(json_data[0]['pm'])
        tmp_trace_col = []
        for trace_idx in range(len(pts)):
            tmp_trace_col.append(traces[trace_idx][point])
        trace_col.append(tmp_trace_col)
    
    return pt_col, trace_col

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
        for trace in range(len(sbox_result_tmp[0])):
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
    for i in trange(len(hw_model_col_result)):#(ascii_letters + digits).encode():
        for j in range(biggest_length):#len(trace_col)
            # correlation_result.append(corrcoef(hw_model_col_result[i], trace_col[j])[0, -1])
            # correlation_result.append(pearsonr(hw_model_col_result[i], trace_col[j])[0])
            correlation_result.append(run_pearson_correlation(hw_model_col_result[i], trace_col[j]))
    return correlation_result
            
def run_pearson_correlation(x, y):
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    covariance = np.sum((x - mean_x) * (y - mean_y))
    
    std_dev_x = np.sqrt(np.sum((x - mean_x)**2))
    std_dev_y = np.sqrt(np.sum((y - mean_y)**2))
    
    correlation = covariance / (std_dev_x * std_dev_y)
    
    return correlation

def display_pt(offset:int, traces, data_offset = (0, 2666)):
    plt.plot(range(data_offset[0], data_offset[1]), traces[offset][data_offset[0]:data_offset[1]])
    plt.savefig(fname="./PicoCTF/Crypto/PowerAnalysis- Part 2/pt_" + str(offset) + ".jpg")
    plt.clf()

pts, traces = data_prepreprocess()
# display_pt(1, (0, 700))
# display_pt(1, traces, (0, 2666))
pt_col, trace_col = data_preprocess(pts, traces)
flag = ''
biggest_length = 100#len(trace_col)
for idx in trange(16):
    sbox_preprocess_result = sbox_preprocess(pt_col[idx])
    choose_sbox_result = choose_sbox(sbox_preprocess_result)
    hw_model_col_result = cal_hamming_weight(choose_sbox_result)
    correlation_result = cal_correlation(hw_model_col_result, trace_col)
    key_idx = correlation_result.index(max(correlation_result))
    # flag += (ascii_letters + digits)[key_idx // biggest_length]
    from Crypto.Util.number import long_to_bytes
    flag += long_to_bytes(key_idx // biggest_length).hex()


print('The key of AES is: ' + flag )
```
:::

Flag: `picoCTF{b7698f76b7e524ee7cd80dbde0cdff59}`