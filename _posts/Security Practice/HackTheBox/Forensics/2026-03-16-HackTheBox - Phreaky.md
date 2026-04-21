---
layout: post
title: "HackTheBox - Phreaky"
date: 2026-03-16
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - Phreaky
<!-- more -->

* Scenario
    > In the shadowed realm where the Phreaks hold sway,
    > 
    > A mole lurks within, leading them astray.
    > 
    > Sending keys to the Talents, so sly and so slick,
    > 
    > A network packet capture must reveal the trick.
    > 
    > Through data and bytes, the sleuth seeks the sign,

## Recon
網路封包的起手式除了TCP Stream Follow以外，我也會看中間溝通的過程有沒有傳輸檔案，果不其然，發現兩邊透過SMTP協定傳送加密的檔案
<img src="/assets/posts/HackTheBox/Phreaky-1.png" width=300>

所以實際把這些檔案dump下來會發現是一個email的附檔文件，把attached file載下來並且用email中附的密碼可以extract出一個pdf file的其中一段
```
phreaks_plan.pdf.part1
phreaks_plan.pdf.part2
...
phreaks_plan.pdf.part15
```
我們要做的事情就是重複15次的開email → 下載附檔 → 解密，並且最後把這15個檔案拼在一起

## Exploit
```bash
$ for i in $(seq 1 15); do cat "phreaks_plan.pdf.part$i"; done > phreaks_plan.pdf
```

會發現這個pdf file的最後有flag
Flag: `HTB{Th3Phr3aksReadyT0Att4ck}`