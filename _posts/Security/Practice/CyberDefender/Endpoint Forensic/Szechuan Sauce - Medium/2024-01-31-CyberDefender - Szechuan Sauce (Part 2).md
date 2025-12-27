---
title: CyberDefender - Szechuan Sauce (Part 2)
tags: [CyberDefender, Endpoint Forensics]

category: "Security｜Practice｜CyberDefender｜Endpoint Forensic｜Szechuan Sauce - Medium"
---

# CyberDefender - Szechuan Sauce (Part 2)
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/31
Part 1: https://hackmd.io/@SBK6401/rkp952e76

:::spoiler TOC
[TOC]
:::

## Scenario
> An employee at a large company was assigned a task with a two-day deadline. Realizing that he could not complete the task in that timeframe, he sought help from someone else. After one day, he received a notification from that person who informed him that he had managed to finish the assignment and sent it to the employee as a test. However, the person also sent a message to the employee stating that if he wanted the completed assignment, he would have to pay $160.
>
> The helper's demand for payment revealed that he was actually a threat actor. The company's digital forensics team was called in to investigate and identify the attacker, determine the extent of the attack, and assess potential data breaches. The team must analyze the employee's computer and communication logs to prevent similar attacks in the future.

## Tools
* volatility2
* FTK
* Timeline Explorer
* Wireshark
* Registry Explorer

## ==Q11==
> What's the name of the attack tool you think this malware belongs to? (one word) 

### Recon
和malware相關的資訊，直覺會先看virustotal上的資訊，也的確發現答案的蹤跡

:::spoiler Flag
Flag: `Metasploit`
:::

## ==Q12==
> One of the involved malicious IP's is based in Thailand. What was the IP? 

