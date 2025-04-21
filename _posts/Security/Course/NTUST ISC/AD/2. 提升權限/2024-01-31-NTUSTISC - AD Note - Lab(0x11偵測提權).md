---
title: NTUSTISC - AD Note - Lab(偵測提權)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/2. 提升權限"
---

# NTUSTISC - AD Note - Lab(偵測提權)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=M0LV3dBCMCOy58LN&t=3600)

## Background
* 提權方法
    * 利用弱點
    * Hijack Token
    * Guess Password
    * 管理服務
    * 錯誤配置

## Lab Time - 本地提權

### ==偵測Network Service提權==
利用Event ID: 4624
* 類型: 5
* 虛擬帳戶: 是
* 提高權限的權杖: 是
這樣的rule會有高機率命中，但經過實測會發現他不會顯示出類型5和虛擬帳戶為是的event，只有類型3會被顯示出來，如下圖
![](https://hackmd.io/_uploads/ryoW9NfC3.png)