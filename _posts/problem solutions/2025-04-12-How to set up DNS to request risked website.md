---
layout: post
title: "How to set up DNS to request risked website"
date: 2025-04-12
categories: "Problem Solutions"
tags: [problem solution]
draft: false
toc: true
comments: true
---

# How to set up DNS to request risked website
<!-- more -->

## Problem Statement
因為學校的宿舍DNS有filter我自己的blog URL，所以為了要能夠訪問自己的blog，要修改電腦的DNS preference

## Solution
1. 開啟「控制台」→「網路和網際網路」→「網路和共用中心」。
    ![alt text](/assets/posts/螢幕擷取畫面 2025-04-12 220056.png)
2. 點選左邊的「變更介面卡設定」。
    ![alt text](/assets/posts/螢幕擷取畫面 2025-04-12 215603.png)
3. 對你正在連線的 Wi-Fi / Ehternet 點右鍵 → 選「內容」。
    ![alt text](/assets/posts/螢幕擷取畫面 2025-04-12 220207.png)
4. 雙擊「Internet Protocol Version 4 (TCP/IPv4)」。
5. 勾選「使用下列 DNS 伺服器位址」。
6. 輸入：
    * 首選 DNS：8.8.8.8
    * 備用 DNS：8.8.4.4
    ![alt text](/assets/posts/螢幕擷取畫面 2025-04-12 220258.png)
