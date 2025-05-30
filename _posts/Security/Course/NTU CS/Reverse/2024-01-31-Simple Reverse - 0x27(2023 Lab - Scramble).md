---
title: Simple Reverse - 0x27(2023 Lab - Scramble)
tags: [eductf, CTF, Reverse]

category: "Security/Course/NTU CS/Reverse"
---

# Simple Reverse - 0x27(2023 Lab - Scramble)
<!-- more -->

## Source code
:::spoiler scramble.py
```python
import random


def generate_scramble_pattern(pattern_length, max_shift, max_add_sub):
    scramble_pattern = []
    for _ in range(random.randint(1, pattern_length)):
        operation = random.randint(0, 3)
        
        if operation == 0:
            sub_value = random.randint(1, max_add_sub)
        elif operation == 1:
            add_value = random.randint(1, max_add_sub)
            scramble_pattern.append(('add', add_value))
        elif operation == 2:
            sub_value = random.randint(1, max_add_sub)
            scramble_pattern.append(('sub', sub_value))
        elif operation == 3:
            shift_value = random.randint(1, max_shift)
            scramble_pattern.append(('lsh', shift_value))
    
    return scramble_pattern

def apply_scramble_pattern(input_bytes, patterns):
    result = []
    for i, operations in enumerate(patterns):
        src = input_bytes[i]
        for operation in operations:
            if operation is None:
                continue
            elif operation[0] == 'add':
                src += operation[1]
            elif operation[0] == 'sub':
                src -= operation[1]
            elif operation[0] == 'lsh':
                src <<= operation[1]
            src &= 0xffffffff

        result.append(src)
    
    return result


k_FLAG = b'FLAG{REDACTED}' 
patterns = [generate_scramble_pattern(6, max_shift=10, max_add_sub=0xffff) for i in range(len(k_FLAG)) ]
scrambled_result = apply_scramble_pattern(k_FLAG, patterns)

print("Input Bytes:", k_FLAG, len(k_FLAG))
# REDACTED, 42
print("Scramble Pattern:", patterns)
# [[('sub', 20935)], [('sub', 31575), ('lsh', 9), ('add', 45363), ('add', 35372), ('sub', 15465)], [('add', 19123), ('add', 35260), ('sub', 49421), ('lsh', 8)], [('lsh', 1), ('sub', 4977), ('sub', 55837)], [('add', 16937)], [('sub', 56984), ('lsh', 2), ('sub', 32363), ('sub', 46293)], [('sub', 94), ('sub', 48860), ('sub', 18342), ('lsh', 3)], [('add', 37549), ('sub', 36283), ('lsh', 6), ('add', 6253)], [('add', 34661), ('sub', 13281), ('sub', 64107)], [('sub', 8525), ('sub', 30349), ('sub', 26744)], [('lsh', 2), ('sub', 18120), ('sub', 63091), ('add', 17287), ('sub', 37618), ('add', 2237)], [('sub', 48573), ('sub', 4449), ('add', 36013), ('sub', 64051)], [('add', 10415), ('lsh', 3), ('lsh', 10)], [('add', 5676), ('lsh', 3), ('lsh', 10), ('add', 32002), ('sub', 60775)], [('add', 35939), ('sub', 32666), ('sub', 45639), ('add', 2077), ('sub', 16253)], [('sub', 30392), ('sub', 26913), ('sub', 14009), ('sub', 62416)], [('sub', 15056), ('sub', 40527)], [('lsh', 5)], [('lsh', 1), ('sub', 16070)], [('add', 2045)], [('lsh', 8), ('add', 37087), ('sub', 22013), ('lsh', 10), ('lsh', 2)], [('add', 31880), ('sub', 56557), ('lsh', 6), ('lsh', 5), ('lsh', 8), ('add', 15535)], [('add', 22937), ('add', 4060)], [('add', 8462), ('sub', 4463), ('sub', 45810), ('lsh', 1)], [('sub', 10144), ('lsh', 8), ('lsh', 5), ('lsh', 1), ('lsh', 8)], [('add', 49937), ('lsh', 2), ('add', 60982), ('sub', 24799)], [('lsh', 4), ('add', 53340), ('add', 50619), ('sub', 56111), ('add', 6134), ('lsh', 1)], [('sub', 22577), ('sub', 50645)], [('add', 21265), ('sub', 41440)], [('add', 63314), ('sub', 45755), ('add', 62216)], [('sub', 52616)], [('add', 21192)], [('add', 62573), ('sub',18811)], [('add', 35452), ('sub', 11573), ('sub', 49079), ('sub', 36361), ('sub', 26862), ('lsh', 9)], [('add', 13610), ('lsh', 7), ('lsh', 3), ('sub', 28490), ('lsh', 10), ('add', 44742)], [('lsh', 10), ('sub', 1797), ('sub', 10564), ('add', 12394)], [('add', 45165), ('lsh', 10), ('sub', 60610), ('sub', 63002), ('sub', 14851), ('lsh', 1)], [('add', 34840), ('lsh', 3), ('sub', 16907)], [('add', 4404), ('lsh', 3), ('lsh', 7), ('lsh', 6)], [('lsh', 6), ('add', 51738), ('sub', 24621), ('add', 58646)], [('lsh', 1)], [('add', 29375), ('sub', 419), ('add', 2854), ('sub', 11878), ('lsh', 10), ('add', 40151)], [('add', 22953)]]
print("Scrambled Result:", scrambled_result)
# [4294946431, 4278905078, 1286912, 4294906624, 17060, 4294661164, 4294429720, 94573, 4294924666, 4294901787, 4294868383, 4294886344, 86147072, 47247259, 4294910851, 4294833676, 4294911813, 3040, 4294951460, 2160, 171843584, 4734127, 27100, 4294883864, 884998144, 236375, 111420, 4294894192, 4294947222, 79889, 4294914775, 21308, 43873, 4249743360, 1477674694, 113697, 92442178, 262757, 295239680, 91843, 210, 20569303, 23078]

```
:::
:::spoiler output.txt
```
[[('sub', 20935)], [('sub', 31575), ('lsh', 9), ('add', 45363), ('add', 35372), ('sub', 15465)], [('add', 19123), ('add', 35260), ('sub', 49421), ('lsh', 8)], [('lsh', 1), ('sub', 4977), ('sub', 55837)], [('add', 16937)], [('sub', 56984), ('lsh', 2), ('sub', 32363), ('sub', 46293)], [('sub', 94), ('sub', 48860), ('sub', 18342), ('lsh', 3)], [('add', 37549), ('sub', 36283), ('lsh', 6), ('add', 6253)], [('add', 34661), ('sub', 13281), ('sub', 64107)], [('sub', 8525), ('sub', 30349), ('sub', 26744)], [('lsh', 2), ('sub', 18120), ('sub', 63091), ('add', 17287), ('sub', 37618), ('add', 2237)], [('sub', 48573), ('sub', 4449), ('add', 36013), ('sub', 64051)], [('add', 10415), ('lsh', 3), ('lsh', 10)], [('add', 5676), ('lsh', 3), ('lsh', 10), ('add', 32002), ('sub', 60775)], [('add', 35939), ('sub', 32666), ('sub', 45639), ('add', 2077), ('sub', 16253)], [('sub', 30392), ('sub', 26913), ('sub', 14009), ('sub', 62416)], [('sub', 15056), ('sub', 40527)], [('lsh', 5)], [('lsh', 1), ('sub', 16070)], [('add', 2045)], [('lsh', 8), ('add', 37087), ('sub', 22013), ('lsh', 10), ('lsh', 2)], [('add', 31880), ('sub', 56557), ('lsh', 6), ('lsh', 5), ('lsh', 8), ('add', 15535)], [('add', 22937), ('add', 4060)], [('add', 8462), ('sub', 4463), ('sub', 45810), ('lsh', 1)], [('sub', 10144), ('lsh', 8), ('lsh', 5), ('lsh', 1), ('lsh', 8)], [('add', 49937), ('lsh', 2), ('add', 60982), ('sub', 24799)], [('lsh', 4), ('add', 53340), ('add', 50619), ('sub', 56111), ('add', 6134), ('lsh', 1)], [('sub', 22577), ('sub', 50645)], [('add', 21265), ('sub', 41440)], [('add', 63314), ('sub', 45755), ('add', 62216)], [('sub', 52616)], [('add', 21192)], [('add', 62573), ('sub',18811)], [('add', 35452), ('sub', 11573), ('sub', 49079), ('sub', 36361), ('sub', 26862), ('lsh', 9)], [('add', 13610), ('lsh', 7), ('lsh', 3), ('sub', 28490), ('lsh', 10), ('add', 44742)], [('lsh', 10), ('sub', 1797), ('sub', 10564), ('add', 12394)], [('add', 45165), ('lsh', 10), ('sub', 60610), ('sub', 63002), ('sub', 14851), ('lsh', 1)], [('add', 34840), ('lsh', 3), ('sub', 16907)], [('add', 4404), ('lsh', 3), ('lsh', 7), ('lsh', 6)], [('lsh', 6), ('add', 51738), ('sub', 24621), ('add', 58646)], [('lsh', 1)], [('add', 29375), ('sub', 419), ('add', 2854), ('sub', 11878), ('lsh', 10), ('add', 40151)], [('add', 22953)]]
[4294946431, 4278905078, 1286912, 4294906624, 17060, 4294661164, 4294429720, 94573, 4294924666, 4294901787, 4294868383, 4294886344, 86147072, 47247259, 4294910851, 4294833676, 4294911813, 3040, 4294951460, 2160, 171843584, 4734127, 27100, 4294883864, 884998144, 236375, 111420, 4294894192, 4294947222, 79889, 4294914775, 21308, 43873, 4249743360, 1477674694, 113697, 92442178, 262757, 295239680, 91843, 210, 20569303, 23078]

```
:::

