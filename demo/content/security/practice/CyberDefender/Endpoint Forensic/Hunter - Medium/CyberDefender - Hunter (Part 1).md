---
title: CyberDefender - Hunter (Part 1)
tags: [CyberDefender, Endpoint Forensics]

---

# CyberDefender - Hunter (Part 1)
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/32
Part 2: https://hackmd.io/@SBK6401/HJlmeuwfT
Part 3: https://hackmd.io/@SBK6401/HylP8ixQp

:::spoiler TOC
[TOC]
:::

## Scenario
> The SOC team got an alert regarding some illegal port scanning activity coming from an employee's system. The employee was not authorized to do any port scanning or any offensive hacking activity within the network. The employee claimed that he had no idea about that, and it is probably a malware acting on his behalf. The IR team managed to respond immediately and take a full forensic image of the user's system to perform some investigations.
>
>There is a theory that the user intentionally installed illegal applications to do port scanning and maybe other things. He was probably planning for something bigger, far beyond a port scanning!
>
>It all began when the user asked for a salary raise that was rejected. After that, his behavior was abnormal and different. The suspect is believed to have weak technical skills, and there might be an outsider helping him!
>
>Your objective as a soc analyst is to analyze the image and to either confirm or deny this theory.

## Tools
AccessData FTK Imager
Registry Explorer
## ==Q1==
> What is the computer name of the suspect machine? 
### Recon
首先看到題目給的檔案就知道他是用FTK Access Data輸出的檔案，所以先用FTK觀察裡面的一些資料
### Exploit
如果要知道電腦名稱，可以先從`/root/Windows/System32/config/`中找到`SYSTEM`這個檔案，它裡面紀錄了很多registry
![](https://hackmd.io/_uploads/H18pCZLGp.png)
其中有一個叫做computer name就紀錄本機器的名稱，先把該檔案export出來，再利用registry explorer看裡面的東西，就在`/ControlSet001/Control/ComputerName/ComputerName`
![](https://hackmd.io/_uploads/By_UkfLfa.png)
其實這個檔案就對應到自己電腦中的`電腦\HKEY_LOCAL_MACHINE\SYSTEM`這個檔案，也可以在依照原本的路徑找到自己電腦的名稱
![](https://hackmd.io/_uploads/SJLkWz8G6.png)

:::spoiler Flag
Flag: `4ORENSICS`
:::
## ==Q2==
> What is the computer IP?
### Exploit
在同樣的檔案也可以找到這個資訊，就在`\ControlSet001\Services\Tcpip\Parameters\Interfaces\`中可以看到這一題的答案是DhcpIPAddress=`10.0.2.15`
![](https://hackmd.io/_uploads/B10tmMIG6.png)
如果在自己的電腦看得話，也可以找到一樣的東西，不過數量有點多，是因為我有裝VMware/VirtualBox/WSL，而每一個都有自己對應的虛擬網卡，就會需要很多不同的機碼，可以搭配command的ipconfig
:::spoiler 和自己電腦做對照
![](https://hackmd.io/_uploads/ry6hNGUfp.png)

![](https://hackmd.io/_uploads/rk0ySMLzT.png)

![](https://hackmd.io/_uploads/HyPmBfLzT.png)

![](https://hackmd.io/_uploads/B1J2HzLza.png)

:::

:::spoiler Flag
Flag: `10.0.2.15`
:::
## ==Q3==
> What was the DHCP LeaseObtainedTime? 
### Recon
我們知道DHCP會固定一段時間就換掉來request的機器的IP，所以就會有"租約"的概念出現，當一台電腦像DHCP server請求一個IP，則除了會拿到一組動態IP之外，也會拿到一個租約開始與結束的時間，則下一次該機器向server請求時會判斷目前時間是不是在租約的範圍中，若不是就會換到下一個IP
### Exploit
也是在同樣的Hive file就可以看到相關的訊息，轉換的方式很簡單，可以直接用datatime這個library或是用[線上工具](https://www.unixtimestamp.com/)，參數就在`\ControlSet001\Services\Tcpip\Parameters\Interfaces\`
![](https://hackmd.io/_uploads/HkL6N7UG6.png)

```python
>>> time = 1466475852
>>> date_time = datetime.datetime.fromtimestamp(time)
>>> date_time.strftime('%d/%m/20%y ' + '{0:0>2d}'.format(int(date_time.strftime('%H')) - 8) + ':%M:%S' + ' UTC')
'21/06/2016 02:24:12 UTC'
>>> date_time = datetime.datetime.fromtimestamp(time)
>>> date_time.strftime('%d/%m/20%y ' + '{0:0>2d}'.format(int(date_time.strftime('%H')) - 8) + ':%M:%S' + ' UTC')
'22/06/2016 02:24:12 UTC'
```
可以看到租約開始的時間是6/21，而到期日是在6/22，
:::spoiler 和自己的電腦對照
```python
>>> time = 1698209088
>>> date_time = datetime.datetime.fromtimestamp(time)
>>> date_time.strftime('%d/%m/20%y ' + '{0:0>2d}'.format(int(date_time.strftime('%H')) - 8) + ':%M:%S' + ' UTC')
'25/10/2023 04:44:48 UTC'
>>> time = 1698295488
>>> date_time = datetime.datetime.fromtimestamp(time)
>>> date_time.strftime('%d/%m/20%y ' + '{0:0>2d}'.format(int(date_time.strftime('%H')) - 8) + ':%M:%S' + ' UTC')
'26/10/2023 04:44:48 UTC'
```
:::

:::spoiler Flag
Flag: `21/06/2016 02:24:12 UTC`
:::
## ==Q4==
> What is the computer SID? 
### Background
[深入了解安全性識別碼(SID Deep Dive)](https://www.lijyyh.com/2015/08/sid-deep-dive.html)
### Recon
可以先了解SID在幹嘛，然後這個基碼是儲存在`SOFTWARE`中，所以可以先dump出來
### Exploit
在`\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\`，同樣的，`SOFTWARE`也是對應到自己電腦的`電腦\HKEY_LOCAL_MACHINE\SOFTWARE`
![](https://hackmd.io/_uploads/ByJHnmUzp.png)

:::spoiler 和自己電腦做對照
利用psGetSid.exe這個微軟提供的工具可以知道自己這一台電腦(帳號)的SID為何
```bash
$ PsGetsid.exe

PsGetSid v1.46 - Translates SIDs to names and vice versa
Copyright (C) 1999-2023 Mark Russinovich
Sysinternals - www.sysinternals.com

SID for \\BERNIE-DESKTOP:
S-1-5-21-1994825736-962948173-1409654112
```
![](https://hackmd.io/_uploads/BkEihXIza.png)
:::

:::spoiler Flag
Flag: `S-1-5-21-2489440558-2754304563-710705792`
:::
## ==Q5==
> What is the Operating System(OS) version?
### Exploit
在`\SOFTWARE\Microsoft\Windows NT\CurrentVersion`中可以看到
![](https://hackmd.io/_uploads/HJTB0mLfT.png)

:::spoiler Flag
Flag: `8.1`
:::
## ==Q6==
> What was the computer timezone?
### Exploit
主要是在`\SYSTEM\ControlSet001\Control\TimeZoneInformation`中，可以看到他的時區是Pacific Standard Time，根據[時區換算](https://redbean101.pixnet.net/blog/post/36971406)的說明，有兩種轉換若有考慮夏令時間就是UTC-7，如果沒有就是UTC-8
![](https://hackmd.io/_uploads/B1Yf4NLGT.png)

:::spoiler 和自己的電腦照
![](https://hackmd.io/_uploads/HJQ2N4Lfp.png)
可以看到是Taipei Standard Time，也就是UTC+08:00
:::

:::spoiler Flag
Flag: `UTC-07:00`
:::
## ==Q7==
> How many times did this user log on to the computer? 
### Background
[二刀流Windows日誌分析　精準掌握資安蛛絲馬跡](https://www.netadmin.com.tw/netadmin/zh-tw/technology/84E5EAA4BC494BB6A4B15607E62418A0)

Event Log在`/root/Windows/System32/winevt/Logs/`中
![圖片.png](https://hackmd.io/_uploads/H1p5uJ4Q6.png)

### Recon
看到題目需要知道使用者操作，直覺會想到稽核的log紀錄，所以可以先把evtx檔案dump出來
### Exploit
原本想說要用logontracer，有美美的GUI好香，但實際用過之後不僅一大堆問題，包括安裝環境和內部source code的瑕疵，重點是還不給我parse，連正常運作都不給用，詳細安裝說明、遇到的問題以及為甚麼不給parse可以看我寫的[這一篇](https://hackmd.io/@SBK6401/SJOwGrUfa)，所以還是乖乖用內建的或是像[^hunter-wp]一樣先把evtx檔案用[EvtxECmd](https://ericzimmerman.github.io/#!index.md)轉成csv檔案再用[timeline explorer]()篩選各種event，不得不說，timeline explorer是真的好用，設定各種filter跟喝水一樣簡單

```bash
$ EvtxECmd.exe -f Security.evtx --csv out
```
用timeline explorer觀察一下整體的payload，會發現#text就是前面找到的SID，所以我們的filter自然就可以先設定Hunter這個username，然後我也不知道為啥，event ID的filter居然不是設定4624，而是設定4672，查了一下[MSDN](https://learn.microsoft.com/zh-tw/windows/security/threat-protection/auditing/event-4672)，看起來應該是一個具有更高權限的登入紀錄，不過我還是覺得這一題出的不好，因為如果只是單單看logon的次數，用4624也說得通
![](https://hackmd.io/_uploads/r1S1vpLzT.png)

:::spoiler Flag
Flag: `3`
:::
## ==Q8==
> When was the last login time for the discovered account? Format: one-space between date and time
### Exploit
呈上題
![](https://hackmd.io/_uploads/HkS4upIMa.png)

:::spoiler Flag
Flag: `2016-06-21 01:42:40`
:::
## ==Q9==
> There was a “Network Scanner” running on this computer, what was it? And when was the last time the suspect used it? Format: program.exe,YYYY-MM-DD HH:MM:SS UTC
### Recon
題目要求要找一個類似nmap之類的掃port的工具，然後還要看最後一次使用的時間，所以要先找到該軟體再哪裡，思路應該是既然他有使用過就一定會有prefetch，所以可以從裡面撈點東西出來這樣，位置就在`\root\Windows\Prefetch`
### Exploit
首先從這一大堆的prefetch中看有哪一個工具很可疑，發現zenmap.exe的pf感覺有點熟悉，[查了一下](https://blog.csdn.net/wkl_venus/article/details/109491200)，原來是nmap的近親(有視覺化功能)，看起來就是他了，接著又是使用新工具的時候，到[這邊](https://ericzimmerman.github.io/#!index.md)載PECmd，(Eric Zimmerman很屌耶，甚麼工具都有做)，下command就會出現Last run的時間了
```bash
$ PECmd.exe -f ZENMAP.EXE-56B17C4C.pf
PECmd version 1.5.0.0

Author: Eric Zimmerman (saericzimmerman@gmail.com)
https://github.com/EricZimmerman/PECmd

Command line: -f ZENMAP.EXE-56B17C4C.pf --csv output

Warning: Administrator privileges not found!

Keywords: temp, tmp

Processing ZENMAP.EXE-56B17C4C.pf

Created on: 2023-10-25 17:04:39
Modified on: 2016-06-21 12:08:21
Last accessed on: 2023-10-25 17:05:58

Executable name: ZENMAP.EXE
Hash: 56B17C4C
File size (bytes): 93,524
Version: Windows 8.0, Windows 8.1, or Windows Server 2012(R2)

Run count: 1
Last run: 2016-06-21 12:08:13

Volume information:
...
```

:::spoiler Flag
Flag: `zenmap.exe,2016-06-21 12:08:13 UTC`
:::
## ==Q10==
> When did the port scan end? (Example: Sat Jan 23 hh:mm:ss 2016) 
### Recon
如果有用過nmap這種工具應該會有一個log file或是最後結果的report，所以直覺應該是找到個這file，但...我不知道去哪裡找，所以求助大神的WP[^hunter-wp-2]
在上一題的結果中，我們會發現一些可疑的資料夾或是檔案，例如:
```
24: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\.ZENMAP
93: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\.ZENMAP\SCAN_PROFILE.USP
95: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\.ZENMAP\ZENMAP.CONF
97: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\.ZENMAP\ZENMAP_VERSION
```
其他可能有一些原因導致資料遺失，所以感覺上這個路徑會有一些資訊可以撈
![](https://hackmd.io/_uploads/BJMH0DDMT.png)
大概看過一遍之後發現他的target是`scanme.nmap.org`，結果的路徑會放在`recent_scans.txt`中$\to$`C:\Users\Hunter\Desktop\nmapscan.xml`，實際去翻了一下發現真的有一些重要資訊
### Exploit
:::spoiler xml檔案內容
```xml
<?xml version="1.0" encoding="iso-8859-1"?>
<?xml-stylesheet href="file:///C:/Program Files (x86)/Nmap/nmap.xsl" type="text/xsl"?><nmaprun start="1466511043" profile_name="" xmloutputversion="1.04" scanner="nmap" version="7.12" startstr="Tue Jun 21 05:10:43 2016" args="nmap -T4 -A -v scanme.nmap.org"><scaninfo services="1,3-4,6-7,9,13,17,19-26,30,32-33,37,42-43,49,53,70,79-85,88-90,99-100,106,109-111,113,119,125,135,139,143-144,146,161,163,179,199,211-212,222,254-256,259,264,280,301,306,311,340,366,389,406-407,416-417,425,427,443-445,458,464-465,481,497,500,512-515,524,541,543-545,548,554-555,563,587,593,616-617,625,631,636,646,648,666-668,683,687,691,700,705,711,714,720,722,726,749,765,777,783,787,800-801,808,843,873,880,888,898,900-903,911-912,981,987,990,992-993,995,999-1002,1007,1009-1011,1021-1100,1102,1104-1108,1110-1114,1117,1119,1121-1124,1126,1130-1132,1137-1138,1141,1145,1147-1149,1151-1152,1154,1163-1166,1169,1174-1175,1183,1185-1187,1192,1198-1199,1201,1213,1216-1218,1233-1234,1236,1244,1247-1248,1259,1271-1272,1277,1287,1296,1300-1301,1309-1311,1322,1328,1334,1352,1417,1433-1434,1443,1455,1461,1494,1500-1501,1503,1521,1524,1533,1556,1580,1583,1594,1600,1641,1658,1666,1687-1688,1700,1717-1721,1723,1755,1761,1782-1783,1801,1805,1812,1839-1840,1862-1864,1875,1900,1914,1935,1947,1971-1972,1974,1984,1998-2010,2013,2020-2022,2030,2033-2035,2038,2040-2043,2045-2049,2065,2068,2099-2100,2103,2105-2107,2111,2119,2121,2126,2135,2144,2160-2161,2170,2179,2190-2191,2196,2200,2222,2251,2260,2288,2301,2323,2366,2381-2383,2393-2394,2399,2401,2492,2500,2522,2525,2557,2601-2602,2604-2605,2607-2608,2638,2701-2702,2710,2717-2718,2725,2800,2809,2811,2869,2875,2909-2910,2920,2967-2968,2998,3000-3001,3003,3005-3007,3011,3013,3017,3030-3031,3052,3071,3077,3128,3168,3211,3221,3260-3261,3268-3269,3283,3300-3301,3306,3322-3325,3333,3351,3367,3369-3372,3389-3390,3404,3476,3493,3517,3527,3546,3551,3580,3659,3689-3690,3703,3737,3766,3784,3800-3801,3809,3814,3826-3828,3851,3869,3871,3878,3880,3889,3905,3914,3918,3920,3945,3971,3986,3995,3998,4000-4006,4045,4111,4125-4126,4129,4224,4242,4279,4321,4343,4443-4446,4449,4550,4567,4662,4848,4899-4900,4998,5000-5004,5009,5030,5033,5050-5051,5054,5060-5061,5080,5087,5100-5102,5120,5190,5200,5214,5221-5222,5225-5226,5269,5280,5298,5357,5405,5414,5431-5432,5440,5500,5510,5544,5550,5555,5560,5566,5631,5633,5666,5678-5679,5718,5730,5800-5802,5810-5811,5815,5822,5825,5850,5859,5862,5877,5900-5904,5906-5907,5910-5911,5915,5922,5925,5950,5952,5959-5963,5987-5989,5998-6007,6009,6025,6059,6100-6101,6106,6112,6123,6129,6156,6346,6389,6502,6510,6543,6547,6565-6567,6580,6646,6666-6669,6689,6692,6699,6779,6788-6789,6792,6839,6881,6901,6969,7000-7002,7004,7007,7019,7025,7070,7100,7103,7106,7200-7201,7402,7435,7443,7496,7512,7625,7627,7676,7741,7777-7778,7800,7911,7920-7921,7937-7938,7999-8002,8007-8011,8021-8022,8031,8042,8045,8080-8090,8093,8099-8100,8180-8181,8192-8194,8200,8222,8254,8290-8292,8300,8333,8383,8400,8402,8443,8500,8600,8649,8651-8652,8654,8701,8800,8873,8888,8899,8994,9000-9003,9009-9011,9040,9050,9071,9080-9081,9090-9091,9099-9103,9110-9111,9200,9207,9220,9290,9415,9418,9485,9500,9502-9503,9535,9575,9593-9595,9618,9666,9876-9878,9898,9900,9917,9929,9943-9944,9968,9998-10004,10009-10010,10012,10024-10025,10082,10180,10215,10243,10566,10616-10617,10621,10626,10628-10629,10778,11110-11111,11967,12000,12174,12265,12345,13456,13722,13782-13783,14000,14238,14441-14442,15000,15002-15004,15660,15742,16000-16001,16012,16016,16018,16080,16113,16992-16993,17877,17988,18040,18101,18988,19101,19283,19315,19350,19780,19801,19842,20000,20005,20031,20221-20222,20828,21571,22939,23502,24444,24800,25734-25735,26214,27000,27352-27353,27355-27356,27715,28201,30000,30718,30951,31038,31337,32768-32785,33354,33899,34571-34573,35500,38292,40193,40911,41511,42510,44176,44442-44443,44501,45100,48080,49152-49161,49163,49165,49167,49175-49176,49400,49999-50003,50006,50300,50389,50500,50636,50800,51103,51493,52673,52822,52848,52869,54045,54328,55055-55056,55555,55600,56737-56738,57294,57797,58080,60020,60443,61532,61900,62078,63331,64623,64680,65000,65129,65389" protocol="tcp" numservices="1000" type="syn"></scaninfo><verbose level="1"></verbose><debugging level="0"></debugging><output type="interactive">

Starting Nmap 7.12 ( https://nmap.org ) at 2016-06-21 05:10 Pacific Daylight Time

NSE: Loaded 138 scripts for scanning.

NSE: Script Pre-scanning.

Initiating NSE at 05:10

Completed NSE at 05:10, 0.08s elapsed

Initiating NSE at 05:10

Completed NSE at 05:10, 0.01s elapsed

Initiating Ping Scan at 05:10

Scanning scanme.nmap.org (45.33.32.156) [4 ports]

Completed Ping Scan at 05:10, 0.05s elapsed (1 total hosts)

Initiating Parallel DNS resolution of 1 host. at 05:10

Completed Parallel DNS resolution of 1 host. at 05:10, 0.22s elapsed

Initiating SYN Stealth Scan at 05:10

Scanning scanme.nmap.org (45.33.32.156) [1000 ports]

Discovered open port 80/tcp on 45.33.32.156

Discovered open port 22/tcp on 45.33.32.156

Discovered open port 9929/tcp on 45.33.32.156

Discovered open port 31337/tcp on 45.33.32.156

Completed SYN Stealth Scan at 05:11, 12.69s elapsed (1000 total ports)

Initiating Service scan at 05:11

Scanning 4 services on scanme.nmap.org (45.33.32.156)

Completed Service scan at 05:11, 28.99s elapsed (4 services on 1 host)

Initiating OS detection (try #1) against scanme.nmap.org (45.33.32.156)

Retrying OS detection (try #2) against scanme.nmap.org (45.33.32.156)

Retrying OS detection (try #3) against scanme.nmap.org (45.33.32.156)

Retrying OS detection (try #4) against scanme.nmap.org (45.33.32.156)

Retrying OS detection (try #5) against scanme.nmap.org (45.33.32.156)

Initiating Traceroute at 05:11

Completed Traceroute at 05:11, 0.01s elapsed

Initiating Parallel DNS resolution of 2 hosts. at 05:11

Completed Parallel DNS resolution of 2 hosts. at 05:12, 13.00s elapsed

NSE: Script scanning 45.33.32.156.

Initiating NSE at 05:12

Completed NSE at 05:12, 4.75s elapsed

Initiating NSE at 05:12

Completed NSE at 05:12, 0.00s elapsed

Nmap scan report for scanme.nmap.org (45.33.32.156)

Host is up (0.011s latency).

Not shown: 994 closed ports

PORT      STATE    SERVICE       VERSION

22/tcp    open     ssh           OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.7 (Ubuntu Linux; protocol 2.0)

| ssh-hostkey: 

|   1024 ac:00:a0:1a:82:ff:cc:55:99:dc:67:2b:34:97:6b:75 (DSA)

|_  256 96:02:bb:5e:57:54:1c:4e:45:2f:56:4c:4a:24:b2:57 (ECDSA)

25/tcp    filtered smtp

26/tcp    filtered rsftp

80/tcp    open     http          Apache httpd 2.4.7 ((Ubuntu))

|_http-favicon: Unknown favicon MD5: 156515DA3C0F7DC6B2493BD5CE43F795

| http-methods: 

|_  Supported Methods: POST OPTIONS GET HEAD

|_http-server-header: Apache/2.4.7 (Ubuntu)

|_http-title: Go ahead and ScanMe!

9929/tcp  open     nping-echo    Nping echo

31337/tcp open     ssl/ncat-chat Ncat chat (users: nobody)

| ssl-cert: Subject: commonName=localhost

| Issuer: commonName=localhost

| Public Key type: rsa

| Public Key bits: 1024

| Signature Algorithm: sha1WithRSAEncryption

| Not valid before: 2016-06-21T04:01:25

| Not valid after:  2017-06-21T04:01:25

| MD5:   d99f 9f02 30cf 3c59 1758 f83d bb2d b1a9

|_SHA-1: 1543 c4be b900 b059 998e 692f cf70 12f5 cf91 eda1

|_ssl-date: TLS randomness does not represent time

No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).

TCP/IP fingerprint:

OS:SCAN(V=7.12%E=4%D=6/21%OT=22%CT=1%CU=37741%PV=N%DS=2%DC=T%G=Y%TM=57692F1

OS:9%P=i686-pc-windows-windows)SEQ(SP=14%GCD=FA00%ISR=9D%TI=I%CI=RD%TS=U)SE

OS:Q(SP=12%GCD=FA00%ISR=9C%CI=RD%TS=U)OPS(O1=M5B4%O2=M5B4%O3=M5B4%O4=M5B4%O

OS:5=M5B4%O6=M5B4)WIN(W1=FFFF%W2=FFFF%W3=FFFF%W4=FFFF%W5=FFFF%W6=FFFF)ECN(R

OS:=Y%DF=N%T=41%W=FFFF%O=M5B4%CC=N%Q=)ECN(R=N)T1(R=Y%DF=N%T=41%S=O%A=S+%F=A

OS:S%RD=0%Q=)T2(R=Y%DF=N%T=100%W=0%S=Z%A=S%F=AR%O=%RD=0%Q=)T3(R=Y%DF=N%T=10

OS:0%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T4(R=Y%DF=N%T=100%W=0%S=A%A=Z%F=R%O=%RD=0

OS:%Q=)T5(R=Y%DF=N%T=100%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=N%T=100%W=0

OS:%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=N%T=100%W=0%S=Z%A=S%F=AR%O=%RD=0%Q=)U1

OS:(R=Y%DF=N%T=34%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=N)



Network Distance: 2 hops

Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel



TRACEROUTE (using port 80/tcp)

HOP RTT     ADDRESS

1   1.00 ms 10.0.2.2

2   1.00 ms scanme.nmap.org (45.33.32.156)



NSE: Script Post-scanning.

Initiating NSE at 05:12

Completed NSE at 05:12, 0.00s elapsed

Initiating NSE at 05:12

Completed NSE at 05:12, 0.00s elapsed

Read data files from: C:\Program Files (x86)\Nmap

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .

Nmap done: 1 IP address (1 host up) scanned in 87.13 seconds

           Raw packets sent: 1331 (66.198KB) | Rcvd: 1445 (64.387KB)

</output><host comment=""><status state="up"></status><address addrtype="ipv4" vendor="" addr="45.33.32.156"></address><hostnames><hostname type="user" name="scanme.nmap.org"></hostname><hostname type="PTR" name="scanme.nmap.org"></hostname></hostnames><ports><extraports count="994" state="closed"></extraports><port protocol="tcp" portid="22"><state reason="syn-ack" state="open" reason_ttl="64"></state><service product="OpenSSH" name="ssh" extrainfo="Ubuntu Linux; protocol 2.0" version="6.6.1p1 Ubuntu 2ubuntu2.7" conf="10" method="probed"></service></port><port protocol="tcp" portid="25"><state reason="no-response" state="filtered" reason_ttl="0"></state><service method="table" conf="3" name="smtp"></service></port><port protocol="tcp" portid="26"><state reason="no-response" state="filtered" reason_ttl="0"></state><service method="table" conf="3" name="rsftp"></service></port><port protocol="tcp" portid="80"><state reason="syn-ack" state="open" reason_ttl="64"></state><service product="Apache httpd" name="http" extrainfo="(Ubuntu)" version="2.4.7" conf="10" method="probed"></service></port><port protocol="tcp" portid="9929"><state reason="syn-ack" state="open" reason_ttl="64"></state><service product="Nping echo" method="probed" conf="10" name="nping-echo"></service></port><port protocol="tcp" portid="31337"><state reason="syn-ack" state="open" reason_ttl="64"></state><service product="Ncat chat" extrainfo="users: nobody" method="probed" conf="10" name="ncat-chat"></service></port></ports><os><portused state="open" portid="22" proto="tcp"></portused><portused state="closed" portid="1" proto="tcp"></portused><portused state="closed" portid="37741" proto="udp"></portused><osmatch line="84526" name="QEMU user mode network gateway" accuracy="96"><osclass type="general purpose" osfamily="QEMU" vendor="QEMU" osgen="" accuracy="96"></osclass></osmatch><osmatch line="27173" name="GNU Hurd 0.3" accuracy="87"><osclass type="general purpose" osfamily="Hurd" vendor="GNU" osgen="" accuracy="87"></osclass></osmatch><osmatch line="2383" name="Allied Telesyn AT-9006SX/SC switch" accuracy="87"><osclass type="switch" osfamily="embedded" vendor="Allied Telesyn" osgen="" accuracy="87"></osclass></osmatch><osmatch line="8655" name="Bay Networks BayStack 450 switch (software version 3.1.0.22)" accuracy="87"><osclass type="switch" osfamily="embedded" vendor="Bay Networks" osgen="" accuracy="87"></osclass></osmatch><osmatch line="8673" name="Bay Networks BayStack 450 switch (software version 4.2.0.16)" accuracy="87"><osclass type="switch" osfamily="embedded" vendor="Bay Networks" osgen="" accuracy="87"></osclass></osmatch><osmatch line="11315" name="Cabletron ELS100-24TXM Switch or Icom IC-7800 radio transceiver" accuracy="87"><osclass type="specialized" osfamily="embedded" vendor="Icom" osgen="" accuracy="87"></osclass></osmatch><osmatch line="13078" name="Cisco Catalyst 1900 switch or RAD IPMUX-1 TDM-over-IP multiplexer" accuracy="87"><osclass type="switch" osfamily="embedded" vendor="RAD Data Communications" osgen="" accuracy="87"></osclass></osmatch><osmatch line="82858" name="Oracle Virtualbox" accuracy="87"><osclass type="bridge" osfamily="Virtualbox" vendor="Oracle" osgen="" accuracy="87"></osclass></osmatch><osmatch line="40192" name="TiVo series 1 (Sony SVR-2000 or Philips HDR112) (Linux 2.1.24-TiVo-2.5, PowerPC)" accuracy="86"><osclass type="media device" osfamily="embedded" vendor="Sony" osgen="" accuracy="86"></osclass></osmatch><osmatch line="37456" name="Konica Minolta 7035 printer" accuracy="86"><osclass type="printer" osfamily="embedded" vendor="Konica Minolta" osgen="" accuracy="86"></osclass></osmatch></os><uptime lastboot="" seconds=""></uptime><tcpsequence index="" values="" difficulty=""></tcpsequence><ipidsequence values="" class=""></ipidsequence><tcptssequence values="" class=""></tcptssequence><trace port="80" proto="tcp"><hop rtt="1.00" host="" ipaddr="10.0.2.2" ttl="1"></hop><hop rtt="1.00" host="scanme.nmap.org" ipaddr="45.33.32.156" ttl="2"></hop></trace></host><runstats><finished timestr="Tue Jun 21 05:12:09 2016" time="1466511129"></finished><hosts down="0" total="1" up="1"></hosts></runstats></nmaprun>
```
:::
如果覺得太冗又很難看可以丟到[online xml parser](https://jsonformatter.org/xml-parser)
就會看到結束的時間
![](https://hackmd.io/_uploads/HkDbldPfT.png)


:::spoiler Flag
Flag: `Tue Jun 21 05:12:09 2016`
:::
## Reference
[第二章、簡易網路基礎架構](https://linux.vbird.org/linux_server/redhat9/0110network_basic.php)
[第十六章、簡易 DHCP 伺服器設定](https://linux.vbird.org/linux_server/redhat9/0340dhcp.php#theory_Whatisdhcp)
[^hunter-wp]:[ Cyberdefenders.org Hunter Walkthrough ](https://youtu.be/0P0DTXiG9qE?si=PLyJ2Y9gvrt9ZePo)
[^hunter-wp-2]:[Cyberdefenders.org Hunter Walkthrough](https://medium.com/@cyberforensicator57/cyberdefenders-org-hunter-walkthrough-65c0c6cb8e87)