### Recon
這個在virustotal上也有完整的資訊，只能說那個network graph真的太屌了，不只清楚也很炫泡
![圖片.png](https://hackmd.io/_uploads/BJw07aEX6.png)

:::spoiler Flag
Flag: `203.78.103.109`
:::

## ==Q13==
> Another malicious IP once resolved to klient-293.xyz . What is this IP? 

### Recon
我是直接在network packets裡面撈比較常見的IP，不過看[^szechuan-sauce-wp]才知道也可以直接用virustotal搜URL

### Exploit
* 方法一:
    我看最多次request的IP有點可疑
    ![圖片.png](https://hackmd.io/_uploads/H12W_a4mT.png)
* 方法二:
    ![圖片.png](https://hackmd.io/_uploads/HJ1xYpEQa.png)

所以根據上一題可知我們現在有兩個可疑的IP，一個是傳送payload的IP$\to$`194.61.24.102`，而另外一個是駭客的C2 server(在泰國的那個)$\to$`203.78.103.109`

:::spoiler Flag
Flag: `194.61.24.102`
:::

## ==Q14==
> The attacker performed some lateral movements and accessed another system in the environment via RDP. What is the hostname of that system? 

### Background
* [LLMNR](https://netpc.pixnet.net/blog/post/12409336)
    > LLMNR 是定義於標題為 "Link-local Multicast Name Resolution (LLMNR)" (連結-本機多點傳送名稱解析 (LLMNR)) (draft-ietf-dnsext-mdns-47.txt) 之網際網路草稿中的通訊協定，同時允許 IPv6 和 IPv4 主機為鄰接電腦執行名稱解析，而不需設定 DNS 伺服器或 DNS 用戶端。
    >
    > 也就是，這是在LAN才會出現的，例如:嘗試使用WakeOnLan的時候，故若你沒有提出此要求，而發現有此封包在攻擊你的電腦時，它肯定就是病毒啦!!
* [Logon Type](https://learn.microsoft.com/zh-tw/windows/security/threat-protection/auditing/event-4624)
    ![圖片.png](https://hackmd.io/_uploads/ByVq_0EXa.png)

### Recon
這一題找很久，不管是從wireshark或是從timeline explorer，參考[^szechuan-sauce-wp]才知道有比較正確的方式

### Exploit
首先，攻擊的方向變成橫向移動，這件事情從rdp的封包就看的出來(內網和內網)
![圖片.png](https://hackmd.io/_uploads/rkj7UCE7T.png)

WP中有提到兩種解析方式，一種是看network packets，另外一種是看event log
* 方法一
    可以直接用LLMNR的protocol當作filter
    ![圖片.png](https://hackmd.io/_uploads/r1SdBCVma.png)
* 方法二
    看了MSDN的logon type可以發現，如果是用RDP登入的話，要看type 10(RemoteInteractive)和3(使用者或電腦從網路登入這部電腦。)，所以橫向移動應該是logon type 3的範疇
    ![圖片.png](https://hackmd.io/_uploads/rJ9EK0EX6.png)
    
:::spoiler Flag
Flag: `DESKTOP-SDN1RPT`
:::

## ==Q15==
> Other than the administrator, which user has logged into the Desktop machine? (two words) 

### Recon
這一題直覺就是延續上一題的狀況，直接看timeline explorer有登入的target
![圖片.png](https://hackmd.io/_uploads/HyOgT0E76.png)

:::spoiler Flag
Flag: `rick sanchez`
:::

## ==Q16==
> What was the password for "jerrysmith" account? 

### Recon
原本的直覺是follow之前寫的[0x13 - Brute Force SAM](https://hackmd.io/@SBK6401/S1KgaEz0h)可以爆破密碼，但我似乎搞錯題目的意思，應該說要找`jerrysmith`的密碼，直覺要對domain controller下手，不過應該不是找SAM hive，因為這個只有存取單一主機的認證authentication，所以如果要找儲存其他AD的密碼資訊，算是一個新的觀念:

[What is NTDS.DIT?](https://medium.com/@harikrishnanp006/understanding-ntds-dit-the-core-of-active-directory-faac54cc628a)
> NTDS.DIT stands for New Technology Directory Services Directory Information Tree. It serves as the primary database file within Microsoft’s Active Directory Domain Services (AD DS). Essentially, NTDS.DIT stores and organizes all the information related to objects in the domain, including users, groups, computers, and more. It acts as the backbone of Active Directory, housing critical data such as user account details, passwords, group memberships, and other object attributes.

### Exploit
1. Export NTDS.DIT & SYSTEM
    NTDS.DIT在Domain Server的`C:\Windows\NTDS\ntds.dit`，而SYSTEM在`C:\Windows\System32\config\SAM`
2. 用Kali裡面的[`impacket-secretsdump`](https://www.kali.org/tools/impacket/)轉成hash
    :::spoiler Result
    ```bash
    $ impacket-secretsdump -system SYSTEM -ntds ntds.dit LOCAL -outputfile hashes.txt
    Impacket v0.11.0 - Copyright 2023 Fortra

    [*] Target system bootKey: 0xdfa37c24984935de32e2063e02918c28
    [*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
    [*] Searching for pekList, be patient
    [*] PEK # 0 found and decrypted: 6e884ac48cd2aa3a8d5f50c64d4bc38a
    [*] Reading and decrypting hashes from ntds.dit 
    Administrator:500:aad3b435b51404eeaad3b435b51404ee:10e63d3f2c9924bae49241cff847e405:::
    Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
    CITADEL-DC01$:1001:aad3b435b51404eeaad3b435b51404ee:33c082748b7d35ec846a513b7be92d94:::
    krbtgt:502:aad3b435b51404eeaad3b435b51404ee:25c9610b742a5bca9aa3801c08b8ca4e:::
    C137.local\jerrysmith:1104:aad3b435b51404eeaad3b435b51404ee:bc51f858ccacc9db408c0ba511d5d639:::
    C137.local\summersmith:1105:aad3b435b51404eeaad3b435b51404ee:26b2cc706093c4fa46e0519ec5feaeaf:::
    C137.local\ricksanchez:1106:aad3b435b51404eeaad3b435b51404ee:746447f27820a9d863eea94d176cc135:::
    C137.local\mortysmith:1108:aad3b435b51404eeaad3b435b51404ee:dc8b282b8f4e1dd3c5f95fd491ff6d8d:::
    C137.local\bethsmith:1109:aad3b435b51404eeaad3b435b51404ee:b9cc9177094af2e17b413a0cbf63fac2:::
    C137.local\birdman:1118:aad3b435b51404eeaad3b435b51404ee:944055b77ebe7d6fd80f24b5fce634fb:::
    DESKTOP-SDN1RPT$:1602:aad3b435b51404eeaad3b435b51404ee:fa6ecdc900cbeeb623cfc92297e5b653:::
    [*] Kerberos keys from ntds.dit 
    CITADEL-DC01$:aes256-cts-hmac-sha1-96:3635b6b22a960673e327ca4c378e162befa74ee56e46b3841b84cabecfc062e8
    CITADEL-DC01$:aes128-cts-hmac-sha1-96:9324dad1f82699bf65cdbfd5a4572067
    CITADEL-DC01$:des-cbc-md5:94abfd29f1929d19
    krbtgt:aes256-cts-hmac-sha1-96:141aca9186cc33caa6ef3db5cf3a53b783bd29e7431a153c89f8b1d4562de7f1
    krbtgt:aes128-cts-hmac-sha1-96:d695009f7f7b6eb48a6b1b749493f199
    krbtgt:des-cbc-md5:b025018c62ec023b
    C137.local\jerrysmith:aes256-cts-hmac-sha1-96:87eb9c5715de1eb078cc6691871672019356976f093348c03b0ca21a75fc0e9f
    C137.local\jerrysmith:aes128-cts-hmac-sha1-96:ea468a0f250c15fea4e8f4c74d20c56e
    C137.local\jerrysmith:des-cbc-md5:7c40d03464e5e9a8
    C137.local\summersmith:aes256-cts-hmac-sha1-96:38060a9e953e8dde6e991db5de72e566c8a652c195b0e88d9c81e26d05ee1ce5
    C137.local\summersmith:aes128-cts-hmac-sha1-96:8851e24f50c80026e2e1578a2a3d3802
    C137.local\summersmith:des-cbc-md5:3bd09e3b73bfb0f4
    C137.local\ricksanchez:aes256-cts-hmac-sha1-96:08bc14d8f69e1ceadd0079303cd1bc434ed61d6a4895f71073662ff24eb8e4dd
    C137.local\ricksanchez:aes128-cts-hmac-sha1-96:0c428543d20db44c45cbf6948b4cf5d4
    C137.local\ricksanchez:des-cbc-md5:cdf891a75889f107
    C137.local\mortysmith:aes256-cts-hmac-sha1-96:ee5442baa6535d2580ac694ac6c0cbe3a65f137ba3ace39a18cba58a160ce73c
    C137.local\mortysmith:aes128-cts-hmac-sha1-96:697ece25fd3cffbfa24d82ab9789596c
    C137.local\mortysmith:des-cbc-md5:3280f79b131aea4c
    C137.local\bethsmith:aes256-cts-hmac-sha1-96:1e98c29b4ba43d21d200bd1802ff5109c0549621931e2f3af0c0809099405b88
    C137.local\bethsmith:aes128-cts-hmac-sha1-96:ea3285637fe5bb216bcd5cd0cfbc6663
    C137.local\bethsmith:des-cbc-md5:151f891ff4cb6b4f
    C137.local\birdman:aes256-cts-hmac-sha1-96:f20039a71fad3a9a0a374c09e55f1d1bed1600c2329fee84aada8a502d903023
    C137.local\birdman:aes128-cts-hmac-sha1-96:6507f6ac1b4ec9c23e65d1528ec92ec1
    C137.local\birdman:des-cbc-md5:2f4068527aeafb85
    DESKTOP-SDN1RPT$:aes256-cts-hmac-sha1-96:424f9a36c72c7bec7a2f7082111ed818c375e8945e6cfc9bc599b6587fb1b3ea
    DESKTOP-SDN1RPT$:aes128-cts-hmac-sha1-96:14122a1520d70f1dc6fccbf8aee330b0
    DESKTOP-SDN1RPT$:des-cbc-md5:6d20ad583729b03e
    [*] Cleaning up...
    $ cat hashes.txt.ntds
    Administrator:500:aad3b435b51404eeaad3b435b51404ee:10e63d3f2c9924bae49241cff847e405:::
    Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
    CITADEL-DC01$:1001:aad3b435b51404eeaad3b435b51404ee:33c082748b7d35ec846a513b7be92d94:::
    krbtgt:502:aad3b435b51404eeaad3b435b51404ee:25c9610b742a5bca9aa3801c08b8ca4e:::
    C137.local\jerrysmith:1104:aad3b435b51404eeaad3b435b51404ee:bc51f858ccacc9db408c0ba511d5d639:::
    C137.local\summersmith:1105:aad3b435b51404eeaad3b435b51404ee:26b2cc706093c4fa46e0519ec5feaeaf:::
    C137.local\ricksanchez:1106:aad3b435b51404eeaad3b435b51404ee:746447f27820a9d863eea94d176cc135:::
    C137.local\mortysmith:1108:aad3b435b51404eeaad3b435b51404ee:dc8b282b8f4e1dd3c5f95fd491ff6d8d:::
    C137.local\bethsmith:1109:aad3b435b51404eeaad3b435b51404ee:b9cc9177094af2e17b413a0cbf63fac2:::
    C137.local\birdman:1118:aad3b435b51404eeaad3b435b51404ee:944055b77ebe7d6fd80f24b5fce634fb:::
    DESKTOP-SDN1RPT$:1602:aad3b435b51404eeaad3b435b51404ee:fa6ecdc900cbeeb623cfc92297e5b653:::
    ```
    :::
3. Brute Force
    * [Online Tool 1](https://www.cmd5.com/)
    * [Online Tool 2](https://hashes.com/en/decrypt/hash)
    * john:
        `$ john hashes.txt.ntds --format=NT`

    我是直接用第二個線上工具解出一半的密碼，如下:
    ```
    10e63d3f2c9924bae49241cff847e405:)&Denver89
    31d6cfe0d16ae931b73c59d7e0c089c0:
    33c082748b7d35ec846a513b7be92d94: (None)
    25c9610b742a5bca9aa3801c08b8ca4e: (None)
    bc51f858ccacc9db408c0ba511d5d639: !BETHEYBOO12!
    26b2cc706093c4fa46e0519ec5feaeaf: (None)
    746447f27820a9d863eea94d176cc135: (None)
    dc8b282b8f4e1dd3c5f95fd491ff6d8d: Jessica@1
    b9cc9177094af2e17b413a0cbf63fac2: RedWine1!
    944055b77ebe7d6fd80f24b5fce634fb: (dimension5150)
    fa6ecdc900cbeeb623cfc92297e5b653: (None)
    ```

:::spoiler Flag
Flag: `!BETHEYBOO12!`
:::

## ==Q17==
> What was the original filename for Beth’s secrets? 

### Recon
直覺會用volatility看filescan的結果，不過沒有甚麼收穫，看了答案的hint才知道要去撈recycle bin的東西(誰知道啊)

### Exploit
![圖片.png](https://hackmd.io/_uploads/rysZqVH76.png)

:::spoiler Flag
Flag: `SECRET_beth.txt`
:::

## ==Q18==
> What was the content of Beth’s secret file? ( six words, spaces in between) 

### Recon
直接呈上題，下一個檔案就是他的file content

:::spoiler Flag
Flag: `Earth beth is the real beth`
:::

## ==Q19==
> The malware tried to obtain persistence in a similar way to how Carbanak malware obtains persistence. What is the corresponding MITRE technique ID? 

### Exploit
直接看Carbanak的MITRE頁面，詳細的訊息可以看[這邊](https://attack.mitre.org/groups/G0008/)

:::spoiler Flag
Flag: `T1543.003`
:::

## Reference
[^szechuan-sauce-wp]:[CyberDefenders: Szechuan Sauce CTF Writeup](https://ellisstannard.medium.com/cyberdefenders-szechuan-sauce-writeup-ab172eb7666c)