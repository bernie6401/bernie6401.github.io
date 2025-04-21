---
title: CyberDefender - CorporateSecrets (Part 2)
tags: [CyberDefender, Endpoint Forensics]

category: "Security/Practice/CyberDefender/Endpoint Forensic/CorporateSecrets - Medium"
---

# CyberDefender - CorporateSecrets (Part 2)
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/33
Part 1: https://hackmd.io/@SBK6401/r18z7VIm6
Part 3: https://hackmd.io/@SBK6401/HyHp4NLQT
Part 4: https://hackmd.io/@SBK6401/H1rAEV87p

:::spoiler TOC
[TOC]
:::

## Tools: 
* FTK Imager
* Registry Explorer
* RegRipper
* HxD
* DB Browser for SQLite
* HindSight
* Event Log Explorer
* MFTDump


## ==Q10==
> What is the SID of the machine?

### Exploit
直接看`SOFTWARE/Microsoft/Windows NT/CurrentVersion/ProfileList`就知道了
![圖片.png](https://hackmd.io/_uploads/ry8fOuU7T.png)

:::spoiler Flag
Flag: `S-1-5-21-2446097003-76624807-2828106174`
:::

## ==Q11==
> How many web browsers are present? 

### Recon
直接搜索一下所有user的AppData或是program1，可以發現有五個瀏覽器(Firefox / Internet Explorer / Chrome / Edge / Tor)
![圖片.png](https://hackmd.io/_uploads/HkKLxF8Xp.png)

:::spoiler Flag
Flag: `5`
:::

## ==Q12==
> How many super secret CEO plans does Tim have?
(Dr. Doofenshmirtz Type Beat) 

### Recon
這一題有一點像[Enlightened 2023 - Jack的flag](https://hackmd.io/@SBK6401/H1w0vImC2)

### Exploit
1. 先從tim的document中看有沒有甚麼特別的file
2. 發現secret.odt其中的內容，最後一個部分被隱藏起來了，要複製到其他editor才會發現
    ![圖片.png](https://hackmd.io/_uploads/Sk9UStL7T.png)
    ```
    Super secret CEO plans:
    •	Take over the world
    •	Destroy Google
    •	Release the new Fruit Phone
    •	Fire Jim Tomato
    ```

:::spoiler Flag
Flag: `4`
:::

## ==Q13==
> Which employee does Tim plan to fire?
(He's Dead, Tim. Enter the full name - two words - space separated) 

### Recon
呈上題

:::spoiler Flag
Flag: `Jim Tomato`
:::

## ==Q14==
> What was the last used username?
(I didn't start this conversation, but I'm ending it!) 

### Recon
我覺得這一題出的不好，應該說題目出到有點看不懂，也可能是我的英文很爛，但反正他要探討的是最後一個使用電腦的帳號為何，所以直覺就是export Security.evtx，然後轉成CSV檔案，接著用timeline explorer找最後一個成功登入者

### Exploit
* 方法一
    ![圖片.png](https://hackmd.io/_uploads/rkrIjYLmp.png)
* 方法二
    在`SOFTWARE/Microsoft/Windows NT/CurrentVersion/Winlogon`可以找到
    ![圖片.png](https://hackmd.io/_uploads/SkEDG5Lm6.png)

:::spoiler Flag
Flag: `jim.tomato`
:::

## ==Q15==
> What was the role of the employee Tim was flirting with? 

### Recon
這一題完全沒有想法，所以解題過程參考[^wp]

### Exploit
主要是export出他在browser上的history database file，並看他的瀏覽紀錄
![圖片.png](https://hackmd.io/_uploads/HkLXgvvX6.png)

:::spoiler Flag
Flag: `secretary`
:::

## ==Q16==
> What is the SID of the user "suzy.strawberry"?

### Exploit
同第十題，`suzy.strawberry`的SID是`S-1-5-21-2446097003-76624807-2828106174-1004`

:::spoiler Flag
Flag: `1004`
:::

## ==Q17==
> List the file path for the install location of the Tor Browser.

### Exploit
呈第11題

:::spoiler Flag
Flag: `C:\Program1`
:::

## ==Q18==
> What was the URL for the Youtube video watched by Jim? 

### Recon
這個是有點新的舊觀念，先看Jim的瀏覽器是用哪一個$\to$Chrome，所以可以查一下Chrome的樓覽紀錄在哪邊$\to$`root/Users/jim.tomato/AppData/Local/Google/Chrome/UserData/Default/`中可以找到History這個database file，接著就是用db browser parse這個file

### Exploit
![圖片.png](https://hackmd.io/_uploads/SkN2-IPQp.png)

:::spoiler Flag
Flag: `https://www.youtube.com/watch?v=Y-CsIqTFEyY`
:::

## Reference
[^wp]:[CyberDefenders: CorporateSecrets](https://forensicskween.com/ctf/cyberdefenders/corporatesecrets/)