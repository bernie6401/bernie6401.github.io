---
title: Simple Crypto - 0x03(2023 Lab - COR)
tags: [eductf, Crypto, CTF]

category: "Security Course｜NTU CS｜Crypto"
date: 2024-01-31
---

# Simple Crypto - 0x03(2023 Lab - COR)
<!-- more -->

## Background
[Simple Crypto - 0x03(Lab - LFSR)](https://hackmd.io/@SBK6401/rkiE18Kas)

## Source Code
:::spoiler
```python
import random
from secret import FLAG

class LFSR:
    def __init__(self, tap, state):
        self._tap = tap
        self._state = state

    def getbit(self):
        f = sum([self._state[i] for i in self._tap]) & 1
        x = self._state[0]
        self._state = self._state[1:] + [f]
        return x

class triLFSR:
    def __init__(self, lfsr1, lfsr2, lfsr3):
        self.lfsr1 = lfsr1
        self.lfsr2 = lfsr2
        self.lfsr3 = lfsr3

    def getbit(self):
        x1 = self.lfsr1.getbit()
        x2 = self.lfsr2.getbit()
        x3 = self.lfsr3.getbit()
        return x2 if x1 else x3

lfsr1 = LFSR([0, 1, 2, 5], [random.randrange(2) for _ in range(19)])
lfsr2 = LFSR([0, 1, 2, 5], [random.randrange(2) for _ in range(23)])
lfsr3 = LFSR([0, 1, 2, 5], [random.randrange(2) for _ in range(27)])
cipher = triLFSR(lfsr1, lfsr2, lfsr3)
flag = map(int, ''.join(["{:08b}".format(c) for c in FLAG]))

output = []
for _ in range(200):
    output.append(cipher.getbit())

for b in flag:
    output.append(cipher.getbit() ^ b)

print(output)
# [0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0]
```
:::

## Recon
這是一個簡單的LFSR題目，基本上和去年的題目一樣，只是有一些小變動，諸如taps或是bits的強度不一樣之類的，但經過調整後還是可以沿用去年寫的script，
1. 簡單來說，雖然題目使用了三層的LFSR確保每一次getBit都會有一定的亂度，但因為x2和x3對於output而言有75%的高機率重複性(如下圖)，所以我們可以針對這一店進行correlation attack，也就是我們可以猜LFSR2和LFSR3的輸出情況(枚舉)，既然output和LFSR2/3各有75%重複，我們可以個別猜，也就是先對其中個枚舉，然後對照output和LFSR吐出的gussing output有沒有超過threshold(例如70%)，如果有就可以把該guessing state存起來，基本上guessing state應該高機率只會有一個，但就算高過一個也沒關係，反正之後要找LFSR1時，再個別考慮即可
![](https://hackmd.io/_uploads/ryG6Y5Gep.png)

2. 等到個別找到LFSR2/3後，就可以模擬一開始的算法，題目一開始產生output的方式是`x2 if x1 else x3`，所以就像找LFSR2/3一樣，只是把threshold調到1，全部找完之後久可以得到flag了

## Exploit
:::spoiler Whole Script
```python
from tqdm import trange

def initialize():
    f = '0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0'
    f = f.split(', ')

    # The first 232 is flag with encrypted
    cipher_text = []
    cipher_flag = []
    for i in range(len(f)):
        if i > 199:
            cipher_flag.append(int(f[i]))
        else:
            cipher_text.append(int(f[i]))
    return cipher_flag, cipher_text

def cal_correlation(a, b):
    count = 0
    for i in range(200):
        if a[i] == b[i]:
            count += 1
    return count / 200

class LFSR:
    def __init__(self, tap, state):
        self._tap = tap
        self._state = state

    def getbit(self):
        f = sum([self._state[i] for i in self._tap]) & 1
        x = self._state[0]
        self._state = self._state[1:] + [f]
        return x

class triLFSR:
    def __init__(self, lfsr1, lfsr2, lfsr3):
        self.lfsr1 = lfsr1
        self.lfsr2 = lfsr2
        self.lfsr3 = lfsr3

    def getbit(self):
        x1 = self.lfsr1.getbit()
        x2 = self.lfsr2.getbit()
        x3 = self.lfsr3.getbit()
        return x2 if x1 else x3

def guess_state(state_size_pow, tap, cipher_text):
    guess_state = [0 for _ in range(state_size_pow)]  # Initial guess state
    result = []

    for state in trange(2**state_size_pow):
        guess_text = []
        lfsr = LFSR(tap, guess_state)

        for _ in range(200):
            guess_text.append(lfsr.getbit())

        for _ in range(216):
            lfsr.getbit()

        acc = cal_correlation(guess_text, cipher_text)
        if acc >= 0.70:
            print(guess_state)
            result.append(guess_state)
            break

        tmp = bin(state)[2:]
        guess_state = [0 for i in range(state_size_pow - len(tmp))] + [int(tmp[i]) for i in range(len(tmp))]

    return result

def final_guess(state_size_pow, tap, cipher_text, b_guess_state, c_guess_state):
    guess_state = [0 for _ in range(state_size_pow)]  # Initial guess state

    for state in trange(223926, 2**state_size_pow):
        guess_text = []
        lfsr1 = LFSR(tap[0], guess_state)
        lfsr2 = LFSR(tap[1], b_guess_state)
        lfsr3 = LFSR(tap[2], c_guess_state)
        cipher = triLFSR(lfsr1, lfsr2, lfsr3)

        for _ in range(200):
            guess_text.append(cipher.getbit())

        for _ in range(216):
            cipher.getbit()
            
        acc = cal_correlation(guess_text, cipher_text)
        if acc == 1:
            print(guess_state)
            return guess_state

        tmp = bin(state)[2:]
        guess_state = [0 for i in range(state_size_pow - len(tmp))] + [int(tmp[i]) for i in range(len(tmp))]

if __name__ == '__main__':
    cipher_flag, cipher_text = initialize()

    tap = [[0, 1, 2, 5], [0, 1, 2, 5], [0, 1, 2, 5]]

    B_guess_state = guess_state(23, tap[1], cipher_text)    # [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1]
    C_guess_state = guess_state(27, tap[2], cipher_text)  # [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1]
    A_guess_state = final_guess(19, tap, cipher_text, B_guess_state, C_guess_state) # [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]

    # B_guess_state = [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1]
    # C_guess_state = [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1]
    # A_guess_state = [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]

    lfsr1 = LFSR(tap[0], A_guess_state)
    lfsr2 = LFSR(tap[1], B_guess_state)
    lfsr3 = LFSR(tap[2], C_guess_state)
    cipher = triLFSR(lfsr1, lfsr2, lfsr3)

    output = []
    plaintext_bin = ''
    plaintext_hex = ''
    tmp = []

    for _ in range(200):
        tmp.append(cipher.getbit())
    assert tmp == cipher_text
    for i, b in enumerate(cipher_flag):
        plaintext_bin += str(cipher.getbit() ^ b)

        if (i+1) % 8 == 0:
            plaintext_hex += hex(int(plaintext_bin, 2))[2:]
            plaintext_bin = ''
    print(bytes.fromhex(plaintext_hex).decode("cp437"))
```
:::