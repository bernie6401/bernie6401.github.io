---
title: BTLO - Bruteforce
tags: [BTLO, Incident Response]

category: "Security/Practice/BTLO/Incident Response"
---

# BTLO - Bruteforce
Challenge: https://blueteamlabs.online/home/challenge/bruteforce-16629bf9a2

:::spoiler TOC
[TOC]
:::

## Scenario
> Can you analyze logs from an attempted RDP bruteforce attack?
>
>One of our system administrators identified a large number of Audit Failure events in the Windows Security Event log.
>
>There are a number of different ways to approach the analysis of these logs! Consider the suggested tools, but there are many others out there! 

## ==Q1==
> How many Audit Failure events are there? (Format: Count of Events)

### Recon
直接用timeline explorer下4625的條件

### Exploit
![圖片](https://hackmd.io/_uploads/HJGemkJdp.png)

:::spoiler Flag
Flag: `3103`
:::

## ==Q2==
> What is the username of the local account that is being targeted? (Format: Username)

### Recon
直接看`./BTLO_Bruteforce_Challenge.txt`的Account Name，總共有
* administartor
* BTLO
* EC2AMAZ-UUEMPAU$
* SYSTEM

:::spoiler Flag
Flag: `administrator`
:::

## ==Q3==
> What is the failure reason related to the Audit Failure logs? (Format: String)

### Recon
直接看`./BTLO_Bruteforce_Challenge.txt`的Failure Reason
`Failure Reason:		Unknown user name or bad password.`

:::spoiler Flag
Flag: `Unknown user name or bad password.`
:::

## ==Q4==
> What is the Windows Event ID associated with these logon failures? (Format: ID)

### Recon
以為是陷阱題，但還是4625

:::spoiler Flag
Flag: `4625`
:::

## ==Q5==
> What is the source IP conducting this attack? (Format: X.X.X.X)

### Recon
直接看`./BTLO_Bruteforce_Challenge.txt`的Source Network Address
`Source Network Address:	113.161.192.227`

:::spoiler Flag
Flag: `113.161.192.227`
:::

## ==Q6=
> What country is this IP address associated with? (Format: Country)

### Recon
直接看該IP的訊息，用whois來看相關內容，詳細query result可以看[這邊](https://www.whois.com/whois/113.161.192.227)
![圖片](https://hackmd.io/_uploads/SkpdSJy_a.png)

:::spoiler Flag
Flag: `Vietnam`
:::

## ==Q7==
> What is the range of source ports that were used by the attacker to make these login requests? (LowestPort-HighestPort - Ex: 100-541)

### Recon
寫個簡單的script
```bash!
$ cat BTLO_Bruteforce_Challenge.txt | grep "Source Port:" > Extracted_port.txt
```

```python!
f = open('./Extracted_port.txt', 'r').read().replace('	Source Port:		', '').replace('-\n', '').split('\n')[:-1]

# for i in range(len(f)):
#     print(f[i])
print(f'Min: {min(f)}, Max: {max(f)}')
```

:::spoiler Flag
Flag: `49162-65534`
:::

## Reference
[^wp1]:[Blue Teams Labs Online | Bruteforce](https://medium.com/@ERBATMAN/blue-teams-labs-online-bruteforce-49cc3e774fdd)