---
title: CyberDefender - PoisonedCredentials
tags: [CyberDefender, Network Forensics]

---

# CyberDefender - PoisonedCredentials
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/146#nav-questions

:::spoiler TOC
[TOC]
:::

## Scenario
> Your organization's security team has detected a surge in suspicious network activity. There are concerns that LLMNR (Link-Local Multicast Name Resolution) and NBT-NS (NetBIOS Name Service) poisoning attacks may be occurring within your network. These attacks are known for exploiting these protocols to intercept network traffic and potentially compromise user credentials. Your task is to investigate the network logs and examine captured network traffic.

## Background
* [ NetBIOS and LLMNR Poisoning | Attack Demonstration ](https://youtu.be/s2YIU2w9T9Q?si=ZCj8xuSR6Jp_7WTW)
* [本機多點傳送名稱解析 (LLMNR)](https://netpc.pixnet.net/blog/post/12409336)
    > 同時允許 IPv6 和 IPv4 主機為鄰接電腦執行名稱解析，而不需設定 DNS 伺服器或 DNS 用戶端。
    >
    >也就是，這是在LAN才會出現的，例如:嘗試使用WakeOnLan的時候，故若你沒有提出此要求，而發現有此封包在攻擊你的電腦時，它肯定就是病毒啦!!
* [NetBIOS & NBNS](https://www.jendow.com.tw/wiki/NBNS)
    > ### 功能
    > 不管使用哪一種傳輸方式，NetBIOS提供三種不同的服務：
    > 1. 名字服務：名字登記和解析
    > 2. 會話服務：可靠的基於連線的通信
    > 3. 數據包服務：不可靠的無連線通信
    > 
    > 當NetBIOS是數據鏈路層協定時，可以通過5Ch中斷訪問其功能。傳遞給這些函式的訊息使用NCB格式。
    > NetBIOS和NetBEUI被設計為僅僅用於區域網路，因此不支持路由，並且最多只能處理72個節點或者設備。NetBIOS和NetBEUI經常使用廣播實現，尤其是名字服務的相關操作。
## ==Q1==
> In the context of the incident described in the scenario, the attacker initiated their actions by taking advantage of benign network traffic from legitimate machines. Can you identify the specific mistyped query made by the machine with the IP address 192.168.232.162? 
### Recon
從scenario和題目敘述可以知道幾件事情
1. 部門遭受LLMNT和NBT-NS poisoning attack，所以重點應該著重在llmnr / nbns這兩個protocol上
2. Victim應該是192.168.232.162
### Exploit
Filter Payload: `nbns and ip.addr == 192.168.232.162`
![image](https://hackmd.io/_uploads/H1APnx4Ip.png)

:::spoiler Flag
Flag: `fileshaare`
:::
## ==Q2==
> We are investigating a network security incident. For a thorough investigation, we need to determine the IP address of the rogue machine. What is the IP address of the machine acting as the rogue entity? 
### Recon
從前一題可以知道，192.168.232.162是一個victim，所以我們的目標應該是去看誰和他溝通，不管是傳送payload / 檔案等等，就可以確定攻擊的人是誰
### Exploit
可以直接看wireshark的conversation，就知道唯一和他連線溝通的，只有==192.168.232.215==
![image](https://hackmd.io/_uploads/rywJRbN8T.png)

:::spoiler Flag
Flag: `192.168.232.215`
:::

## ==Q3==
> During our investigation, it's crucial to identify all affected machines. What is the IP address of the second machine that received poisoned responses from the rogue machine?
### Exploit
和上一題相關，如果是想要直接看誰和attacker連線就直接看conversation最快

:::spoiler Flag
Flag: `192.168.232.176`
:::
## ==Q4==
> We suspect that user accounts may have been compromised. To assess this, we must determine the username associated with the compromised account. What is the username of the account that the attacker compromised? 
### Recon
從題目可以知道，受害者是前一題的==192.168.232.176==，而attacker是==192.168.232.215==，另外兩者溝通的管道通常是smb
### Exploit
Filter Payload: `smb2 and ip.src==192.168.232.215 and ip.dst==192.168.232.176`
![image](https://hackmd.io/_uploads/S17LNzEI6.png)

:::spoiler Flag
Flag: `janesmith`
:::
## ==Q5==
> As part of our investigation, we aim to understand the extent of the attacker's activities. What is the hostname of the machine that the attacker accessed via SMB? 
### Exploit
這一題是看[^wp]的說明，有一個ntlm challenge的error，進去看會發現NetBIOS Computer 
Filter Payload: `(ip.addr == 192.168.232.162 or ip.addr == 192.168.232.176 or ip.addr == 192.168.232.215) and (smb2)`
![image](https://hackmd.io/_uploads/SJUFGQV8p.png)

:::spoiler Flag
Flag: `accountingpc`
:::
## Reference
[^wp]:[PoisonedCredentials-CyberDefenders](https://medium.com/@anas.hey/poisonedcredentials-cyberdefenders-7b62dfeb1205)