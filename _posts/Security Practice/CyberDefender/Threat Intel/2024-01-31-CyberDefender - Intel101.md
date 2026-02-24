---
title: CyberDefender - Intel101
tags: [CyberDefender, Threat Intel]

category: "Security Practice｜CyberDefender｜Threat Intel"
date: 2024-01-31
---

# CyberDefender - Intel101
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/38

:::spoiler TOC
[TOC]
:::

## Scenario
> Open-source intelligence (OSINT) exercise to practice mining and analyzing public data to produce meaningful intel when investigating external threats as a security blue team analyst.
Tools

## Tool
* [Google Lens](https://lens.google/)
* [archive.org](https://web.archive.org/)
* [WhoIS](https://www.tecmint.com/whois-command-get-domain-and-ip-address-information/#:~:text=In%20Linux%2C%20the%20whois%20command,in%20a%20human%2Dreadable%20format.)

## ==Q1==
> Who is the Registrar for jameskainth.com? 

### Recon
看[whois](https://www.whois.com/whois/jameskainth.com)的搜尋結果
![圖片.png](https://hackmd.io/_uploads/rJIevf8mp.png)

:::spoiler Flag
Flag: `NameCheap`
:::

## ==Q2==
> You get a phone call from this number: 855-707-7328, they were previously known by another name? (No spaces between words) 

### Recon
這一題是參考[^Intel101-wp]，看[truecaller](https://www.truecaller.com/search/us/855-707-7328)的搜尋結果會發現他是Spectrum Cable的客服電話，這應該是其中一個美國電信公司，所以直接查他舊的名字就知道
![圖片.png](https://hackmd.io/_uploads/BJ5wvfUmp.png)

:::spoiler Flag
Flag: `TimeWarnerCable`
:::

## ==Q3==
> What is the Zoom meeting id of the British Prime Ministers Cabinet Meeting? 

### Recon
慢慢google就會看到[這個網站](https://grahamcluley.com/uk-cabinet-zoom-meeting/)
![](https://grahamcluley.com/wp-content/uploads/2020/03/cabinet-zoom.jpeg.webp)

:::spoiler Flag
Flag: `539544323`
:::

## ==Q4==
> What Percentage of full-time degree-seeking freshmen from the fall of 2018 re-enrolled to Champlain in the fall of 2019? 

### Recon
這一題是參考[^Intel101-wp]的說明，因為現在都只有2022/2023之類的比較近一點的資訊，如果用wayback machine也沒有那麼久之前的資料，不過用wayback machine是正確的方向

:::spoiler Flag
Flag: `82.5%`
:::

## ==Q5==
> In 1998 specifically on February 12th, Champlain was planning on adding an exciting new building to its campus. Back then, it was called “The Information Commons”. Can you find a picture of what the inside would look like? Upload the sha256 hash here. 

### Recon
直覺會先用wayback machine看1998的時候，網站的變化

### Exploit
1. wayback machine
    ![圖片.png](https://hackmd.io/_uploads/HyYScQL7p.png)
2. Search Informations Common
    ![圖片.png](https://hackmd.io/_uploads/rkbOqXIQT.png)
3. 存檔並checksum
    ![inside1.jpg](https://hackmd.io/_uploads/rJes9XIQT.jpg)
    ![圖片.png](https://hackmd.io/_uploads/SynAqmUm6.png)

:::spoiler Flag
Flag: `f4952b314eb15acf0eec79c954f83881c17d50d2b5922ee37e8fc5e5cd1aeac2`
:::

## ==Q6==
> One of Champlain College's Cyber Security Faculty got a bachelor's degree in arts from this Ohioan university. Who was the other faculty member who studied there? (FirstName LastName - two words)

### Exploit
1. 可以先看[Cybersecurity - facaulty](https://www.champlain.edu/technology-degrees/computer-networking-and-information-security/faculty)的東西
    ![圖片.png](https://hackmd.io/_uploads/r1_Jl4IXT.png)
2. 題目有提到有人是在Ohioan大學取得美術學士學位，這是個重點，他不是說在Ohio University而是Ohioan University，也就是只提到該間大學是在Ohio，所以要先知道是哪一間，parse過一下現任的員工後發現University of Toledo就在Ohio State
    ![圖片.png](https://hackmd.io/_uploads/Hynb-NUmp.png)
3. 題目問的是"其他員工"也是在該間大學就讀過，而不是"其他cybersecurity員工"，代表我們要找的對象是全校所有的員工，因此可以直接在所有員工的頁面parse有這間大學的資訊頁面，最後我找到這個人，字數和hint也和題目相同
    ```
    inurl:champlain.edu/academics/our-faculty intext:University of Toledo
    ```
    ![圖片.png](https://hackmd.io/_uploads/H1E-zN8mp.png)
    ![圖片.png](https://hackmd.io/_uploads/H1hbf4L7a.png)

:::spoiler Flag
Flag: `Todd Schroeder`
:::

## ==Q7==
> In 2019 UVM’s Ichthyology Class Had to Name their fish for class. Can you find out what the last person on the public roster named their fish? 

### Recon
這一題照著[^Intel101-wp]也是找不到

:::spoiler Flag
Flag: `Saccopharyngiformes`
:::

## ==Q8==
> Can You Figure Out Which State This Picture Has Been Taken From? See attached photo 

### Exploit
這一題我是先google map找外國的恐龍主題樂園，然後就看他的所在地try & error，因為答案有最後一個char的hint

:::spoiler Flag
Flag: `Virginia`
:::

## Reference
[^Intel101-wp]:[CyberDefenders Walkthrough : Intel101](https://infosecwriteups.com/cyberdefenders-walkthrough-intel101-47dc943409a6)