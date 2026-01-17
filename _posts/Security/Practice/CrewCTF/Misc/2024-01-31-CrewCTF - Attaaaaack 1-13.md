---
title: CrewCTF - Attaaaaack 1-13
tags: [CTF, CrewCTF, Misc]

category: "Security｜Practice｜CrewCTF｜Misc"
date: 2024-01-31
---

# CrewCTF - Attaaaaack 1-13
<!-- more -->
:::spoiler TOC
[TOC]
:::

One of our employees at the company complained about suspicious behavior on the machine, our IR team took a memory dump from the machine and we need to investigate it.

## ==Attaaaaack 1==
> Q1. What is the best profile for the the machine?

### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memdump.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (D:\NTU\CTF\CrewCTF\Misc\Attaaaaack\memdump.raw)
                      PAE type : PAE
                           DTB : 0x185000L
                          KDBG : 0x82b7ab78L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0x80b96000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2023-02-20 19:10:54 UTC+0000
     Image local date and time : 2023-02-20 21:10:54 +0200
```

Flag: `crew{Win7SP1x86_23418}`

## ==Attaaaaack 2==
> Q2. How many processes were running ? (number)

### Exploit
:::spoiler Command Result
```bash
$ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x8419c020 System                    4      0     89      536 ------      0 2023-02-20 19:01:19 UTC+0000
0x962f2020 smss.exe                268      4      2       29 ------      0 2023-02-20 19:01:19 UTC+0000
0x860a8c78 csrss.exe               352    344      9      462      0      0 2023-02-20 19:01:20 UTC+0000
0x855dfd20 wininit.exe             404    344      3       76      0      0 2023-02-20 19:01:20 UTC+0000
0x8550b030 csrss.exe               416    396      9      268      1      0 2023-02-20 19:01:20 UTC+0000
0x85ea2368 services.exe            480    404      8      220      0      0 2023-02-20 19:01:20 UTC+0000
0x85ea8610 lsass.exe               488    404      6      568      0      0 2023-02-20 19:01:20 UTC+0000
0x85eab718 lsm.exe                 496    404     10      151      0      0 2023-02-20 19:01:20 UTC+0000
0x85eacb80 winlogon.exe            508    396      5      115      1      0 2023-02-20 19:01:20 UTC+0000
0x85f4d030 svchost.exe             632    480     10      357      0      0 2023-02-20 19:01:21 UTC+0000
0x85ef0a90 svchost.exe             700    480      8      280      0      0 2023-02-20 19:01:21 UTC+0000
0x919e2958 svchost.exe             752    480     22      507      0      0 2023-02-20 19:01:21 UTC+0000
0x85f9c3a8 svchost.exe             868    480     13      309      0      0 2023-02-20 19:01:21 UTC+0000
0x85fae030 svchost.exe             908    480     18      715      0      0 2023-02-20 19:01:21 UTC+0000
0x85fb7670 svchost.exe             952    480     34      995      0      0 2023-02-20 19:01:22 UTC+0000
0x85ff1380 svchost.exe            1104    480     18      391      0      0 2023-02-20 19:01:22 UTC+0000
0x8603a030 spoolsv.exe            1236    480     13      270      0      0 2023-02-20 19:01:22 UTC+0000
0x86071818 svchost.exe            1280    480     19      312      0      0 2023-02-20 19:01:22 UTC+0000
0x860b73c8 svchost.exe            1420    480     10      146      0      0 2023-02-20 19:01:22 UTC+0000
0x860ba030 taskhost.exe           1428    480      9      205      1      0 2023-02-20 19:01:22 UTC+0000
0x861321c8 dwm.exe                1576    868      5      114      1      0 2023-02-20 19:01:23 UTC+0000
0x8613c030 explorer.exe           1596   1540     29      842      1      0 2023-02-20 19:01:23 UTC+0000
0x841d7500 VGAuthService.         1636    480      3       84      0      0 2023-02-20 19:01:23 UTC+0000
0x86189d20 vmtoolsd.exe           1736   1596      8      179      1      0 2023-02-20 19:01:23 UTC+0000
0x8619dd20 vm3dservice.ex         1848    480      4       60      0      0 2023-02-20 19:01:24 UTC+0000
0x861a9030 vmtoolsd.exe           1884    480     13      290      0      0 2023-02-20 19:01:24 UTC+0000
0x861b5360 vm3dservice.ex         1908   1848      2       44      1      0 2023-02-20 19:01:24 UTC+0000
0x861fc700 svchost.exe             580    480      6       91      0      0 2023-02-20 19:01:25 UTC+0000
0x86261030 WmiPrvSE.exe           1748    632     10      204      0      0 2023-02-20 19:01:25 UTC+0000
0x86251bf0 dllhost.exe             400    480     15      196      0      0 2023-02-20 19:01:26 UTC+0000
0x8629e518 msdtc.exe              2168    480     14      158      0      0 2023-02-20 19:01:31 UTC+0000
0x8629e188 SearchIndexer.         2276    480     12      581      0      0 2023-02-20 19:01:31 UTC+0000
0x8630b228 wmpnetwk.exe           2404    480      9      212      0      0 2023-02-20 19:01:32 UTC+0000
0x862cca38 svchost.exe            2576    480     15      232      0      0 2023-02-20 19:01:33 UTC+0000
0x85351030 WmiPrvSE.exe           3020    632     11      242      0      0 2023-02-20 19:01:45 UTC+0000
0x853faac8 ProcessHacker.         3236   1596      9      416      1      0 2023-02-20 19:02:37 UTC+0000
0x843068f8 sppsvc.exe             2248    480      4      146      0      0 2023-02-20 19:03:25 UTC+0000
0x85f89640 svchost.exe            2476    480     13      369      0      0 2023-02-20 19:03:25 UTC+0000
0x843658d0 cmd.exe                2112   2876      1       20      1      0 2023-02-20 19:03:40 UTC+0000
0x84368798 cmd.exe                2928   2876      1       20      1      0 2023-02-20 19:03:40 UTC+0000
0x84365c90 conhost.exe            1952    416      2       49      1      0 2023-02-20 19:03:40 UTC+0000
0x84384d20 conhost.exe            2924    416      2       49      1      0 2023-02-20 19:03:40 UTC+0000
0x84398998 runddl32.exe            300   2876     10     2314      1      0 2023-02-20 19:03:40 UTC+0000
0x84390030 notepad.exe            2556    300      2       58      1      0 2023-02-20 19:03:41 UTC+0000
0x84df2458 audiodg.exe            1556    752      6      129      0      0 2023-02-20 19:10:50 UTC+0000
0x84f1caf8 DumpIt.exe             2724   1596      2       38      1      0 2023-02-20 19:10:52 UTC+0000
0x84f3d878 conhost.exe            3664    416      2       51      1      0 2023-02-20 19:10:52 UTC+0000
```
:::

Flag: `47`

## ==Attaaaaack 3==
> Q3. i think the user left note on the machine. can you find it ?

### Recon
這一題真的要通靈，看到note第一直覺應該是想到要看有沒有類似notepad這樣的文字編輯器，果不其然pslist有這個process，所以可以把該process的memory dump出來，然後strings search再grep特定的regular expression，不過這邊有一個需要通靈的地方，就是通靈regular expression的形式，還必須要注意strings的形式是16 bits和little endian的形式才找的到，上述方法是參考[^crewctf-attaaaaack3-wp]，另外一個方法是可以通靈到作者有可能會把字串暫存在clipboard上，這樣就可以搭配clipboard這個plugin，可以直接print出clipboard中的內容

### Exploit
* 方法一
    ```bash
    $ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 clipboard
    Volatility Foundation Volatility Framework 2.6
    Session    WindowStation Format                 Handle Object     Data
    ---------- ------------- ------------------ ---------- ---------- --------------------------------------------------
             1 WinSta0       CF_UNICODETEXT        0xa00d9 0xfe897838 1_l0v3_M3m0ry_F0r3ns1cs_S0_muchhhhhhhhh
             1 WinSta0       0x0L                     0x10 ----------
             1 WinSta0       0x2000L                   0x0 ----------
             1 WinSta0       0x0L                   0x3000 ----------
             1 ------------- ------------------   0x1a02a9 0xfe670a68
             1 ------------- ------------------   0x100067 0xffbab448
    ```
* 方法二
    ```bash
    $ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 pslist | findstr notepad
    Volatility Foundation Volatility Framework 2.6
    0x84390030 notepad.exe            2556    300      2       58      1      0 2023-02-20 19:03:41 UTC+0000
    $ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 memdump --pid 2556 -D .\output
    $ strings -el 2556.dmp | grep -E "(.*?)_(.*?)_"
    ...
    _040515AD&REV_00
    PCI\VEN_15AD&DEV_0405&SUBSYS_040515AD&REV_TERMINAL
    CI\VEN_15AD&DEV_0405&CC_0300
    DEV_0405&CC_030000
    PCI\VEN_15AD&DEV_0405&CC_0300
    1_l0v3_M3m0ry_F0r3ns1cs_S0_muchhhhhhhhh
    EN_15AD&DEV_0405&CC_0300
    \??\HID#VID_0E0F&PID_0003&MI_00#8&167f267&0&0000#{378de44c-56ef-11d1-bc8c-00a0c91405dd}
    \??\IDE#CdRomNECVMWar_VMware_SATA_CD01_______________1.00____#6&22d3c06&0&1.0.0#{53f56308-b6bf-11d0-94f2-00a0c91efb8b}
    \??\HID#VID_0E0F&PID_0003&MI_01#8&226f4b5b&0&0000#{378de44c-56ef-11d1-bc8c-00a0c91405dd}
    ```

Flag: `crew{1_l0v3_M3m0ry_F0r3ns1cs_S0_muchhhhhhhhh}`

## ==Attaaaaack 4==
> Q4. What is the name and PID of the suspicious process ?
> example : crew{abcd.exe_111}

### Recon
因為是賽後解，所以其實...如果是線上解的話可以try&error，反正這一題也是頗單純，如果觀察pslist的process，會發現有一個runddl32.exe他就是在模仿rundll32，所以這就是一個怪可疑的process

### Exploit
Flag: `crew{runddl32.exe_300}`

## ==Attaaaaack 5==
> Q5. What is the another process that is related to this process and it's strange ?
> example : crew{spotify.exe}

### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
...
0x84398998 runddl32.exe            300   2876     10     2314      1      0 2023-02-20 19:03:40 UTC+0000
0x84390030 notepad.exe            2556    300      2       58      1      0 2023-02-20 19:03:41 UTC+0000
...
```

