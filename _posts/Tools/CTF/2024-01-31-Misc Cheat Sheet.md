---
title: Misc Cheat Sheet
tags: [Tools, CTF, Misc]

category: "Tools｜CTF"
date: 2024-01-31
---

# Misc Cheat Sheet
<!-- more -->

## CTF - Encode & Decode

| Encode & Decode |
| -------- |
|[Free Online Barcode Reader](https://online-barcode-reader.inliteresearch.com/)|
|[QR Code Barcode Reader Online](https://products.aspose.app/barcode/recognize/qr#/recognized)|
| [Encoding](https://emn178.github.io/online-tools/index.html)|
| [獸語](https://roar.iiilab.com/)|

## CTF - Check file info
```bash
$ binwalk [-e] [filename] # or binwalk --dd=".*" [filename]
$ exiftool [filename]
$ pngcheck [filename]
$ stat [filename]
$ file [filename]
```
* `$ binwalk -e` 的範例可以參考[Deadface - Electric Steel ]({{base.url}}/DEADFACE-CTF-2023#Electric-Steel)

## CTF - Steganography
* text: [zsteg](https://github.com/zed-0xff/zsteg)(just for `bmp` and `png` files), [Quick Crypto](http://quickcrypto.com/download.html)
* file: steghide(`sudo apt-get install steghide`)(`$ steghide extract -sf atbash.jpg`)
* 進階的steghide → [stegseek](https://github.com/RickdeJager/stegseek)
    ```bash
    $ wget https://github.com/RickdeJager/stegseek/releases/download/v0.6/stegseek_0.6-1.deb
    $ sudo apt install ./stegseek_0.6-1.deb -y
    $ stegseek [stegofile.jpg] [wordlist.txt]
    ```

## CTF - Sound
* hide files: [MP3stego](https://www.petitcolas.net/steganography/mp3stego/)
    ```bash
    $ ./encode -E hidden_text.txt -P pass svega.wav svega_stego.mp3
    $ ./decode -X -P pass svega_stego.mp3
    ```
* sound to image:
    * [How to convert a SSTV audio file to images using QSSTV - en](https://ourcodeworld.com/articles/read/956/how-to-convert-decode-a-slow-scan-television-transmissions-sstv-audio-file-to-images-using-qsstv-in-ubuntu-18-04)
    * [How to convert a SSTV audio file to images using QSSTV - zh-cn](https://www.srcmini.com/62326.html)
* hide message: [silenteye](https://sourceforge.net/projects/silenteye/)

## CTF - Others
* [All stego decrypt tools](https://aperisolve.fr/)
* [All stego encrypt tools](https://tools.miku.ac/)
* [ctf tool](http://www.ctftools.com/)
* [Other people's note](https://w1a2d3s4q5e6.blogspot.com/2016/06/blog-post.html)

## Pentest
可以參考[^1]，裡面有詳細說明Vulnerability Assessment and Penetration Testing (VAPT)會使用到的工具有哪些。

### 平台
* Kali的所有工具可以直接參考[^2]，裡面有詳細分類
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
* [Everything About Net Scanning](https://www.yougetsignal.com/)
* [WpScan](https://wpscan.com/): 專門檢測WordPress類型的網頁，有哪些漏洞，前期可以掃描出WP版本、安裝的theme或是插件有哪些、安全漏洞等等
* [Nessus教學](https://ithelp.ithome.com.tw/articles/10268209): Nessus 作為修復網路、網站和軟體開發中的安全漏洞、作業系統漏洞、應用程式漏洞、配置漏洞等的工具
* [Metasploit教學](https://ithelp.ithome.com.tw/articles/10302923)


### Pre-engagement interactions
* 確認測試範圍
* 簽 NDA
* 確定目標

### Intelligence Gathering (Recon)
* [Google Hacking](https://www.exploit-db.com/google-hacking-database)

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
* [Shodan](https://www.shodan.io/dashboard)
* [Censys](https://search.censys.io/)
    ![](https://hackmd.io/_uploads/Hym-h3oH2.png)

#### Inspect Platform
* [Virus Total](https://www.virustotal.com/gui/home/upload)
* [Alien Vault](https://otx.alienvault.com)
* [IBM X-Force](https://exchange.xforce.ibmcloud.com)
* [Any.Run](https://app.any.run/): Online Sandbox

#### Mail
* [PST Viewer](https://goldfynch.com/goldfynch-pst-viewer)
* [eml Viewer](https://products.groupdocs.app/zh-hant/viewer/eml)
* [ThunderBird Client](https://www.thunderbird.net/zh-TW/)

#### OSINT
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

#### Web Directory
* Dirbuster
* Gobuster
* Wfuzz

#### Network Info & Package
* [Wireshark cheat sheet](https://packetlife.net/blog/2008/oct/18/cheat-sheets-tcpdump-and-wireshark/)
    
    |Type|eth|ip|tcp|udp|說明|
    |---|---|---|---|---|---|
    |dst|eth.dst == ff:ff:ff:ff:ff|ip.dst == 140. 134.4. 1|||目的 MAC/IP|
    |src|eth.src == 00:e0:18:64;ce:f2|ip.src == 140.134. 30.72|||來源 MAC/IP|
    |addr|eth.addr == ff:ff:ff:ff:ff|ip.addr == 140.134. 30.72|||MAC/IP 位址|
    |proto||ip.proto == 0x06(TCP)<br>ip.proto == 0x01(ICMP)<br>ip.proto == 0x11 (UDP)|||下一層協定|
    |type|eth.type == 0x800(IP)<br>eth.type == 0x806(ARP)||||下一層協定|
    |port|||tcp.port == 23(Talnet)|ucp.port == 53|Port編號|
    |dstport|||tcp.dstport == 80(HTTP)|ucp.dstport == 53(DNS)|目的Port|
    |scrport|||tcp.scrport == 21(FTP)|ucp.scrport == 69(TSTP)|來源Port|
* [nmap](http://www.osslab.tw/books/linux-administration/page/nmap-%E5%B8%B8%E7%94%A8%E6%8C%87%E4%BB%A4%E9%9B%86), [教學](https://blog.gtwang.org/linux/nmap-command-examples-tutorials/)
    ```bash
    $ sudo apt-get install nmap
    ```
* [ntpdc](https://www.ibm.com/docs/zh-tw/aix/7.3?topic=n-ntpdc4-command)
    ```bash
    $ sudo apt-get install ntpdc
    ```
* tcpflow
    ```bash
    $ sudo tcpflow -r {pcap file}
    ```
* [dsniff]: Various tools to sniff network traffic for cleartext insecurities
    * arpspoof: 
        ```bash
        $ arpspoof -t victim_ip router_ip
        $ arpspoof -i eth0 -t victim_ip -r gateway
        ```
    * dnsspoof: Forge replies to DNS address / pointer queries
        ```bash
        $ sudo dnsspoof -i eth0 -f dns.txt
        ```
    * dsniff: Password sniffer
* [Snort](https://www.snort.org/downloads): 是一個非常知名的開源網路入侵偵測系統（IDS, Intrusion Detection System），有3種模式
    * Sniffer Mode: 最基本模式，只是讀取封包並顯示，類似tcpdump
        ```bash
        $ snort -v
        ```
    * Packet Logger Mode: 將封包記錄到檔案
        ```bash
        $ snort -dev -l ./log
        ```
    * Network Intrusion Detection Mode（最常用）: 使用 rules 來偵測攻擊
        ```bash
        $ snort -c snort.conf
        ```

        ```
        # 如果任何 TCP 流量連到192.168.1.10:80就產生 alert
        alert tcp any any -> 192.168.1.10 80 (msg:"Possible attack"; 
        sid:10001;)

        # 如果某個來源在 1 秒內向 SSH server 發送 2 次 SSH 連線流量，就觸發警報。
        ## 任何 TCP 流量 → port 22 都會被檢查。
        ## 只檢查 client 發送到 SSH server 的封包
        ## 封包 payload 必須包含：SSH
        ## 不區分大小寫
        ## 從 payload 的 第 0 byte 開始比對。
        ## 只檢查 前 4 bytes。所以實際上檢查：payload[0:4]是否包含：SSH
        ## 同一個來源 IP在 1 秒內發送 2 次符合條件的封包
        ## 每個 rule 的唯一 ID。
        alert tcp any any -> any 22 
        ( msg:"SSH Brute Force Attempt"; 
        flow:established,to_server; 
        content:"SSH"; 
        nocase; 
        offset:0; 
        depth:4; 
        detection_filter:track by_src, count 2, seconds 1; 
        sid:1000001; 
        rev:1;)
        ```

### Threat Modeling
* 分析 attack surface
* 找 attack path

### Vulnerability Analysis
* 找漏洞
* CVE analysis

### Exploitation
* 利用漏洞取得 access
* Post Exploitation

#### Wireless Related
* 大部分都會用到[Aircrack](https://sectools.tw/aircrack-ng-%E6%95%99%E5%AD%B8/)這個工具
* Deauthentication - [airodump-ng教學](http://atic-tw.blogspot.com/2014/01/airodump-ng.html) / [aireplay-ng教學](http://atic-tw.blogspot.com/2014/01/aireplay-ng6.html)
    * 攻擊說明: [\[Day 05\]資安百物語：第二談：現代飛頭蠻的反制法-反無人機技術(下) ](https://ithelp.ithome.com.tw/articles/10218551?sc=rss.iron)
    1. Scan
        將掃描範圍縮小到一個目標，並取得連接到目標網路的裝置的MAC位址。
        ```
        $ airodump-ng -bSSID <bssid> --ch <channels> WLAN0mon
        # 此命令用於通過識別 BSSID（基本服務集識別符）和所使用的通道來設置目標網路上的掃描
        # -c: 指定只接收特定的 channels，如果有多個 channel，用 , 分隔，例如：-c 6,8,10,11
        ```
    2. Attack
        ```bash
        $ aireplay-ng --deauth <count, e.g. 1000> -a <bssid, e.g. 6A:BF:C4:06:35:94> -c <AP MAC address, e.g 34:CF:F6:96:72:E2> wlan0mon
        # -c dmac : 指定 Client 的 MAC address
        # -a bssid : 指定 AP 的 MAC address
        # --deauth:  count 是指執行阻斷的次數，如果設為 0 表循環攻擊，Client 將無法上網。
        ```
* Fluxion: 攻擊說明與工具教學: [實戰-Fluxion與wifi熱點偽造、釣魚、中間人攻擊、wifi破解](https://www.cnblogs.com/xuanhun/p/5783836.html)，Fluxion 攻擊的主要目標是獲取目標 Wi-Fi 網路使用者使用的密碼或訪問憑據。此攻擊可使攻擊者未經授權訪問目標網路，而有關於Captive Portal(WEB Portal)的驗證流程可以參考[這篇](https://ithelp.ithome.com.tw/articles/10280421)
    1. Captive Portal Attack
        根據前面的background可以知道web portal的驗證流程，那如果把原本的hotspot換成一個假的hotspot，讓使用者誤以為這是真的驗證頁面(需要帳號密碼之類的)，那我們就有機會拿到credentials session
    2. 直接取得SSID/BSSID/Channel Used/Password Used/Type of Security Applied
* MITM - [Xerosploit教學](https://blog.csdn.net/chinabyxl/article/details/121463891): Sniff模組允許攻擊者監控通過目標Wi-Fi網路的數據流量，包括使用者發送的數據。通過監視此類流量，攻擊者可以竊取身份驗證憑據、個人資訊或其他敏感數據等資訊，sniff完了以後可以用wireshark打開看流量
* WEP/WPA Attack: WEP/WPA 注入攻擊是針對使用 WEP/WPA 安全協定的無線網路的針對性攻擊。此攻擊旨在滲透網路安全並獲得對透過網路傳輸的資料流量的未經授權的存取。一旦收集到加密的流量數據，攻擊者就可以分析該數據的模式和結構，以識別網路中使用的加密金鑰。透過取得加密金鑰，攻擊者可以破解透過網路發送的資料流量的加密。
    1. Handshake on the target Wi-Fi network
* DoS - Aircrack的Wi-Fi DoS攻擊

#### Brute Force
* For system user:[John The Ripper](https://www.openwall.com/john/), [教學](https://ithelp.ithome.com.tw/articles/10300529)
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
* 生成字典: [Crunch](https://www.kali.org/tools/crunch/)
    ```bash
    # crunch <min_length> <max_length> [charset]
    $ crunch 4 4 # 生成所有 4 個字元的組合aaaa ~ zzzz
    $ crunch 4 4 abc # 可以指定可使用的字元 aaaa ~ cccc
    ```
* for WPA/Wifi based: [`aircrack-ng`](https://linuxhint.com/install_aircrack-ng_ubuntu/), [Wifite](https://ithelp.ithome.com.tw/articles/10280928)
* creddump: [教學]({{base.url}}/NTUSTISC-AD-Note-Lab(0x13Brute-Force-SAM)/)

### privilege escalation
* lateral movement
* data exfiltration
* For Windows: [Mimikatz](https://github.com/ParrotSec/mimikatz)


### Reporting
* 撰寫 pentest report
* remediation suggestion
* CaseFile
* dos2unix

## Forensics
### Disk Analysis
* [Foremost](https://darkranger.no-ip.org/archives/v5/document/linux/foremost_recovery.htm): 針對所支援的檔案結構去進行資料搜尋與救援
    ```bash
    $ foremost -v {filename}
    ```
* [Sleuth kit/Autopsy](https://blog.csdn.net/wxh0000mm/article/details/99447206)
* [FTK Imager](https://www.exterro.com/ftk-imager)
* [Logontracer]({{base.url}}/How-to-install-LogonTracer/): Just use GUI to present event log traced on windows
    ```bash
    $ python logontracer.py -r -o 8000 -u neo4j -p neo4j -s localhost
    ```

### Memory Forensics
* 建議直接使用[windown protable version](https://www.volatilityfoundation.org/releases)會比較穩定而且不需要處理環境的問題
* [Volatility - Cheat Sheet](https://hackmd.io/@TuX-/BymMpKd0s)
* [Volatility 3](https://github.com/volatilityfoundation/volatility3)
    
    Set up & How2Use
    * [Windows Volatility 3 Problems & Solutions](https://blog.csdn.net/u011250160/article/details/120461405)
    * [Windows Set up Tutorials](https://volatility3.readthedocs.io/en/latest/getting-started-windows-tutorial.html)
    
    ```bash
    $ git clone https://github.com/volatilityfoundation/volatility3
    $ cd volatility3
    $ pip install -r requirement.txt
    $ python vol.py -f <path to memory image> plugin_name plugin_option
    $ python vol.py -h # For help
    ```
    
* [Volatility 2](https://github.com/volatilityfoundation/volatility)
    
    Set up & How2Use
    [Windows Set up Tutorials](https://volatility3.readthedocs.io/en/latest/getting-started-windows-tutorial.html)
    ```bash
    $ conda create --name py27 python=2.7
    $ conda activate py27
    $ git clone https://github.com/volatilityfoundation/volatility
    $ cd volatility
    $ pip install pycrypto
    $ pip install distorm3
    $ python vol.py -f <path to memory image> plugin_name plugin_option
    $ python vol.py -h # For help
    ```






## 資安防禦平台與工具
### XDR
* [WAZUH](https://wazuh.com/)

### SIEM
* [splunk](https://www.splunk.com/)
* [ArcSight](https://www.microfocus.com/en-us/cyberres/secops/arcsight-esm)

### AD
* [Ping Castle](https://www.pingcastle.com/): 這個工具可以幫AD環境做快速的稽核，然後會產生報表，讓使用者可以一目了然目前AD的狀況

### Sysinternal
* [PsExec](https://learn.microsoft.com/zh-tw/sysinternals/downloads/psexec)
    > psexec是windows下非常好的一款遠程命令行工具。psexec的使用不需要對方主機開機3389端口，只需要對方開啟admin共享或c(該共享默認開啟，依賴於445端口)。但是，假如目標主機開啟了防火墻(因為防火墻默認禁止445端口的連接)，psexec也是不能使用的，會提示找不到網絡路徑。由於psexec是windows提供的工具，所以殺毒軟件會將其添加到白名單中。

## Reference
[^1]:Ravindran, U., & Potukuchi, R. V. (2022). A Review on Web Application Vulnerability Assessment and Penetration Testing. Review of Computer Engineering Studies, 9(1).
[^2]:[ul Hassan, S. Z., Muzaffar, Z., & Ahmad, S. Z. (2021). Operating Systems for Ethical Hackers-A Platform Comparison of Kali Linux and Parrot OS. International Journal, 10(3).](https://www.researchgate.net/profile/Syed-Zain-Ul-Hassan-2/publication/369305777_Operating_Systems_for_Ethical_Hackers_-_A_Platform_Comparison_of_Kali_Linux_and_Parrot_OS/links/6414544c315dfb4cce89b6a3/Operating-Systems-for-Ethical-Hackers-A-Platform-Comparison-of-Kali-Linux-and-Parrot-OS.pdf)