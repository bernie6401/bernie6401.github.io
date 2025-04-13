---
title: PicoCTF - scrambled-bytes
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/Flow"
---

# PicoCTF - scrambled-bytes

## Background
[盤點一款 Python 發包收包利器 - scapy](https://www.readfog.com/a/1635090435931213824)
> ### 只發不收
> ```python
> send(pkt, inter=0, loop=0, count=1, iface=N) 
> pkt:數據包
> inter：發包間隔時間
> count：發包數量
> iface：網卡接口名稱
> send()，在第三層發包，沒有接收功能；send(IP(dst="www.baidu.com",ttl=2)/ICMP())
> sendp()，在第二層發包，沒有接收功能。sr(Ether()/IP(dst="www.baidu.com"))
> ```

[time-時間的訪問和轉換](https://docs.python.org/zh-tw/3/library/time.html#time.time)
[python 的pyshark庫如何使用](https://zhuanlan.zhihu.com/p/602431298)
[PyShark入門(2)：FileCapture和LiveCapture模塊](https://segmentfault.com/a/1190000006064442)

## Source code
:::spoiler Source Code
```python=
#!/usr/bin/env python3

import argparse
from progress.bar import IncrementalBar

from scapy.all import *
import ipaddress

import random
from time import time

def check_ip(ip):
  try:
    return ipaddress.ip_address(ip)
  except:
    raise argparse.ArgumentTypeError(f'{ip} is an invalid address')

def check_port(port):
  try:
    port = int(port)
    if port < 1 or port > 65535:
      raise ValueError
    return port
  except:
    raise argparse.ArgumentTypeError(f'{port} is an invalid port')

def main(args):
  with open(args.input, 'rb') as f:
    payload = bytearray(f.read())
  random.seed(int(time()))
  random.shuffle(payload)
  with IncrementalBar('Sending', max=len(payload)) as bar:
    for b in payload:
      send(
        IP(dst=str(args.destination)) /
        UDP(sport=random.randrange(65536), dport=args.port) /
        Raw(load=bytes([b^random.randrange(256)])),
      verbose=False)
      bar.next()

if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('destination', help='destination IP address', type=check_ip)
  parser.add_argument('port', help='destination port number', type=check_port)
  parser.add_argument('input', help='input file')
  main(parser.parse_args())
```
:::

## Recon
這一題真的沒必要出的那麼複雜，有點硬要的感覺，不喜歡...，不看[^picoMini-misc-scrambled-bytes-wp-0x534b]我已經猜到八成了，但我感受到一股惡意...

1. Recon pcapng & Source Code
一開始我先做基本的packet的recon，然後沒啥發現，他的description寫說: `I sent my secret flag over the wires, but the bytes got all mixed up!`
代表他應該是傳了一些東西，然後把network flow記錄下來，可以看一下source code也的確是這樣，但標題和內文就有提示，說明他有打亂要transfer的東西，不過因為我不知道實際執行這支程式後，wireshark到底會錄到怎麼樣的東西，應該說形式上到底長怎樣，所以為了確定就直接reproduce一下
2. Reproduce the outcome
    Q1: 先說，如果用wsl的環境下command，但會出現以下error
    ```bash!
    $ python send.py 192.168.137.2 8888 test_flag.txt
    Sending |                                | 0/22
    Traceback (most recent call last):
      File "send.py", line 46, in <module>
        main(parser.parse_args())
      File "send.py", line 34, in main
        send(
      File "/home/sbk6401/.local/lib/python3.8/site-packages/scapy/sendrecv.py", line 445, in send
        return _send(
      File "/home/sbk6401/.local/lib/python3.8/site-packages/scapy/sendrecv.py", line 414, in _send
        socket = socket or _func(iface)(iface=iface, **kargs)
      File "/home/sbk6401/.local/lib/python3.8/site-packages/scapy/arch/linux.py", line 484, in __init__
        self.ins = socket.socket(
      File "/home/sbk6401/anaconda3/envs/CTF/lib/python3.8/socket.py", line 231, in __init__
        _socket.socket.__init__(self, family, type, proto, fileno)
    PermissionError: [Errno 1] Operation not permitted
    ```
    根據[^permissionerror-operation-not-permitted]的說明，應該是沒有用sudo，但如果用sudo又會出現`no module named scapy`或是`no module named progress`的問題，解決方式就是直接進入root然後安裝這兩個library，如果沒有進入root然後看pip list其實會看到這兩個library我之前就裝過了，但root好像不是找一般放library的地方
    ```bash!
    $ sudo su
    # pip install scapy; pip install progress
    # exit
    ```
    
    Q2: 另外一個問題可能會是如[^env-python\r-no-such-file-or-directory]提到的，因為unix系統的換行和一般的windows不一樣，所以要轉換一下
    
    以上問題都解決之後，就可以利用wireshark抓一下中間過程會有甚麼特別的東西，首先我傳送的`test_flag.txt`的內容是`picoCTF{test_12345678}`，總共要傳送22個bytes，可以看到的確他一次是傳送一個bytes，然後是用UDP傳送，destination IP也是我們指定的`192.168.137.2`，但是會發現他每一個packet所帶的data，都和我們的flag沒有任何關聯，再回去看一下他在傳送前做了哪些事情，首先他在31行做了shuffle，然後在傳送前和產生的random number進行XOR，所以才會看起來都不一樣
    ![](https://hackmd.io/_uploads/SJAfx3763.png)
3. Extract Data
到這邊我們就成功一半了，接著就是把data dump下來進行還原就好(開始感受痛苦吧!一袋米要扛幾樓)，我們把data印出來後就可以直接拿來用
    ```python!
    import pyshark

    capture = pyshark.FileCapture('./capture.pcapng', display_filter='udp and ip.dst == 172.17.0.3 and !icmp')

    data = []
    for pkt in capture:
        try:
            data.append(pkt.data.data)
        except:
            pass
    print(data)
    ```
    * ==陷阱一==
    如果觀察data的length會發現他只有==1990==，但是用wireshark卻filter出==1992==，仔細看會發現有兩個data是unknown(No.1943那個不算)
    ![](https://hackmd.io/_uploads/SkJTQnX6h.png)
    他應該是抓不到No. 4777的0x23和No.10562的0x0f，所以要手動把這兩個數值插入我們的list中
    
4. Recover input.txt
首先他有先利用time()的epoch當作random的seed，所以我是先看第一個傳送的packet他的時間是==1614044650==，當作他的seed，接下來只要有關random的操作都要和send.py一模一樣
![](https://hackmd.io/_uploads/H1m-rhXpn.png)
由於我們還要考慮到他有事先進行shuffle，所以還要想辦法把順序調整回來，這邊我是參考[^picoMini-misc-scrambled-bytes-wp-0x534b]的方式，先建立一個大小為len(data)的list，再針對這個list進行shuffle，就可以得到一模一樣的順序，接著我們就把data和random所產出的東西做XOR就可以放回去到對應的index
    * ==陷阱二==
    這邊就不是原作者的鍋，反而是參考的WP有問題，原本是想說可以直接試看看[^picoMini-misc-scrambled-bytes-wp-0x534b]寫的腳本，但怎麼樣都沒有像是圖片的byte code出現，幾經波折後才發現原來用他的腳本會在data list的最後多一個null element，這會導致len(data)不是1992而是1993，這樣shuffle的結果可想而知一定不一樣，我也回報給原作者了[^report-error-to-0x534b]，就看他要不要修
只要把最後的random byte $\oplus$ data的結果寫回去到一個file，就會發現是一個png圖檔，那就是flag

## Exploit
```python=
from time import time
import random
# import pyshark

# capture = pyshark.FileCapture('./capture.pcapng', display_filter='udp and ip.dst == 172.17.0.3 and !icmp')

# data = []
# for pkt in capture:
#     try:
#         data.append(pkt.data.data)
#     except:
#         pass
# print(data)
data = ['3b', '04', '79', '27', '76', 'd2', '88', 'b9', 'ba', '7b', 'fe', '15', '78', 'e5', '5c', '8d', 'ac', 'fa', '1b', 'a2', '48', '63', '04', 'bc', '40', 'dc', 'd1', '56', 'f3', 'd4', '82', '97', '95', 'fa', 'd1', '27', '88', '6c', 'df', '9c', '73', '67', 'f4', '93', '9d', '5e', '72', '0d', 'ae', '9a', '05', 'be', 'b0', '12', '6b', '81', '92', '46', '0f', '92', '70', '23', '2b', '44', '38', '71', 'e3', '18', 'fc', '8d', '3e', '58', 'bd', 'f8', 'ff', '72', '61', 'f9', 'aa', 'b8', 'f5', 'f3', '87', '2f', '5e', 'cc', '4b', '86', '25', 'd1', '95', '4f', '41', 'c2', '91', '93', '61', '10', 'f5', '9d', '96', 'de', '1c', 'e3', '1a', '54', '6d', '0a', '51', '3b', 'dd', '53', 'cf', 'ba', '12', 'c9', 'a5', 'e5', '5f', 'c9', '15', 'b5', '8c', '97', '90', '1a', 'db', 'fe', 'b7', 'c9', 'e3', '47', '32', 'b5', '92', '63', '0d', '8b', '37', 'e7', '3c', '1b', '73', 'bd', '87', '0b', '89', '6b', '66', 'dc', 'fa', 'e8', '3a', '9b', '47', '53', '35', 'db', '71', '98', 'e4', 'd1', '5e', 'b0', '88', '59', 'fd', 'c5', 'dd', '87', 'e4', 'a9', '02', '64', '01', '26', '25', '9d', 'e5', '37', 'a3', '3e', '74', '8a', '56', 'de', 'e8', '52', '87', '8d', '01', 'c5', '80', '2a', '35', 'bd', '11', 'e0', '04', 'd0', '8d', 'db', '22', 'a9', 'cb', '17', 'ad', 'e2', '1d', '48', 'ea', 'ca', 'c5', '1b', 'a7', '93', 'ff', '07', '82', '6d', '4b', '74', '6c', '5f', 'd4', '8b', '53', '32', 'f5', '16', '9a', '2c', '58', '45', 'b3', '61', '77', '0f', 'b0', '84', '54', '51', '27', 'f8', '6d', 'f1', 'd9', 'e1', '1e', '2f', '3c', 'd6', '06', 'e6', 'b6', '7f', '8b', 'a7', '36', '03', '7c', 'cf', '2e', '90', 'fc', '47', 'ad', 'dd', 'd7', 'a2', '1d', '7d', '0c', '44', '6d', 'b0', 'd3', 'e1', 'f3', 'f4', '9b', 'b5', '88', 'c9', 'dc', '11', 'de', '22', '89', '1b', 'f3', 'c5', '96', '60', 'e2', '2d', '6c', 'e2', '87', '51', 'fd', '29', '86', '3e', 'c2', 'e9', 'd1', 'a4', '05', '9a', 'bd', '09', '1d', '44', 'b4', 'da', '73', '98', '0c', 'd3', 'fb', '8c', '33', '3e', '91', 'ed', '83', '4a', '91', '59', '2f', '94', '78', '06', 'fe', '66', '84', '7b', 'ea', 'ba', 'cc', 'ef', 'fe', 'f1', '5f', 'c3', '5c', '79', '6f', '70', 'dd', '37', '17', '4d', '43', '20', '15', '1b', 'bc', '34', '39', 'f3', 'b6', '3f', '1c', 'b0', 'ce', '47', '12', 'b8', '39', '8c', '05', 'a1', 'b0', 'ce', 'ce', '25', '0f', '9c', '70', 'ed', '49', 'c5', 'ec', '86', '9e', '56', '5a', '89', '93', '3d', '0a', '95', 'ca', '4f', '42', '7a', '34', '05', 'be', '20', '2c', '4e', '2d', 'af', '31', '4c', '7c', '0f', '25', 'd6', '32', 'f1', 'f7', '2e', '5b', '1a', '49', '2e', '42', '82', '60', '13', '69', '33', 'b4', '90', 'a2', '44', '08', '72', '06', '23', '92', 'c0', 'e9', '25', 'd8', '45', '5e', '89', '35', '13', 'de', 'f2', 'ad', 'ae', '61', '0e', '0a', '68', 'cb', 'd2', '55', 'a3', '68', '60', '5f', '7f', 'f5', 'a8', '7e', '4f', '44', '95', '0a', '6c', '38', '5c', '1f', 'a7', '1b', '16', '07', '88', '98', '26', '72', '99', '2d', 'e7', '54', 'e2', 'b8', '6e', 'd3', 'af', '5b', '2b', '98', '7c', '8b', 'd6', 'c4', '0b', '06', 'dc', '38', 'f0', '45', 'cb', '70', 'f9', '61', 'f8', 'bb', '27', 'e6', 'f9', '0b', '05', 'ba', 'ba', 'bf', 'b8', 'c5', '03', '90', '88', '5c', '00', '08', '5c', 'd0', '31', '5b', '50', 'c7', 'ae', 'a0', '07', '42', 'd1', '0b', 'd5', 'fe', '9c', '6e', '07', '56', 'c1', '13', 'eb', '4e', 'ae', '83', '20', '0c', '1f', 'e4', '4c', 'c1', 'ab', '20', '5c', '8c', 'f3', '97', '66', 'af', '1c', 'af', '0b', '42', 'e2', 'fd', '35', 'fa', '45', '0d', '86', '37', 'e2', 'c6', '22', '4b', '48', '19', 'eb', '2a', '53', '52', 'e6', '41', '39', 'd6', '45', '1f', '1d', 'e3', 'ce', 'a6', '31', 'd0', 'd8', 'ec', 'ea', '3d', 'ff', '7a', '6b', '4f', '8c', '72', 'c8', 'bc', 'f0', 'f9', 'e0', '46', '31', '49', '8e', 'eb', 'f8', '28', 'dd', '3f', '90', '44', '71', 'b2', '25', 'a3', '3a', 'c1', 'f5', '24', '1c', '0b', '3b', 'd3', '86', 'e8', 'e7', '69', 'e7', '08', '03', '9c', '4d', 'ea', 'ee', '5f', '4f', '32', '28', '33', 'f0', 'a4', 'c6', '64', 'bb', 'cd', 'e0', '44', '4a', '96', 'ed', 'f7', '2d', '48', '3b', '62', 'a5', '54', 'a4', 'e7', 'b1', 'fd', 'f6', '59', 'fc', '13', '80', '47', '8f', '7b', '2c', '93', 'f6', 'bf', '76', '61', '8d', '71', '3c', 'e6', 'fb', '05', '00', 'a7', 'f6', '00', '2c', '8a', '18', '5a', '85', '9e', '8f', '3c', '1f', 'be', '87', 'f1', '7d', '32', 'f6', '57', 'c5', 'd8', '95', 'f5', '96', 'b5', '38', '8a', '95', '7f', '48', 'fa', '26', '66', '8e', '8e', 'ef', '68', '1e', '9d', '73', '23', '99', '7c', '2e', 'b7', '4e', 'ca', '72', 'ff', '2a', 'fd', '1e', '6e', '08', '4f', '63', '2a', '8e', '7b', '36', '4b', '64', 'c3', 'cc', '74', 'cd', '0f', '7a', '80', '9f', 'dc', 'dd', '16', '56', 'c5', '6a', 'd3', '8c', '87', '8a', 'b9', '7b', '90', '7d', '83', 'c7', 'ed', 'e4', '60', 'df', '9b', '80', 'a0', '3d', 'cc', '83', '56', 'c2', '83', 'f9', '9a', 'e8', '1d', '10', '41', '1f', 'c8', '29', 'cb', '36', '1c', '28', 'd8', '54', '55', 'ff', '04', '84', '15', '7f', 'ff', '35', '49', 'e9', '0e', 'a9', '64', '40', 'c8', '73', '54', '9f', 'e0', 'b4', '42', '54', '9a', 'df', '59', '49', '8d', '67', '60', '39', 'af', 'd4', 'ce', '73', '85', '4f', '9c', '12', 'bf', 'b6', '4f', '99', '1a', '9b', '3b', '59', '64', '0e', 'f4', '53', 'e6', 'b8', 'b1', '3e', 'fd', '66', '21', 'e5', '35', 'e6', '7b', '4e', '81', 'f3', '74', '9c', 'da', '9f', '46', 'e5', 'e8', '1d', 'a7', 'a4', '7a', 'd3', '3f', '5d', 'a7', '8d', 'fc', 'd0', '13', '21', '47', '76', 'c3', '8c', '27', 'a7', '09', '8f', 'e7', '85', '41', '23', 'ea', 'b4', 'cb', 'eb', 'a9', '4c', '7b', 'd2', '9e', '4a', 'ee', 'be', '6d', 'f0', '67', 'bf', '95', '33', '06', 'dd', 'd9', '06', '86', '28', '24', 'b2', 'ad', '84', '04', 'ed', '61', '3c', '6a', '05', 'e1', '60', '20', '77', '8a', '88', 'f5', '79', 'a0', 'c5', 'a9', '42', 'c6', '8b', '72', 'bd', '98', '6e', 'f8', '39', '52', '47', '04', '6b', '8a', 'ad', '07', '4e', 'f4', '8b', '45', 'e4', '4e', '80', 'd9', '5f', 'd6', 'ee', '53', '21', 'b5', 'bb', '5d', '19', '94', '87', '01', 'e6', '6d', 'ff', 'ef', '72', '51', 'f3', '58', '71', 'b8', '86', 'dc', '69', '5e', 'a1', '1d', '80', '1d', '4f', '20', '9b', '7b', '99', 'a0', '98', '86', '32', 'fa', '0e', 'f7', 'b0', '6d', '1d', '4e', '93', 'f0', '1d', '8a', '25', '95', 'c8', '7a', '69', '98', 'fb', '3c', 'fa', '0d', '51', 'd6', 'e4', '4b', '52', '4a', '5c', '06', '5a', '4d', '7c', '8a', '86', 'c0', '6f', '85', 'df', 'ec', 'd1', '6d', 'de', 'd9', '4a', '27', 'e2', '66', '37', 'd5', 'c1', '29', '2e', 'ac', 'ab', '0b', '39', '2a', '35', '6c', '42', 'ed', '9c', '39', '01', '05', '40', '24', '3f', '07', '0b', 'bb', 'c6', '5c', 'ab', '6f', '38', 'c2', '58', '32', 'e3', '7f', 'aa', 'df', '3b', '03', 'c4', '99', '1b', '5f', '04', '22', '2b', '37', 'ce', '56', '8b', '14', '6e', '75', '1d', '48', '23', 'c8', '47', 'c8', '5d', '2b', '7e', '1b', 'c9', '6a', 'aa', '1f', 'e0', '24', 'dd', '93', '83', '29', '4f', '27', 'd4', '0a', '64', '61', '44', 'fb', 'f8', 'dc', '4c', '9c', '42', 'cf', 'dc', '6a', '00', '15', '35', 'd2', 'b9', '20', '3f', '75', 'f6', 'e2', '26', 'b7', '76', '7c', '8f', 'd3', '66', '6f', 'fa', '12', 'e6', '0a', '56', '46', '9c', '00', 'e3', 'f0', '55', '97', 'd4', '02', '45', '49', '5e', 'bc', '42', '15', '6e', '9e', '70', '18', 'fb', 'a8', '93', 'c3', '42', '9f', '2e', '93', 'ff', 'ba', '50', '7e', '2f', '3b', '3f', 'ee', '81', '18', 'ac', 'fc', '40', '62', 'ef', '65', 'ea', 'd6', 'd8', '36', '77', '7a', '98', 'ad', 'a6', '8f', '55', 'cb', '5c', '9e', '1d', 'cc', '73', '8d', '55', 'a1', '7f', 'd5', 'cc', '78', '5e', 'e3', '69', '3a', 'f2', '6f', '6a', '7a', '18', '03', '76', 'bc', '6c', 'bd', '39', '7e', 'bf', 'e8', '8f', '22', 'ed', '28', 'db', 'be', 'e7', '66', '68', '61', 'b1', 'ac', 'd3', '15', '3b', '3c', 'c3', '1e', '5d', '47', '04', '56', 'f0', '36', 'a5', 'c0', 'f6', '16', 'fe', '20', '04', '56', '28', '7c', '5d', '68', '53', '15', 'e6', '55', 'bd', '1d', '58', 'bf', '0f', 'f9', '80', '3d', 'b3', '2d', '3d', '4c', '9a', '34', '3e', 'cb', 'f3', '38', '3b', '42', '7d', 'ff', 'd5', '57', '91', 'ec', 'ee', 'b2', '8b', '27', '8a', 'fa', 'e6', '08', '34', '38', '0f', '30', 'ab', '3d', 'f8', 'af', '99', '54', 'b1', 'de', '97', '8c', '03', 'aa', '43', 'd0', 'bc', '76', '35', '3d', 'fa', 'ba', 'c5', '03', 'c2', '8e', '8c', '83', 'd9', '4a', 'f0', 'cc', '8f', '1c', '40', 'c1', 'cd', '3e', '40', 'f1', '91', 'b2', '3d', 'a2', 'b9', 'ac', 'ba', '94', '7b', 'd3', '9a', '26', 'f5', '41', '0c', '22', '7f', '7c', '71', '7f', '9b', 'f5', 'e3', '1a', 'f6', '06', 'fd', '42', 'f3', 'e3', '0e', 'e0', '13', '37', '02', '3b', '44', '14', '29', '1f', 'a7', 'cb', '28', '37', 'f2', 'a2', 'b1', '5b', '84', '38', '50', 'ce', '68', '98', '02', '46', 'ca', '6c', '71', '05', '08', '7f', '34', '84', 'cb', 'a7', '3c', '62', 'bd', '73', 'ea', '3a', '68', '1e', 'f7', 'ba', '73', 'fb', '01', '0f', '43', '7d', 'e3', '39', 'd2', '66', '3a', '82', '8a', '7b', 'ca', '9f', 'ef', '66', '30', 'e4', 'ff', '9e', 'dc', '6e', '0e', '1d', '45', 'b0', 'fb', '63', 'd6', '45', '60', 'b9', 'd8', '8d', 'f1', 'd8', '40', '29', 'b0', '07', '0f', '11', '2f', '7a', '56', '7d', '1d', '90', 'c1', 'e9', '70', 'e1', 'd9', 'b0', 'b3', 'ae', '4a', '61', '89', 'd4', '67', '2f', 'ca', '5a', '93', '4b', 'fe', '10', '3c', '90', '9f', '7b', '9e', 'e8', '41', 'b4', '78', 'ef', 'b3', '95', '37', '94', '11', '5f', 'be', 'a2', 'db', '6c', '36', '28', '69', '13', '36', '7c', '1f', '63', 'f9', 'fb', '16', '80', '62', '6d', 'd4', '20', '08', '9c', '8c', 'ba', 'f7', 'd0', '61', '9f', '0c', 'ac', '04', 'de', '7c', 'c9', 'a6', '55', 'fe', '8a', 'ec', 'ab', '79', '30', 'f1', 'c5', '55', 'af', '3b', '6c', '24', 'd7', '9f', '8c', 'bb', '75', '2e', '03', '9e', '1c', '05', 'b5', '24', 'b1', '21', 'ec', '18', '3a', 'dc', 'e9', '71', 'a8', 'c9', 'be', '4c', '7d', 'fa', 'd4', 'e9', '73', 'e0', '91', '45', '71', '39', '3a', '57', 'd4', '8d', '8d', 'a2', 'd5', '21', '59', 'b2', '7b', '24', '57', 'ab', '7d', '90', 'ee', 'e0', 'd4', 'fa', 'df', '24', '26', '78', '30', '95', 'f9', '20', 'ad', '54', 'dd', 'd7', '19', '52', 'bf', '7c', 'db', '06', 'db', '55', '66', '21', 'c2', '91', '05', '48', '8e', '8e', 'e9', 'f9', '24', 'ab', 'c1', 'a4', 'b7', '50', '58', '1b', 'd6', '13', '6b', 'c5', '86', 'd3', '41', '33', 'f8', '1f', '38', '6c', '11', '1a', '98', '3a', 'bb', '4b', 'f3', 'a6', 'f8', '98', '33', 'c9', 'fb', '3a', 'b9', '0f', 'f7', '0a', '18', 'eb', '34', '1f', '2f', '83', 'e0', '26', '2e', 'e9', '3d', '62', '29', '9d', '5c', 'ff', 'a6', 'bb', '3e', '6b', '42', '48', '4c', 'b1', 'cd', 'a3', '71', '83', 'ea', '2f', 'e4', '33', '50', '6a', '15', 'f3', 'f1', '52', 'c4', '4c', 'fa', 'c8', '5f', '44', '46', 'c3', '9a', '68', 'e8', '4f', '7e', '17', '31', 'c2', 'bd', '96', '7f', '1d', 'c6', '1b', '8b', 'c8', '37', '8d', '88', '9d', 'aa', 'da', '6b', 'ce', '55', 'c0', 'e5', '59', 'd2', 'e8', 'cb', 'df', 'ed', '69', '25', 'c5', '0d', '0e', '77', '52', '76', 'b0', 'f7', 'f1', 'c9', '55', '25', '86', '40', '3b', '68', '08', '5f', 'da', '43', 'fe', '6c', 'ac', 'ff', 'ce', '6a', 'ff', 'bc', 'f5', 'e4', '41', '30', '8f', '7c', '34', '1b', '42', 'f7', 'b4', 'ca', '28', '53', 'fa', '7e', '3c', '28', 'db', 'b3', '90', 'fb', 'e7', '90', '1f', '13', 'de', '39', '37', '49', '2a', '96', 'fb', '2a', '73', '40', 'ee', '58', 'ce', 'a0', 'c1', '9c', '62', 'da', '2c', '82', 'ed', '26', 'c7', '76', '1a', 'eb', '43', '98', 'ce', '8f', '96', '3d', '76', '27', '02', '3a', '5d', '7c', '1d', 'a6', 'c4', '91', 'ef', 'a1', 'b1', 'd1', 'a5', 'b1', 'b4', 'b8', 'b3', '6f', 'ae', 'dd', '29', 'be', '88', 'ea', '2f', '81', '99', '46', '8f', '86', '0e', 'f2', '3f', '0f', 'c2', 'ed', 'b7', '81', 'db', '0f', '48', 'a9', 'b0', '7a', 'f2', '47', '7e', 'ab', '2c', '3f', '38', '90', '17', '12', 'd3', '9f', '5e', '73', 'e6', '13', '40', 'c3', '61', 'dc', '0b', 'b4', '0c', '38', 'e7', '94', '42', '41', 'dc', 'a9', 'f9', 'd9', '1f', '0b', '66', 'f4', 'b8', 'fb', '6d', '32', 'de', 'de', '0e', '65', '87', '58', 'a3', '6e', 'dd', '67', 'f6', '5c', '12', '4b', 'a3', 'ce', 'cc', 'bf', '65', 'b5', '6d', '9b', '00', '8b', '24', '11', '87', '6d', 'df', '1f', 'cc', 'd0', '45', 'f1', '16', '20', '08']
seed = 1614044650
random.seed(seed)
shuffle_idx = [i for i in range(len(data))]
print(len(shuffle_idx))
random.shuffle(shuffle_idx)
decoded = bytearray([0 for i in range(len(data))])

for i in range(len(data)):
    dummy = random.randrange(65536)
    tmp= int(data[i], 16) ^ random.randrange(256)
    decoded[shuffle_idx[i]] = tmp
print(decoded)

f = open('flag.png', 'wb')
f.write(decoded)
f.close()
```

![](https://hackmd.io/_uploads/S1R0qhQp3.png)
Flag: `picoCTF{n0_t1m3_t0_w4st3_5hufflin9_ar0und}`

## Reference
[^picoMini-misc-scrambled-bytes-wp-0x534b]:[PicoMini Misc scrambled-bytes WP - 0x534b](https://github.com/0x534b/ctf-writeups/blob/master/picoMini%20by%20redpwn%202021/scrambled-bytes.md)
[^permissionerror-operation-not-permitted]:[PermissionError: [Errno 1] Operation not permitted](https://stackoverflow.com/questions/44304988/permissionerror-errno-1-operation-not-permitted)
[^env-python\r-no-such-file-or-directory]:[env: python\r: No such file or directory](https://stackoverflow.com/questions/19425857/env-python-r-no-such-file-or-directory)
[^report-error-to-0x534b]:[Report the error](https://github.com/0x534b/ctf-writeups/issues/1)