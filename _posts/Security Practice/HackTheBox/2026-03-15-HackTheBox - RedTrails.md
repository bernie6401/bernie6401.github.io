---
layout: post
title: "HackTheBox - RedTrails"
date: 2026-03-15
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - RedTrails
<!-- more -->

* Challenge: https://app.hackthebox.com/challenges/RedTrails
* Challenge Scenario
    > Our SOC team detected a suspicious activity on one of our redis instance. Despite the fact it was password protected it seems that the attacker still obtained access to it. We need to put in place a remediation strategy as soon as possible, to do that it's necessary to gather more informations about the attack used. NOTE: flag is composed by three parts.


## Recon
這一題給一個network flow pcap，不長，所以先follow tcp stream，發現這是一個redis protocol(RESP)，並且發現攻擊者應該是已經取得了server password並且recon了一段時間，從stream 0中可以看到其中一段flag

<img src="/assets/posts/HackTheBox/RedTrails-1.png" width=300>

接著看stream 1，會發現有一段類似base64 encode的string

<img src="/assets/posts/HackTheBox/RedTrails-2.png" width=300>


## Reference
[^1]:[HTB RedTrails Forensics Challenge](https://mihirps.medium.com/htb-redtrails-forensics-challange-c487fe34af3f)