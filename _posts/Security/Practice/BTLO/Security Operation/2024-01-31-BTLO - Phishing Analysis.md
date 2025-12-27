---
title: BTLO - Phishing Analysis
tags: [BTLO, Security Operation]

category: "Security｜Practice｜BTLO｜Security Operation"
---

# BTLO - Phishing Analysis
<!-- more -->
Challenge: https://blueteamlabs.online/home/challenge/phishing-analysis-f92ef500ce

:::spoiler TOC
[TOC]
:::

## Scenario
> A user has received a phishing email and forwarded it to the SOC. Can you investigate the email and attachment to collect useful artifacts? 

## Tools
Text Editor
Mozilla Thunderbird
URL2PNG
WHOis 

## ==Q1==
> Who is the primary recipient of this email?

### Recon
這一題可以直接用[線上工具 - EML Viewer](https://products.groupdocs.app/zh-hant/viewer/eml)把eml file轉成pdf，不過風險就是有很多的資訊會流失掉，所以比較好的方式就是直接裝Mozilla Thunderbird查看
![圖片](https://hackmd.io/_uploads/Bk2fj8ldT.png)

:::spoiler Flag
Flag: `kinnar1975@yahoo.co.uk`
:::

## ==Q2==
> What is the subject of this email?

### Recon
呈上題
![圖片](https://hackmd.io/_uploads/BJA7o8g_6.png)

:::spoiler Flag
Flag: `Undeliverable: Website contact form submission`
:::

## ==Q3==
> What is the date and time the email was sent?

### Recon
呈上題
![圖片](https://hackmd.io/_uploads/r1NLsUgdT.png)

:::spoiler Flag
Flag: `18 March 2021 04:14`
:::

## ==Q4==
> What is the Originating IP?

### Recon
這個就是要用Text Editor string search Originating就會發現這個IP
![圖片](https://hackmd.io/_uploads/HJSG2Ul_p.png)

:::spoiler Flag
Flag: `103.9.171.10`
:::

## ==Q5==
> Perform reverse DNS on this IP address, what is the resolved host? (whois.domaintools.com)

### Recon
直接用[線上工具](https://whois.domaintools.com/)看這個IP的相關資訊
![圖片](https://hackmd.io/_uploads/Hyr5n8gdT.png)

:::spoiler Flag
Flag: `c5s2-1e-syd.hosting-services.net.au`
:::

## ==Q6==
> What is the name of the attached file?

### Recon
呈第一題可以發現有一個attachment
![圖片](https://hackmd.io/_uploads/BkVh28lua.png)

:::spoiler Flag
Flag: `Website contact form submission.eml`
:::

## ==Q7==
> What is the URL found inside the attachment?

### Recon
呈上題，點進這個附件可以看到一段URL
![圖片](https://hackmd.io/_uploads/S1bN6Uxdp.png)

:::spoiler Flag
Flag: `https://35000usdperwwekpodf.blogspot.sg?p=9swghttps://35000usdperwwekpodf.blogspot.co.il?o=0hnd`
:::

## ==Q8==
> What service is this webpage hosted on?

### Recon
呈上題，這個我是參考[^wp1]的說明，可以觀察釣魚的網址

:::spoiler Flag
Flag: `blogspot`
:::

## ==Q9==
> Using URL2PNG, what is the heading text on this page? (Doesn't matter if the page has been taken down!)

### Recon
這個就直接看[線上工具 - URL2PNG](https://www.url2png.com/#testdrive)
![圖片](https://hackmd.io/_uploads/SJg6TLl_p.png)

:::spoiler Flag
Flag: `Blog has been removed`
:::

## Reference
[^wp1]:[Phishing Analysis- Blue Team Lab Walkthrough](https://medium.com/@josephkarug/phishing-analysis-blue-team-lab-walkthrough-a164c63724e5)