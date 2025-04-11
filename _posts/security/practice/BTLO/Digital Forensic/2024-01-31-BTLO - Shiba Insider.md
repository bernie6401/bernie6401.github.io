---
title: BTLO - Shiba Insider
tags: [BTLO, Digital Forensics]

category: "Security > Practice > BTLO > Digital Forensic"
---

# BTLO - Shiba Insider
Challenge: https://blueteamlabs.online/home/challenge/shiba-insider-5b48123711

:::spoiler TOC
[TOC]
:::

## Tools
Wireshark
CyberChef
Steghide
Command Line
Exiftool 

## ==Q1==
> What is the response message obtained from the PCAP file?
### Recon
這一題首先看到一個pcap file，以及zip file，不過zip file需要密碼才能unzip，所以先看pcap file有沒有相關訊息

這個流量紀錄非常簡單，就是一個簡單的tcp connection，包含前面的三向交握以及get packet，交換完訊息之後當然就是要finish conversation，所以重點在中間他們交換的訊息
![圖片](https://hackmd.io/_uploads/S1rZCIpPT.png)

傳回來的訊息說: `use your own password`，其實也就是該題的答案

:::spoiler Flag
Flag: `use your own password`
:::
## ==Q2==
> What is the password of the ZIP file?
### Recon
呈上題，我們看到他給的提示後，往上看他的Authorization其實是個base64 encode的可疑資訊，decode之後發現是個username:password的資訊→==fakeblue:redforever==

:::spoiler Flag
Flag: `redforever`
:::
## ==Q3==
> Will more passwords be required?
### Recon
呈上題，利用密碼解開zip file後會看到readme.txt和ssdog1.jpeg，根據readme的內容，我們之後不會需要用到其他的密碼

:::spoiler Flag
Flag: `No`
:::
## ==Q4==
> What is the name of a widely-used tool that can be used to obtain file information?
### Recon
呈上題，看到圖片直覺就是那幾個工具: steghide / exiftool / pngcheck / stat / file / formost / zsteg / binwalk...，所以該題就是==exiftool==

:::spoiler Flag
Flag: `exiftool`
:::
## ==Q5==
> What is the name and value of the interesting information obtained from the image file metadata?
### Recon
查看完了exiftool的確看到蠻多資訊，包含steghide，所以根據字數的提示找到flag

:::spoiler Flag
Flag: `Technique:Steganography`
:::
## ==Q6==
> Based on the answer from the previous question, what tool needs to be used to retrieve the information hidden in the file?
### Recon
呈上題，看解析出的info就知道是用steghide藏訊息在裡面

:::spoiler Flag
Flag: `steghide`
:::
## ==Q7==
> Enter the ID retrieved.
### Recon
我們利用steghide解析出隱藏的訊息並且根據上兩題的提示沒有任何密碼，就可以得到一個idInsider.txt的檔案，內容就是該題Flag
```bash
$ steghide extract -sf ssdog1.jpeg
Enter passphrase:
wrote extracted data to "idInsider.txt".
```

:::spoiler Flag
Flag: `0726ba878ea47de571777a`
:::
## ==Q8==
> What is the profile name of the attacker?
### Recon
這一題是最難的，應該說他的題目敘述讓我很難想到怎麼解，所以這個是按照其他人的[^wp]才知道

首先前一題的內容是一個user的id，而我們在第二題解析出的username其實是個fake username，真正的user其實應該是我們前一題拿到的id對應到的user，也就是BTLO網站上會顯示的user ID，所以只要前往https://blueteamlabs.online/home/user/0726ba878ea47de571777a 的頁面，就會看到該user為何
![圖片](https://hackmd.io/_uploads/BykebvTva.png)
是一個叫做bluetiger的用戶，也就是我們此題的答案
### Exploit
:::spoiler Flag
Flag: `bluetiger`
:::
## Reference
[^wp]:[ Shiba Insider - Steganography Challenge - Blue Team Labs Online ](https://youtu.be/Ij5954djG3o?si=0woTtMAfv36SlHZe)