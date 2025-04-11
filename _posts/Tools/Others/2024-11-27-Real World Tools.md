---
title: Real World Tools
tags: [Tools]

category: "Tools/Others"
---

# Real World Tools
## Kali-Linux
有關Kali的所有工具可以直接參考[Operating Systems for Ethical Hackers - A Platform Comparison of Kali Linux and Parrot OS](https://www.researchgate.net/profile/Syed-Zain-Ul-Hassan-2/publication/369305777_Operating_Systems_for_Ethical_Hackers_-_A_Platform_Comparison_of_Kali_Linux_and_Parrot_OS/links/6414544c315dfb4cce89b6a3/Operating-Systems-for-Ethical-Hackers-A-Platform-Comparison-of-Kali-Linux-and-Parrot-OS.pdf)
:::info
ul Hassan, S. Z., Muzaffar, Z., & Ahmad, S. Z. (2021). Operating Systems for Ethical Hackers-A Platform Comparison of Kali Linux and Parrot OS. International Journal, 10(3).
:::
裡面有詳細分類
* Information Gathering Tools(67)
* Vulnerability Analysis Tools(27)
* Exploitation Tools(21)
* Wireless Attacks Tools(54)
* Forensics Tools(23)
* Web Applications tools(43)
* Stress Testing tools(14)
* Sniffing & Spoofing Tools(33)
* Password Attacks Tools(39)
* Maintaining Access Tools(17)
* Reverse Engineering Tools(11)
* Reporting Tools(10)
* Hardware Hacking(6)
* Some Parrot OS in-built tools(20)

## Recon
* [Google Hacking](https://www.exploit-db.com/google-hacking-database)
    :::spoiler Description
    | Syntax | Description | Example |
    | ------ | ----------- | ------- |
    |+|連接多個關鍵字|--|
    |-|忽略關鍵字|--|
    |..|範圍|--|
    |\*|萬用字元|--|
    |''|精準查詢，一定要符合關鍵字|index of|
    |intext|搜尋網頁內容，列出符合關鍵字的網頁|intext:SECRET_KEY|
    |intitle|搜尋網頁中的標題|intitle:index of|
    |define|搜尋關鍵字的定義|define:hacker|
    |filetype|搜尋指定類型的文件|filetype:pdf|
    |info|搜尋指定網站的基本資訊|info:www.fcu.edu.tw|
    |related|搜尋類似於指定網站的其他網站|related:www.fcu.edu.tw|
    |inurl|尋找指定的字串是否在網址列當中|inurl:www.fcu.edu.tw|
    | site   | 搜尋指定網址的內容|site:www.fcu.edu.tw|
    :::


* [Shodan](https://www.shodan.io/dashboard) / [Censys](https://search.censys.io/)
    :::spoiler Description
    ![](https://hackmd.io/_uploads/Hym-h3oH2.png)
    :::

## Dictionary Brute Force
* [John The Ripper](https://www.openwall.com/john/)
    ```bash
    # NTLM
    $ ./run/john.exe {pwn file} --wordlist={dictionary path} --format={NT...}
    
    # JWT
    $ john jwt.txt --wordlist={e.g. /usr/share/wordlists/rockyou.txt} --format={jwt alg, e.g. HMAC-SHA256}
    ```
* [Rockyou.txt](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiyotmP3uD_AhVB72EKHd3QCHMQFnoECBQQAQ&url=https%3A%2F%2Fgithub.com%2Fbrannondorsey%2Fnaive-hashcat%2Freleases%2Fdownload%2Fdata%2Frockyou.txt&usg=AOvVaw3snAERl1mU6Ccr4WFEazBd&opi=89978449)
* [Online Tool 1](https://www.cmd5.com/)
* [Online Tool 2](https://hashes.com/en/decrypt/hash)
* [hashcat](https://home.gamer.com.tw/creationDetail.php?sn=3669363):
    ```bash
    # NTLM
    $ hashcat -a 0 -m 1000 {ntlm.hash} {rockyou.txt} --force
    
    # JWT
    $ hashcat -a 3 -m 16500 {jwt.txt} {secrets format, e.g. ?a?a?a?a}
    ```
## Escalation
* For Windows: [Mimikatz](https://github.com/ParrotSec/mimikatz)

## Overall
* [Mitre ATT&CK](https://attack.mitre.org/)
* 如果要查常用指令怎麼下，可以找tldr

## Inspect
* [Virus Total](https://www.virustotal.com/gui/home/upload)
* [Alien Vault](https://otx.alienvault.com)
* [IBM X-Force](https://exchange.xforce.ibmcloud.com)
* [Any.Run](https://app.any.run/): Online Sandbox
## OSINT
* [sherlock](https://github.com/sherlock-project/sherlock)
    ```bash
    $ git clone https://github.com/sherlock-project/sherlock.git
    $ cd sherlock
    $ conda create --name sherlock python=3.10 -y
    $ pip install -r requirements.txt
    $ python sherlock/sherlock.py {username}
    ```
* [Image Search](https://images.google.com/)
* [Google Map](https://www.google.com/maps)
* [OSINT Framework](https://osintframework.com/)
    * [Phone](https://www.truecaller.com)
    * [Whois](https://www.whois.com/whois) or [ipwhoisinfo](https://ipwhoisinfo.com/)
    * [Whatsmyname - online tool](https://whatsmyname.app/)
    * [DNS Lookup(從Domain Name看IP)](https://www.whatismyip.com/dns-lookup/)
* 如果要查看手機本身的Network IP(不是wifi)，可以看 https://ipinfo.io 