Flag: `crew{notepad.exe}`

## ==Attaaaaack 6==
> Q6. What is the full path (including executable name) of the hidden executable?
example : crew{C:\Windows\System32\abc.exe}

### Recon
這一題指的是runddl32.exe在哪邊，就直接filescan然後string search就找到了

### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 filescan | findstr runddl32.exe
Volatility Foundation Volatility Framework 2.6
0x0000000024534f80      5      0 R--r-d \Device\HarddiskVolume1\Users\0XSH3R~1\AppData\Local\Temp\MSDCSC\runddl32.exe
0x000000003ea44038      8      0 RWD--- \Device\HarddiskVolume1\Users\0XSH3R~1\AppData\Local\Temp\MSDCSC\runddl32.exe
```

Flag: `crew{C:\Users\0XSH3R~1\AppData\Local\Temp\MSDCSC\runddl32.exe}`

## ==Attaaaaack 7==
> Q7. What is the API used by the malware to retrieve the status of a specified virtual key on the keyboard ?
flag format: crew{AbcDef}

### Recon
仔細分析題目的話，會知道他要我們找出malware使用哪個API(method/function)取得keyboard上的虛擬按鍵，所以直覺的做法是直接把該執行檔dump出來，然後string search這隻檔案有哪些和key相關的東西

### Exploit
如果把該支malware丟到virustotal後，結果可以看[這邊](https://www.virustotal.com/gui/file/25aaa2657e649d8976cb321a6bf63eb56e8451ebde550003ef98782dd1b5ae62)
```bash
$ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 procdump --pid 300 -D .\output
Volatility Foundation Volatility Framework 2.6
Process(V) ImageBase  Name                 Result
---------- ---------- -------------------- ------
0x84398998 0x00400000 runddl32.exe         OK: executable.300.exe
$ strings executable.300.exe | grep -i key
AutoHotkeysd-C
AutoHotkeys
AutoHotkeys
TWMKey
System\CurrentControlSet\Control\Keyboard Layouts\%.8x
        TKeyEvent
