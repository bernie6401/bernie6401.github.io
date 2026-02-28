---
title: CyberDefender - CorporateSecrets (Part 1)
tags: [CyberDefender, Endpoint Forensics]

category: "Security Practice｜CyberDefender｜Endpoint Forensic｜CorporateSecrets - Medium"
date: 2024-01-31
---

# CyberDefender - CorporateSecrets (Part 1)
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/33
Part 2: https://hackmd.io/@SBK6401/ByFhEE8X6
Part 3: https://hackmd.io/@SBK6401/HyHp4NLQT
Part 4: https://hackmd.io/@SBK6401/H1rAEV87p

:::spoiler TOC
[TOC]
:::

## Tools: 
* FTK Imager
* Registry Explorer
* RegRipper
* HxD
* DB Browser for SQLite
* HindSight
* Event Log Explorer
* MFTDump


## ==Q1==
> What is the current build number on the system? 

### Exploit
直接把Software hive從`root/Windows/System32/config/` export出來後找`Microsoft/Windows NT/CurrentVersion`中就有紀錄CurrentBuild number
![圖片.png](https://hackmd.io/_uploads/ryvoSV8mT.png)
:::spoiler Result
![圖片.png](https://hackmd.io/_uploads/rJpJ8EUXa.png)
:::

:::spoiler Flag
Flag: `16299`
:::

## ==Q2==
> How many users are there? 

### Exploit
直接看`Microsoft/Windows NT/CurrentVersion/ProfileList`有幾個SID就知道了
![圖片.png](https://hackmd.io/_uploads/H1A6vVL7a.png)

:::spoiler Flag
Flag: `6`
:::

## ==Q3==
> What is the CRC64 hash of the file "fruit_apricot.jpg"? 

### Exploit
在`root/Users/hansel.apricot/Pictures/Saved Pictures`可以找到，再用[線上工具](https://www.lddgo.net/en/encrypt/crc)，記得選擇CRC-64-ECMA的演算法才會是對的
![圖片.png](https://hackmd.io/_uploads/HyAYjVUX6.png)

:::spoiler Flag
Flag: `ED865AA6DFD756BF`
:::

## ==Q4==
> What is the logical size of the file "strawberry.jpg" in bytes? 

### Recon
在`root/Users/suzy.strawberry/Pictures/`可以找到，右鍵看他的內容就知道了
![圖片.png](https://hackmd.io/_uploads/SkNOwwIma.png)

:::spoiler Flag
Flag: `72448`
:::

## ==Q5==
> What is the processor architecture of the system? (one word)

### Exploit
這是新的知識，processor architecture就在`SYSTEM/ControlSet001/Control/Session Manager/Environment/`
![圖片.png](https://hackmd.io/_uploads/BJYgfYLQp.png)

:::spoiler Flag
Flag: `amd64`
:::

## ==Q6==
> Which user has a photo of a dog in their recycling bin? 

### Recon
首先進入recycle bin看到底是哪一個SID丟棄這張圖片，發現是`S-1-5-21-2446097003-76624807-2828106174-1005`，回到registry去看他的username是甚麼

### Exploit
![圖片.png](https://hackmd.io/_uploads/B11movI7T.png)

:::spoiler Flag
Flag: `hansel.apricot`
:::

## ==Q7==
> What type of file is "vegetable"? Provide the extension without a dot. 

### Recon
從`root/Users/miriam.grapes/Pictures/`就可以找到vegetable，看到前面的file signature就可以知道是7z的壓縮檔

### Exploit
![圖片.png](https://hackmd.io/_uploads/SJQCpPIXp.png)

:::spoiler Flag
Flag: `7z`
:::

## ==Q8==
> What type of girls does Miriam Grapes design phones for (Target audience)? 

### Recon
這一題是全部解完才回來解的，因為當初真的一點想法都沒有，不過仔細看Miriam Grapes的folder，發現他是使用firefox當作browser，所以沒想法的時候就看瀏覽紀錄就對了(firefox的artifact就在`./Users/miriam.grapes/AppData/Roaming/Mozilla/Firefox/Profiles/9far2v52.default-release/places.sqlite`)
![圖片.png](https://hackmd.io/_uploads/SJySlAwma.png)

### Exploit
果然發現一點東西，他設計的這個手機就是面向VSCO女性族群而設計的
![圖片.png](https://hackmd.io/_uploads/BJamJAwXp.png)
[What is VSCO?](https://hot-tag.com/fashion/vsco%E6%98%AF%E4%BB%80%E9%BA%BC%E6%84%8F%E6%80%9D%EF%BC%9F%E4%BB%80%E9%BA%BC%E6%99%82%E5%80%99%E7%94%A8%EF%BC%9F-vsco/)
> 有一種意思是指VSCO是一種修圖(濾淨)的APP，全名叫做(Visual Supply Company)，但另一種意思是指一種女性的穿著與生活風格。VSCO Girl幾乎是連在一起的字詞。這種風格的女性穿搭是簡單風，Tshirt 搭配短褲，或是簡單的襯衫與牛仔褲的組合，反正一看就是輕鬆、簡單的穿搭就符合VSCO

:::spoiler Flag
Flag: `VSCO`
:::

## ==Q9==
> What is the name of the device?

### Exploit
直接看`SYSTEM/ControlSet001/Control/ComputerName/ComputerName`

:::spoiler Flag
Flag: `DESKTOP-3A4NLVQ`
:::

## Reference