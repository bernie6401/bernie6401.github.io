---
title: NTUSTISC - AD Note - Lab(當前網域控制站(DC))
tags: [NTUSTISC, AD, information security]

category: "Security｜Course｜NTUST ISC｜AD｜1. 環境調查Normal"
date: 2024-01-31
---

# NTUSTISC - AD Note - Lab(當前網域控制站(DC))
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=SycYwgWohlu97dc3)

## Lab Time - 環境調查

### 情報蒐集：==當前網域控制站(DC)==
以駭客的角度來說，如果已經連到AD中，要怎麼知道目前DC是誰
常用的cheat sheet
```bash!
$ echo %logonserver%
$ nltest /dclist:<domain>
```
:::spoiler Implementation
```bash
$ echo %logonserver%
\\WIN-818G5VCOLJO
$ nltest /dclist:kuma.org
取得網域 'kuma.org' (從 '\\WIN-818G5VCOLJO.kuma.org') 中的 DC 清單。
    WIN-818G5VCOLJO.kuma.org [PDC]  [DS] 站台: Default-First-Site-Name
命令成功完成
```
![](https://hackmd.io/_uploads/S1pgfnvph.png)
從Win10當中下指令的確可以知道Win2016的PC Name是`WIN-818G5VCOLJO`
:::