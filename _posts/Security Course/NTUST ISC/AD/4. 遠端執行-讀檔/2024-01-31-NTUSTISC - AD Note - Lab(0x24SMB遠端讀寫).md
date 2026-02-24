---
title: NTUSTISC - AD Note - Lab(SMB遠端讀寫)
tags: [NTUSTISC, AD, information security]

category: "Security Course｜NTUST ISC｜AD｜4. 遠端執行-讀檔"
date: 2024-01-31
---

# NTUSTISC - AD Note - Lab(SMB遠端讀寫)
<!-- more -->
[TOC]

Lecture Video: [ 2022/05/11 AD 安全 2 ](https://youtu.be/ubNMQ7_dcm0?si=26g2Lz2CB-O-7S5d)

## Lab
這個lab主要和之前不太一樣的地方在於都是利用SMB的功能達到遠端電腦讀寫的效果，雖然遠端執行也可以做到，但這樣會比較方便

### ==遠端讀寫(w/ GUI)==
1. Open File Explorer
2. Enter `\\<IP>\c$`
For example: `\\192.168.222.128\c$`
3. Login Local Admin
![](https://hackmd.io/_uploads/S1uCNUBlp.png)

* Result
    我在Win10中利用上述步驟，成功讀取到Win2016的資料
    ![](https://hackmd.io/_uploads/HJbEr8Bxa.png)

### ==遠端讀寫(w/o GUI)==
沒有GUI的情況就需要先掛載遠端的C槽在本地端，然後才可以進行後續的讀寫，有時候他會跳出錯誤
* Cheat Sheet
    ```bash
    $ net use \\<IP>\C$ "<password>" /user:<username>
    ```
    :::spoiler Result
    ```bash
    $ net use \\192.168.222.128\C$ "1qaz@WSX3edc" /user:administrator # 掛載遠端磁碟
    命令已經成功完成。
    $ net use # 查看已掛載的遠端磁碟
    會記錄新的網路連線。


    狀態       本機        遠端                    網路

    -------------------------------------------------------------------------------
    OK                     \\192.168.222.128\C$      Microsoft Windows Network
    命令已經成功完成。
    $ copy Rubeus.exe \\192.168.222.128\C$
    複製了         1 個檔案。
    ```
    ![](https://hackmd.io/_uploads/BykOL8rgT.png)
    可以看到Win2016的C槽中多了一個Rubeus.exe的檔案，代表成功
    :::

### ==How to Detect SMB Access==
Event ID: 5145
預設不開，因為會有大量的event湧入，除非設定有存取c$的filter，就會少非常多，因為遠端存取c槽本身就蠻可疑的，所以偵測到非法存取的機率就蠻高的

## ==組合技==
1. 利用SMB開進去遠端檔案總管，然後把procdump.exe送過去(忘記procdump.exe可以複習一下[NTUSTISC - AD Note - Lab(其他方法得到lsass.dmp)](https://hackmd.io/@SBK6401/S16T17NCn))
2. 使用psexec.exe遠端執行procdump.exe就可以取得lsass的memory dump
3. 再利用SMB把dump result取回本機
4. 在本地端使用mimikatz以便取得更多密碼