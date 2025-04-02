---
title: CyberDefender - CorporateSecrets (Part 4)
tags: [CyberDefender, Endpoint Forensics]

---

# CyberDefender - CorporateSecrets (Part 4)
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/33
Part 1: https://hackmd.io/@SBK6401/r18z7VIm6
Part 2: https://hackmd.io/@SBK6401/ByFhEE8X6
Part 3: https://hackmd.io/@SBK6401/HyHp4NLQT

:::spoiler TOC
[TOC]
:::

## Tools: 
* FTK Imager
* Registry Explorer
* RegRipper
* HxD
* DB Browser for SQLite
* HindSight
* Event Log Explorer
* MFTDump


## ==Q28==
> What cloud service was a Startup item for the user admin? 
### Recon
直接看admin的NTUSER.DAT中的`./Software/Microsoft/Windows/CurrentVersion/Run`就可以了
### Exploit
![圖片.png](https://hackmd.io/_uploads/BJodWuDmp.png)

:::spoiler Flag
Flag: `OneDrive`
:::
## ==Q29==
> Which Firefox prefetch file has the most runtimes?
(Flag format is )
### Exploit
直接export出和firefox有關的prefetch file，再用PECmd去parse他就可以看到各個執行檔執行的次數
```bash!
$ ./PECmd.exe -f FIREFOX\ INSTALLER.EXE-71BB164E.pf | grep "Run count"
Run count: 1
$ ./PECmd.exe -f FIREFOX.EXE-20153F0F.pf | grep "Run count"
Run count: 10
$ ./PECmd.exe -f FIREFOX.EXE-A606B53C.pf | grep "Run count"
Run count: 21
$ ./PECmd.exe -f FIREFOX.EXE-B4420372.pf | grep "Run count"
Run count: 4
$ ./PECmd.exe -f FIRSTLOGONANIM.EXE-674CDAB9.pf | grep "Run count"
Run count: 1
```

:::spoiler Flag
Flag: `FIREFOX.EXE-A606B53C.pf/21`
:::
## ==Q30==
> What was the last IP address the machine was connected to?
### Exploit
直接看`SYSTEM/ControlSet001/Services/Tcpip/Parameters/Interfaces/`
![圖片.png](https://hackmd.io/_uploads/S18wduPQT.png)

:::spoiler Flag
Flag: `192.168.2.242`
:::
## ==Q31==
> Which user had the most items pinned to their taskbar? 
### Recon
這一題也是新的觀念，taskbar items會在`C:\Users\USERNAME\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar`
### Exploit
* admin
    ![圖片.png](https://hackmd.io/_uploads/Hk8oCKw76.png)
* jim.tomato
    ![圖片.png](https://hackmd.io/_uploads/Hy4pRtwma.png)
* hansel.apricot
    ![圖片.png](https://hackmd.io/_uploads/BkD-J9v7a.png)
* miriam.grapes
    ![圖片.png](https://hackmd.io/_uploads/H1rQkcvm6.png)
* suzy.strawberry
    ![圖片.png](https://hackmd.io/_uploads/Sk1SyqvmT.png)

:::spoiler Flag
Flag: `admin`
:::
## ==Q32==
> What was the last run date of the executable with an MFT record number of 164885?
(Format: MM/DD/YYYY HH:MM:SS (UTC).) 
### Recon
直覺會看第26題用mftdump的結果，然後去看164885的offset address，再去看\$MFT的timestamp，不過後來想想，\$MFT的timestamp所記錄的是`Creat Time + Modified Time + $MFT Modified Time + Access Time`，並不是最後執行的timestamp，所以應該是去看是哪一個檔案，然後去看他的prefetch file
### Exploit
1. Record No. 164885 $\to$ 0x0a105400
2. `7zG.exe`
    ![圖片.png](https://hackmd.io/_uploads/Syb-8KD7a.png)
3. Export Prefetch
    ![圖片.png](https://hackmd.io/_uploads/SJgmLFvQp.png)
4. Parse Prefetch File
    ```bash
    $ ./PECmd.exe -f 7ZG.EXE-0F8C4081.pf | grep "Last run"
    Last run: 2020-04-12 02:32:09
    ```

:::spoiler Flag
Flag: `04/12/2020 02:32:09`
:::
## ==Q33==
> What is the log file sequence number for the file "fruit_Assortment.jpg"? 
### Recon
這也是一個新觀念，log file sequence number就是在\$MFT的magic header(FILE0)的後面(SO=8, LE=8)，並且倒著看再轉換成十進制就可以了，當然也可以直接用像[MFTEcmd](https://ericzimmerman.github.io/#!index.md)這樣的parser
### Exploit
```bash
>>> num = '60 BA 1A 4C 00 00 00 00'
>>> int("".join(num.split(' ')[::-1]), 16)
1276820064
```

:::spoiler Flag
Flag: `1276820064`
:::
## ==Q34==
> Jim has some dirt on the company stored in a docx file. Find it, the flag is the fourth secret, in the format of <"The flag is a sentence you put in quotes">.
(Secrets, secrets are no fun) 
### Recon
這一題很複雜，一開始想說是類似docx forensics的這種CTF類型，所以找了一下其他的.docx files
### Exploit
1. Search .docx Files
    從recycle bin中可以看到Jim的SID(1003)有丟棄一些docx file的痕跡，直接把這些file export出來
2. 一番操作之後都沒有甚麼結果，所以就參考[^wp]的作法，和[之前的經驗](https://hackmd.io/@SBK6401/H1w0vImC2)，先把extension改成zip，然後解壓縮他
3. 再把`./Document1/Content.xml`用Microsoft Word開啟，就可以看到主要的內容了，這神奇的操作也是第一次看到
    ![圖片.png](https://hackmd.io/_uploads/SytYatPmT.png)

:::spoiler Flag
Flag: `Customer data is not stored securely`
:::
## ==Q35==
> In the company Slack, what is threatened to be deactivated if the user gets their email deactivated? 
### Recon

### Exploit
我覺得[^wp]解法比較有效率，不然慢慢找真的會瘋掉
1. 先找到有誰使用slack這套軟體，因為之前在寫前面的東西的時候就翻到了，所以可以參考就好
    ```bash
    $ find . -type d -name 'Slack'
    ./Users/hansel.apricot/AppData/Roaming/Slack
    ```
2. 接著看有沒有和題目相關的字眼
    ```bash
    $ grep -r -i 'deactivate' ./Users/hansel.apricot/AppData/Roaming/Slack > grep_deactivate.txt
    ```
3. 看哪一個file有和`deactivate`有關係，前面一大段是Cache就不用理他
    ![圖片.png](https://hackmd.io/_uploads/Hyr_PqvQ6.png)
    可以看到應該是`./Users/hansel.apricot/AppData/Roaming/Slack/IndexedDB/https_app.slack.com_0.indexeddb.leveldb/000003.log matches`比較符合
4. 直接strings search
    ```bash!
    $ strings ./Users/hansel.apricot/AppData/Roaming/Slack/IndexedDB/https_app.slack.com_0.indexeddb.leveldb/000003.lo
    g | grep text > log_dump.txt
    ```
5. 仔細看其中的內容，看來看去`kneecaps`應該就是答案，但我不確定這一題到底在幹嘛，或者說出題意義不明
    ```
    text"5And so do your kneecaps, well, as much as they do now{
    ```
    
:::spoiler Flag
Flag: `kneecaps`
:::
## Reference
[^wp]:[CyberDefenders: CorporateSecrets](https://forensicskween.com/ctf/cyberdefenders/corporatesecrets/)