## Recon
這一題先看source code會發現他做了一連串的scramble動作，包含加減和移位，而次數也不一定，他主要是針對flag中的每一個字元都做1~6次不等的操作，可能是加也可能是減甚至是移位，不過題目也有給我們這些pattern所以應該是可以直接透過這些pattern進行還原，但我們可以用z3下一大堆constraint就可以不用那麼麻煩了

z3的大致步驟:
1. 建立一個solver
2. 建立符號 - 以此lab來說就是建立43個符號對應每一個flag字元
3. 加上constraint - 以此lab來說每一個flag字元都應該限制在空白到0x7f之間，另外還要加上每一個符號(就是flag字元)，經過我們已知的scramble pattern之後應該要是最後的target
4. 判斷有無解，如果有的話就把每一個符號的值取出來

## Exploit
```python
from z3 import *

patters = [[('sub', 20935)], [('sub', 31575), ('lsh', 9), ('add', 45363), ('add', 35372), ('sub', 15465)], [('add', 19123), ('add', 35260), ('sub', 49421), ('lsh', 8)], [('lsh', 1), ('sub', 4977), ('sub', 55837)], [('add', 16937)], [('sub', 56984), ('lsh', 2), ('sub', 32363), ('sub', 46293)], [('sub', 94), ('sub', 48860), ('sub', 18342), ('lsh', 3)], [('add', 37549), ('sub', 36283), ('lsh', 6), ('add', 6253)], [('add', 34661), ('sub', 13281), ('sub', 64107)], [('sub', 8525), ('sub', 30349), ('sub', 26744)], [('lsh', 2), ('sub', 18120), ('sub', 63091), ('add', 17287), ('sub', 37618), ('add', 2237)], [('sub', 48573), ('sub', 4449), ('add', 36013), ('sub', 64051)], [('add', 10415), ('lsh', 3), ('lsh', 10)], [('add', 5676), ('lsh', 3), ('lsh', 10), ('add', 32002), ('sub', 60775)], [('add', 35939), ('sub', 32666), ('sub', 45639), ('add', 2077), ('sub', 16253)], [('sub', 30392), ('sub', 26913), ('sub', 14009), ('sub', 62416)], [('sub', 15056), ('sub', 40527)], [('lsh', 5)], [('lsh', 1), ('sub', 16070)], [('add', 2045)], [('lsh', 8), ('add', 37087), ('sub', 22013), ('lsh', 10), ('lsh', 2)], [('add', 31880), ('sub', 56557), ('lsh', 6), ('lsh', 5), ('lsh', 8), ('add', 15535)], [('add', 22937), ('add', 4060)], [('add', 8462), ('sub', 4463), ('sub', 45810), ('lsh', 1)], [('sub', 10144), ('lsh', 8), ('lsh', 5), ('lsh', 1), ('lsh', 8)], [('add', 49937), ('lsh', 2), ('add', 60982), ('sub', 24799)], [('lsh', 4), ('add', 53340), ('add', 50619), ('sub', 56111), ('add', 6134), ('lsh', 1)], [('sub', 22577), ('sub', 50645)], [('add', 21265), ('sub', 41440)], [('add', 63314), ('sub', 45755), ('add', 62216)], [('sub', 52616)], [('add', 21192)], [('add', 62573), ('sub',18811)], [('add', 35452), ('sub', 11573), ('sub', 49079), ('sub', 36361), ('sub', 26862), ('lsh', 9)], [('add', 13610), ('lsh', 7), ('lsh', 3), ('sub', 28490), ('lsh', 10), ('add', 44742)], [('lsh', 10), ('sub', 1797), ('sub', 10564), ('add', 12394)], [('add', 45165), ('lsh', 10), ('sub', 60610), ('sub', 63002), ('sub', 14851), ('lsh', 1)], [('add', 34840), ('lsh', 3), ('sub', 16907)], [('add', 4404), ('lsh', 3), ('lsh', 7), ('lsh', 6)], [('lsh', 6), ('add', 51738), ('sub', 24621), ('add', 58646)], [('lsh', 1)], [('add', 29375), ('sub', 419), ('add', 2854), ('sub', 11878), ('lsh', 10), ('add', 40151)], [('add', 22953)]]
targets = [4294946431, 4278905078, 1286912, 4294906624, 17060, 4294661164, 4294429720, 94573, 4294924666, 4294901787, 4294868383, 4294886344, 86147072, 47247259, 4294910851, 4294833676, 4294911813, 3040, 4294951460, 2160, 171843584, 4734127, 27100, 4294883864, 884998144, 236375, 111420, 4294894192, 4294947222, 79889, 4294914775, 21308, 43873, 4249743360, 1477674694, 113697, 92442178, 262757, 295239680, 91843, 210, 20569303, 23078]
flag_len = 43

# 起手式 - 開一個Solver
s = Solver()

# 建立符號 - 以此lab來說就是建立43個符號對應每一個flag字元
bvs = [BitVec(f'bt_{i}', 32) for i in range(flag_len)]

# 加上constraint - 以此lab來說每一個flag字元都應該限制在空白到0x7f之間
for bv in bvs:
    s.add(And(bv >= 0x20, bv <= 0x7f))


for i, patter in enumerate(patters):
    formula = f'bvs[{i}]'

    for step in patter:
        op = step[0]
        value = step[1]

        if op == 'add':
            formula = f'({formula} + {value})'
        elif op == 'sub':
            formula = f'({formula} - {value})'
        elif op == 'lsh':
            formula = f'({formula} << {value})'

    print(f'{formula} == {targets[i]}')
    s.add(eval(formula) == targets[i])

# 如果有解的話就會做以下操作
if s.check() == sat:
    print('Find ~~~')
    print(s.model())

    flag = ""
    for bv in bvs:
        flag += chr(s.model()[bv].as_long())

    print(flag)
```