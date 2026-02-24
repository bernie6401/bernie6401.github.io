---
title: CyberDefender - WebStrike
tags: [CyberDefender, Network Forensics]

category: "Security Practice｜CyberDefender｜Network Forensic"
date: 2024-01-31
---

# CyberDefender - WebStrike
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/149

:::spoiler TOC
[TOC]
:::

## Scenario
> An anomaly was discovered within our company's intranet as our Development team found an unusual file on one of our web servers. Suspecting potential malicious activity, the network team has prepared a pcap file with critical network traffic for analysis for the security team, and you have been tasked with analyzing the pcap.

## ==Q1==
> Understanding the geographical origin of the attack aids in geo-blocking measures and threat intelligence analysis. What city did the attack originate from? 

### Recon
這一題直覺想法是利用whois的線上工具直接看註冊的ip，有甚麼樣的info，除了地點還有使用人的email之類的

### Exploit
[Detailed Info](https://www.whois.com/whois/117.11.88.124)
![image](https://hackmd.io/_uploads/rkeoSKKUp.png)

:::spoiler Flag
Flag: `Tianjin`
:::

## ==Q2==
> Knowing the attacker's user-agent assists in creating robust filtering rules. What's the attacker's user agent? 

### Recon
直接看封包就有了

### Exploit
直接string search就好了，這一題很貼心，它是直接擷取開頭就是attacker和victim之間的conversation，沒有其他額外的protocol，所以比較好找
![image](https://hackmd.io/_uploads/SJnUdFKUT.png)

:::spoiler Flag
Flag: `Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0`
:::

## ==Q3==
> We need to identify if there were potential vulnerabilities exploited. What's the name of the malicious web shell uploaded? 

### Recon
直覺就是extract中間所有傳輸的檔案，再看他傳送檔案的packet內容寫的是甚麼

### Exploit
從下圖可以清楚的看到，他上傳檔案名稱是==image.jpg.php==
![image](https://hackmd.io/_uploads/rJClFYYIp.png)

:::spoiler Flag
Flag: `image.jpg.php`
:::

## ==Q4==
> Knowing the directory where files uploaded are stored is important for reinforcing defenses against unauthorized access. Which directory is used by the website to store the uploaded files? 

### Recon
可以翻看dump下來的那一些files，會發現它不只把傳送到victim的payload擷取下來，也擷取到victim回傳回來的結果

### Exploit
從payload和response可以知道存放upload files的path
![image](https://hackmd.io/_uploads/ByGqYYFI6.png)

:::spoiler Flag
Flag: `/reviews/uploads/`
:::

## ==Q5==
> Identifying the port utilized by the web shell helps improve firewall configurations for blocking unauthorized outbound traffic. What port was used by the malicious web shell? 

### Recon
我是直接follow tcp的flow，跟到它實際傳送payload的地方就知道Port Number是8080

### Exploit
![image](https://hackmd.io/_uploads/B1dovKKLp.png)

:::spoiler Flag
Flag: `8080`
:::

## ==Q6==
> Understanding the value of compromised data assists in prioritizing incident response actions. What file was the attacker trying to exfiltrate? 

### Recon
呈上上題

### Exploit

:::spoiler Flag
Flag: `passwd`
:::