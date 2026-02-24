---
title: TaiwanHolyHigh - SoC基礎維運 - ArcSight教學
tags: [TaiwanHolyHigh]

category: "Security Course｜Tai.HolyHigh｜SoC基礎維運"
date: 2024-01-31
---

# TaiwanHolyHigh - SoC基礎維運 - ArcSight教學
<!-- more -->

## Set Up
先進到https://bit.ly/44IFecN下載ArcSight Console，並且全部default下一步
1. (editor需要admin權限)進入localhost host DNS解析 -> C:\Windows\System32\drivers\etc\host
	新增 211.75.237.80 chtpoc
2. 打開ArcSight Console，用之前提供的帳密以及最後打chtpoc，進行登入
    ![圖片](https://hackmd.io/_uploads/B1_MkKc8p.png)
3. 登入之後的狀態
    ![圖片](https://hackmd.io/_uploads/BJNleKc8p.png)

![圖片](https://hackmd.io/_uploads/Hy8IUYqIa.png)
![圖片](https://hackmd.io/_uploads/Syx6UK986.png)
![圖片](https://hackmd.io/_uploads/S1vRUKcUp.png)
ArcSight預設有分大小寫
![圖片](https://hackmd.io/_uploads/SJrXPY5UT.png)


活動頻道可以儲存0
![圖片](https://hackmd.io/_uploads/SJCEqt9Up.png)
![圖片](https://hackmd.io/_uploads/HkSr5t5La.png)

## 規則
* WAF規則
    ![圖片](https://hackmd.io/_uploads/B1Ljrc9UT.png)
* Firewall規則
    ![圖片](https://hackmd.io/_uploads/rJY6S55IT.png)
* IPS
    ![image](https://hackmd.io/_uploads/Bykw2m3Ia.png)
* Firewall-BotNet
    ![image](https://hackmd.io/_uploads/HkZK2QnIT.png)
* Snort
    ![image](https://hackmd.io/_uploads/rJ3onmnUp.png)
* Trojan
    ![image](https://hackmd.io/_uploads/BkPhnX2U6.png)
* WineventLog
    ![image](https://hackmd.io/_uploads/SkSan7hUT.png)

## 清單
* 抑制清單
    ![image](https://hackmd.io/_uploads/rkPcT7hL6.png)
* 弱掃清單
    ![image](https://hackmd.io/_uploads/HJNlNSnU6.png)

## 規則
* 即時規則
    ![image](https://hackmd.io/_uploads/BJFeaX2La.png)
* 中繼站監控
    ![image](https://hackmd.io/_uploads/HyqNaX3Lp.png)
    ![image](https://hackmd.io/_uploads/H1mr672Up.png)

* 中繼站監控持續連線
    ![image](https://hackmd.io/_uploads/Sk4wpm28T.png)
* WAF弱掃
    ![image](https://hackmd.io/_uploads/H1kMNHhL6.png)
    ![image](https://hackmd.io/_uploads/rJ6GEHnUp.png)
    ![image](https://hackmd.io/_uploads/HymmES386.png)
