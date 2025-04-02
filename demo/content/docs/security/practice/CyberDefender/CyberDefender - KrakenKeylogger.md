---
title: CyberDefender - KrakenKeylogger
tags: [CyberDefender, Endpoint Forensics]

---

# CyberDefender - KrakenKeylogger
:::spoiler TOC
[TOC]
:::

## Scenario
> An employee at a large company was assigned a task with a two-day deadline. Realizing that he could not complete the task in that timeframe, he sought help from someone else. After one day, he received a notification from that person who informed him that he had managed to finish the assignment and sent it to the employee as a test. However, the person also sent a message to the employee stating that if he wanted the completed assignment, he would have to pay $160.

The helper's demand for payment revealed that he was actually a threat actor. The company's digital forensics team was called in to investigate and identify the attacker, determine the extent of the attack, and assess potential data breaches. The team must analyze the employee's computer and communication logs to prevent similar attacks in the future.

## Tools
* DB Browser
* LECmd
* Timeline Explorer

## ==Q1==
> What is the the web messaging app the employee used to talk to the attacker? 
### Recon
這一題看了超久，主要是東西都刪的很乾淨，包含Program Files / Users Download / AppData甚至是機碼的Start up Application都沒有相關的足跡，俗話說沒想法就看log，所以我就去看chrome的瀏覽紀錄，最後就找到了
### Exploit
Google Chrome的artifact在`.challenge\Users\OMEN\AppData\Local\Google\Chrome\User Data\Default\`的History
![圖片](https://hackmd.io/_uploads/rkP8Xi5ma.png)

Flag: `telegram`
## ==Q2==
> What is the password for the protected ZIP file sent by the attacker to the employee? 
### Recon

### Exploit

## ==Q3==
> What domain did the attacker use to download the second stage of the malware? 
### Recon

### Exploit

## ==Q4==
> What is the name of the command that the attacker injected using one of the installed LOLAPPS on the machine to achieve persistence? 
### Recon

### Exploit

## ==Q5==
> What is the complete path of the malicious file that the attacker used to achieve persistence? 
### Recon

### Exploit

## ==Q6==
> What is the name of the application the attacker utilized for data exfiltration? 
### Recon

### Exploit

## ==Q7==
> What is the IP address of the attacker? 
### Recon

### Exploit


## Reference