TKeyPressEvent
HelpKeyword nA
80211_SHARED_KEY
KEYNAME
KEYNAME
KEYNAME
KEYNAME
RegOpenKeyExA
RegCloseKey
GetKeyboardType
keybd_event
VkKeyScanA
MapVirtualKeyA
LoadKeyboardLayoutA
GetKeyboardState
GetKeyboardLayoutNameA
GetKeyboardLayoutList
GetKeyboardLayout
GetKeyState
GetKeyNameTextA
ActivateKeyboardLayout
RegQueryInfoKeyA
RegOpenKeyExA
RegOpenKeyA
RegFlushKey
RegEnumKeyExA
RegDeleteKeyA
RegCreateKeyExA
RegCreateKeyA
RegCloseKey
UntKeylogger
UntControlKey
```
一個一個try就可以了

Flag: `crew{GetKeyState}`

## ==Attaaaaack 8==
> Q8. What is the Attacker's C2 domain name and port number ? (domain name:port number)
example : crew{abcd.com:8080}

### Background
[CyberDefender - MrRobot - POS - Q21](https://hackmd.io/@SBK6401/B1LqaNGCh/https%3A%2F%2Fhackmd.io%2F%40SBK6401%2FBJpJqDhlp#Q21)

### Recon
這一題直覺會想用netscan，畢竟從前面的題目以及找到的資訊，還有virustotal上的資訊，幾乎確定他就是一個keylogger，然後會把得到的資訊傳回去C&C server中，但奇怪的是察看netscan沒有相關的connection，不確定到底是怎麼樣，找了很久，最後是參考[siunam321](https://siunam321.github.io/ctf/CrewCTF-2023/Forensics/Attaaaaack1-13/#attaaaaack8)的writeup，他也是找了很久，結果其實virustotal都已經寫好了，

### Exploit
![](https://hackmd.io/_uploads/S1-f44e-p.png)
在Behavior的地方

Flag: `crew{test213.no-ip.info:1604}`

## ==Attaaaaack 9==
> Q9. Seems that there is Keylogger, can you find it's path ?
example : crew{C:\Windows\System32\abc.def}

### Background

### Recon
這一題完全不會，所以看了[siunam321](https://siunam321.github.io/ctf/CrewCTF-2023/Forensics/Attaaaaack1-13/#attaaaaack9)的writeup，他的做法是到網路上找有沒有`test213.no-ip.info keylogger`的相關文章，結果[TekDefense](http://www.tekdefense.com/news/2013/12/23/analyzing-darkcomet-in-memory.html)就有提到這隻malware
> The OFFLINEK option had me confused for a bit. So to explain it a bit better, when OFFLINEK is enabled “{1}” the malware will continue to log keystroke to a local file that can then be picked up by the attacker as they want. When disabled, the attacker only has access to keystrokes when the attacker has a live session open with the victim.

簡單來說就是他有一個參數(OFFLINEK)，如果被設定為1，則在離線的時候還是會繼續記錄，然後把結果存在local file，這也回應了前面位甚麼用netscan找不到的原因，因為作者沒有連線，所以當然不會有相關的process，而該bloger也找到了他存在local端的地方就在
`C:\Users\{Username}\AppData\Roaming\dclogs\{timestamp}.dc`
![](https://hackmd.io/_uploads/SyycDNx-6.png)

### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 filescan | findstr .dc | findstr \AppData\Roaming\dclogs
Volatility Foundation Volatility Framework 2.6
0x000000003fcb3350      8      0 -W-r-- \Device\HarddiskVolume1\Users\0xSh3rl0ck\AppData\Roaming\dclogs\2023-02-20-2.dc
```

