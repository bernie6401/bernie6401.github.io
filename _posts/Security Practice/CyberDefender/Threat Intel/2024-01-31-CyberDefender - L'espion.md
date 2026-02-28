---
title: CyberDefender - L'espion
tags: [CyberDefender, Threat Intel]

category: "Security Practice｜CyberDefender｜Threat Intel"
date: 2024-01-31
---

# CyberDefender - L'espion
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/73

:::spoiler TOC
[TOC]
:::

## Scenario
> You, as a soc analyst, have been tasked by a client whose network was compromised and brought offline to investigate the incident and determine the attacker's identity.
>
> Incident responders and digital forensic investigators are currently on the scene and have conducted a preliminary investigation. Their findings show that the attack originated from a single user account, probably, an insider.
>
> Investigate the incident, find the insider, and uncover the attack actions.

## Tools
* Google Maps
* Google Image search
* [sherlock](https://github.com/sherlock-project/sherlock)


## ==Q1==
> File -> Github.txt:
What is the API key the insider added to his GitHub repositories? 

### Recon
直接在github key word search，就找到了
![圖片.png](https://hackmd.io/_uploads/H11t-rrmp.png)

:::spoiler Flag
Flag: `aJFRaLHjMXvYZgLPwiJkroYLGRkNBW`
:::

## ==Q2==
> File -> Github.txt:
What is the plaintext password the insider added to his GitHub repositories? 

### Exploit
還是和上一題一樣慢慢找，終於找到一個base64的密碼
![圖片.png](https://hackmd.io/_uploads/H1MVJIr7a.png)

```python
>>> b64decode(b'UGljYXNzb0JhZ3VldHRlOTk=')
b'PicassoBaguette99'
```

:::spoiler Flag
Flag: `PicassoBaguette99`
:::

## ==Q3==
> File -> Github.txt:
What is the plaintext password the insider added to his GitHub repositories? 

### Recon
像第一題一樣直接key word search
![圖片.png](https://hackmd.io/_uploads/HkJVZHH76.png)

:::spoiler Flag
Flag: `xmrig`
:::

## ==Q4==
> What university did the insider go to? 

### Recon
看了第一個hint，發現可以用linkedin找大學

:::spoiler Flag
Flag: `Sorbonne`
:::

## ==Q5==
> What gaming website the insider had an account on? 

### Exploit
這一題是通靈，答案是steam，但是其實在此刻(2023/11/06)，這個帳號已經消失了，所以就算用[sherlock](https://github.com/sherlock-project/sherlock)，都會找不到
```bash
$ conda create --name sherlock python=3.10 -y
$ pip install -r requirements.txt
$ python sherlock/sherlock.py EMarseille99
[*] Checking username EMarseille99 on:

[+] CNET: https://www.cnet.com/profiles/EMarseille99/
[+] Dealabs: https://www.dealabs.com/profile/EMarseille99
[+] G2G: https://www.g2g.com/EMarseille99
[+] GitHub: https://www.github.com/EMarseille99
[+] Lolchess: https://lolchess.gg/profile/na/EMarseille99
[+] Twitter: https://twitter.com/EMarseille99
[+] Virgool: https://virgool.io/@EMarseille99
[+] Whonix Forum: https://forums.whonix.org/u/EMarseille99/summary
[+] metacritic: https://www.metacritic.com/user/EMarseille99

[*] Search completed with 9 results
```

:::spoiler Flag
Flag: `steam`
:::

## ==Q6==
> What is the link to the insider Instagram profile? 

### Recon
直接google search: `Émilie Marseille`

:::spoiler Flag
Flag: `https://www.instagram.com/emarseille99/`
:::

## ==Q7==
> Where did the insider go on the holiday? (Country only) 

### Recon
直接看[IG的貼文](https://www.instagram.com/p/CAjDd_dlHds/?hl=en)，可以用image search搜尋圖片，發現這就是新加坡濱海灣金沙飯店
![未命名.jpg](https://hackmd.io/_uploads/H1KnoBB7p.jpg)

:::spoiler Flag
Flag: `Singapore`
:::

## ==Q8==
> Where is the insider's family live? (City only) 

### Recon
可以先觀察[IG post 1](https://www.instagram.com/p/CAjCdGrldGr/?hl=en)和[IG post 2](https://www.instagram.com/p/CAjCfM1lKhq/?hl=en)
![圖片.png](https://hackmd.io/_uploads/HyyzXUSX6.png)
![圖片.png](https://hackmd.io/_uploads/SJwMXLSma.png)

### Exploit
第一張圖片可以看到若隱若現的國旗，可能是Jordan / Palestine / United Arab Emirates，這三個國家的國旗都很像，再看第二張圖片可以發現有一個高塔，幾乎確定就是杜拜塔，也很符合他的國家(United Arab Emirates)

:::spoiler Flag
Flag: `Dubai`
:::

## ==Q9==
> File -> office.jpg:
You have been provided with a picture of the building in which the company has an office. Which city is the company located in? 

### Recon
直接找`hippodrome theatre chinese quarter`就知道是在英國的Birmingham

:::spoiler Flag
Flag: `Birmingham`
:::

## ==Q10==
> File -> Webcam.png:
With the intel, you have provided, our ground surveillance unit is now overlooking the person of interest's suspected address. They saw them leaving their apartment and followed them to the airport. Their plane took off and has landed in another country. Our intelligence team spotted the target with this IP camera. Which state is this camera in? 

### Recon
直接丟到image search就知道是`university of notre dame`，就在印第安納州

:::spoiler Flag
Flag: `INDIANA`
:::

## Reference