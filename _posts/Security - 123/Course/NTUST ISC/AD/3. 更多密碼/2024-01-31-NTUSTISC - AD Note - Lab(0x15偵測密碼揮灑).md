---
title: NTUSTISC - AD Note - Lab(偵測密碼揮灑)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/3. 更多密碼"
---

# NTUSTISC - AD Note - Lab(偵測密碼揮灑)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=l1na5hFGpAPk6Uux&t=4257)

## Background
得到更高權限之後，會想要更多的密碼
* 密碼收集
    * SAM.hive(Security Account Manager)
    * Password Spraying(用猜的)
        * 和brute force差在哪裡呢?其實概念一樣，只是角度不一樣，brute force是針對一隻帳號，用很多的密碼去猜；而password spraying則是用一組密碼去爆所有的帳號，其實就是反過來
        * Tool: [CrackMapExec](https://github.com/Porchetta-Industries/CrackMapExec) - 結合各種功能的內網滲透神器
    * GPO
    * 記憶體(lsass)

## Lab

### ==Lab: How to detect Password Spraying==
利用Event ID: 4625, 4648, 4771的認證失敗紀錄
![](https://hackmd.io/_uploads/ryxGszmR2.png)
可以看到我是大約在4:52:08左右執行的，有一大堆的4625紀錄，如果抓最後一筆的紀錄，會顯示Account Name就是我們在Kali看到的最後一個帳戶，而且Keyword顯示Audit Failure
![](https://hackmd.io/_uploads/SJ0wszXA2.png)
 