Flag: `crew{C:\Users\0xSh3rl0ck\AppData\Roaming\dclogs\2023-02-20-2.dc}`

## ==Attaaaaack 10==
> Q10. we think that the malware uses persistence technique can you detect it ?
example : crew{Scheduled_tasks} (first letter of the first word is uppercase and the first letter of other is lowercase)

### Background
[NTUSTISC - CyberDefender - MrRobot - Target 1 - Q5](https://hackmd.io/@SBK6401/B1LqaNGCh/https%3A%2F%2Fhackmd.io%2F%40SBK6401%2FSkJAThwla#Q5)

### Recon
這題background可以看前面寫的文章，然後基本上都差不多，只是要特別注意-K後面帶的參數，一定要是從Software開始，他和原本cyberdefender的版本有點不太一樣，下-k參數之前先看printkey印出甚麼東西，然後再從他的subkey往後推看是要接Software還是Mircosoft，基本上都會寫在**`\REGISTRY\USER\`**的部分

### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 printkey -K "Software\Microsoft\Windows\CurrentVersion\Run"
Volatility Foundation Volatility Framework 2.6
Legend: (S) = Stable   (V) = Volatile

----------------------------
Registry: \??\C:\Users\0xSh3rl0ck\ntuser.dat
Key name: Run (S)
Last updated: 2023-02-20 19:03:40 UTC+0000

Subkeys:

Values:
REG_SZ        MicroUpdate     : (S) C:\Users\0XSH3R~1\AppData\Local\Temp\MSDCSC\runddl32.exe
----------------------------
Registry: \REGISTRY\USER\S-1-5-20
Key name: Run (S)
Last updated: 2009-07-14 04:34:14 UTC+0000

Subkeys:

Values:
REG_EXPAND_SZ Sidebar         : (S) %ProgramFiles%\Windows Sidebar\Sidebar.exe /autoRun
----------------------------
Registry: \??\C:\Windows\ServiceProfiles\LocalService\NTUSER.DAT
Key name: Run (S)
Last updated: 2009-07-14 04:34:14 UTC+0000

Subkeys:

Values:
REG_EXPAND_SZ Sidebar         : (S) %ProgramFiles%\Windows Sidebar\Sidebar.exe /autoRun
```

Flag: `crew{Registry_keys}`

## ==Attaaaaack 11==
> Q11. can you find the key name and it's value ?
example : crew{CurrentVersion_ProductName}

### Exploit
從上一題的輸出就知道key name是run，然後value是MicroUpdate
Flag: `crew{Run_MicroUpdate}`

## ==Attaaaaack 12==
> Q12. What is the strange handle used by the malware ?
example : crew{the name of the handle}

### Background
[NTUSTISC - CyberDefender - MrRobot - Target 1 - Q6](https://hackmd.io/@SBK6401/B1LqaNGCh/https%3A%2F%2Fhackmd.io%2F%40SBK6401%2FSkJAThwla#Q6)

### Recon
基本上就和之前寫的文章一樣，

### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memdump.raw --profile Win7SP1x86_23418 handles --pid 300 | findstr Mutant
Volatility Foundation Volatility Framework 2.6
Offset(V)     Pid     Handle     Access Type             Details
---------- ------ ---------- ---------- ---------------- -------
0x843b0728    300       0x58   0x1f0001 Mutant
0x843b0b28    300       0x5c   0x1f0001 Mutant
0x842eb8b8    300      0x170   0x1f0001 Mutant           DC_MUTEX-KHNEW06
0x843ac810    300      0x234   0x1f0001 Mutant
0x843ac7c0    300      0x23c   0x1f0001 Mutant
```

Flag: `crew{DC_MUTEX-KHNEW06}`

## ==Attaaaaack 13==
> Q13. Now can you help us to know the Family of this malware ?
example : crew{Malware}

### Recon
這一題在第7題就找到了

### Exploit
Flag: `crew{DarkKomet}`

## Reference
[^crewctf-attaaaaack3-wp]:[Attaaaaack3](https://github.com/daffainfo/ctf-writeup/tree/main/CrewCTF%202023/Attaaaaack3)