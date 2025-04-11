---
title: TaiwanHolyHigh - Windows Forensics - Background
tags: [TaiwanHolyHigh, Forensics, Windows]

category: "Security/Course/Tai.HolyHigh/Windows OS Forensics"
---

# TaiwanHolyHigh - Windows Forensics - Background
[TOC]

## Background
### ==資安事件的流程==
![](https://hackmd.io/_uploads/BkbVWYmz6.png)
* Prepare
    * 建立Infra
    * 購買ISO(e.g. [ISO 27001](https://www.tsg.com.tw/blog-detail10-248-0-iso27001.htm))
    * SPA([資安健診](https://www.issdu.com.tw/service/9-shc))
* Predict
    * [Threat Intelligence(威脅情資)](https://www.informationsecurity.com.tw/article/article_detail.aspx?aid=8376)
    * Recon(情蒐)
    * Monitor(監控)
    * 搜尋Pattern
* Identify(識別): 有興趣可以看這一篇論文筆記[DeepCase](https://hackmd.io/@SBK6401/BJuCGSnAo)
    * [SOC(資安監控中心)](https://www.freedom.net.tw/ict-insight/security/siem-vs-soc.html)
        > ![](https://www.freedom.net.tw/images/article/caption/siem%20vs%20soc.jpg)
    * IDS: 入侵偵測系統（Intrusion Detection System，IDS）是用來偵測資訊系統或網路上潛在的惡意破壞活動
    * IPS: [IThelp - Active Defense](https://www.ithome.com.tw/tech/28712)
    * Audit: AD常常遇到
    * EDR
    * Code Review
* Prevent: 防禦攻擊
    * Firewall(Layer 4 - Transport)
    * [WAF(Layer 7 - Application)](https://www.oracle.com/tw/security/cloud-security/what-is-waf/)
    * [DLP(資料外洩防護)](https://www.mikotek.com.tw/dlp/)
* Incident Profile: 這個項目比較能夠得到一些惡意的行為，而該行為一定脫離不了下面三點
    1. Purpose/Payload(有可能是Data, Source, 或金錢等等)
    2. Path(透過甚麼途徑達成目的，有可能是USB, 社交工程, 0-day)
    3. Behavior(建立帳戶/開service/與C&C連線等等)
* Incident Response
    * Restore(主動)
    * Recovery(被動)
    * Isolate
* Deter: 主動式的阻絕
    * Inside
    * Outside(就是找外援通常是執法單位)
        * law enforcement(執法單位)
* Forensics Triage: 做分流的動作
    * 揮發性資料(RAM...)
    * Network
    * Process
    * System
    * Artifacts(registry/log/temp...)
* Duplicate(Image): 製作證據的映像檔$\to$非揮發性的資料
    * RAW Image
    * Evidence File
* Forensics Analysis
    * 已知項目(Known)
        * Keyword
        * Hash
    * Baseline
        * Recovery
        * Signature
        * Sorting
        * Artifact
            * LNK
            * Prefetch
            * SPL
            * Thumbnail
            * Registry(非揮發性)
            * Log
            * Recycle Bin
### ==網路攻擊鍊(Cyber Kill Chain)==
詳細資料: [TeamT5 - Cyber Kill Chain](https://teamt5.org/tw/posts/what-is-cyber-kill-chain/)
1. 偵查 Reconnaissance
2. 武裝 Weaponization
3. 遞送 Delivery
4. 漏洞利用 Exploitation: 確保遞送的惡意軟體，藉由目標對象的系統漏洞，得以順利開啟，並使攻擊者獲得控制權
5. 安裝 Installation
6. 發令與控制 Command & Control
7. 行動 Actions