---
title: Cryptography Lec 5(Symmetric Key Cryptography) - Notes
tags: [Cryptography, NTU]

category: "Security > Course > NTU Crypto"
---

# Cryptography Lec 5(Symmetric Key Cryptography) - Notes
###### tags: `Cryptography` `NTU`

## Background
[What is MDC and MAC? - 【CN007】数据安全笔记8 —— MDC 和 MAC](https://blog.csdn.net/qq_42950838/article/details/117536583#Modification_Detection_Code_MDC_9)
> MDC 是一種用於驗證數據完整性的摘要信息，保證數據沒有被更改。
> ![](https://img-blog.csdnimg.cn/20210603231335485.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyOTUwODM4,size_16,color_FFFFFF,t_70)
> ---
> MAC 在 MDC 的基礎上增加了 Key 的使用。同時驗證數據完整性和發送者，保證發送者是特定人並且傳輸過程中數據沒有被更改。MAC 函數又稱為 Key 哈希函數（Keyed Hash Function）
> ![](https://img-blog.csdnimg.cn/20210603225822420.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyOTUwODM4,size_16,color_FFFFFF,t_70)

:::spoiler [About RC4](https://ithelp.ithome.com.tw/articles/10263124)
* 第一部分 前置作業
    1. 建立一個 S-box（寫作 S）
    2. 決定密鑰
    3. 建立密鑰列表 K

* 第二部分 把 S 打亂
* 第三部分 加密
```python
S = [0,1,2,3,4,5,6,7]
K = [1,2,3,1,2,3,1,2]
P = [5,3,6,7]

j = 0 
for i in range(8):
    j = ( j + S[i] + K[i] ) %8
    S[i], S[j] = S[j], S[i]

i, j = 0, 0
flag = 0
c_list = []
while flag < len(P):
    
    i = (i + 1) % 8
    j = (j +S[i]) % 8
    S[i], S[j] = S[j], S[i]
    t = (S[i] + S[j] ) % 8
    k = S[t]
    
    k = '{:03b}'.format(k)
    p = '{:03b}'.format(P[flag])
    c  = ''
    for n in range(3):
        c += str(int(k[n])^int(p[n]))
    c_list.append(int(c, 2))
    flag += 1
    
print(c_list)
```

* Drawback
> RC4在後來被指出他所產生的密鑰並不隨機，存在統計上的偏誤，並且密文有洩漏明文資訊的可能，
因此已不再被建議使用。
:::

---
[About Feistel Cipher](https://youtu.be/dXuN-2CIdIY)
![](https://i.imgur.com/eHGhsBG.png)

---
[About DES](https://youtu.be/WnsgWK0DOOM)
![](https://i.imgur.com/NbaLsJb.png)

---
[What is OFB and CFB?](https://ithelp.ithome.com.tw/articles/10249953)
> ## CFB：密文反饋模式
>與CBC模式類似，但不同的地方在於，CFB模式先生成密碼流字典，然後用密碼字典與明文進行異或操作並最終生成密文。後一分組的密碼字典的生成需要前一分組的密文參與運算。
>CFB模式是用分組演算法實現流演算法，明文資料不需要按分組大小對齊。
>
>![](https://i.imgur.com/WyhjpXN.png)
>---
>## OFB：輸出反饋模式
>OFB模式與CFB模式不同的地方是：生成字典的時候會採用明文參與運算，CFB採用的是密文。
>
>![](https://i.imgur.com/X0K16vA.png)