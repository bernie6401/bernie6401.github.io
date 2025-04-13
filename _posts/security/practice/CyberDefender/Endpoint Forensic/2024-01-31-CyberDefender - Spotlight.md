---
title: CyberDefender - Spotlight
tags: [CyberDefender, Endpoint Forensics]

category: "Security/Practice/CyberDefender/Endpoint Forensic"
---

# CyberDefender - Spotlight
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/34#nav-questions

:::spoiler TOC
[TOC]
:::

## Tools:
* Autopsy
* [mac_apt](https://github.com/ydkhatri/mac_apt/releases)
* SQLite
* steghide

:::info
因為這一個lab是有關Mac-OS的forensics，也沒有相關的背景知識，所以解出來的部分大多參考[^wp][^wp-1]，就是當作第一次學習的課題
:::

## ==Q1==
> What version of macOS is running on this image? 

#### Recon
這個是參考[^wp]

#### Exploit
在`./root/System/Library/CoreServices/`中可以找到`SystemVersion.plist`
![圖片](https://hackmd.io/_uploads/HJqsQEjQp.png)

:::spoiler Flag
Flag: `10.15`
:::

## ==Q2==
> What "competitive advantage" did Hansel lie about in the file AnotherExample.jpg? (two words)

#### Exploit
直接翻一下`AnotherExample.jpg`所在的資料夾，就可以發現有一個secret的text檔案，裡面就有這題的flag，不太知道和這張圖片有甚麼關係
:::info
11/13更新: 直接strings search這張圖片也可以找到secret strings的東西
:::

:::spoiler Flag
Flag: `flip phone`
:::

## ==Q3==
> How many bookmarks are registered in safari? 

#### Recon
這個是參考[^wp]

#### Exploit
首先可以在`./root/Users/hansel.apricot/Library/Safari`的地方找到`Bookmarks.plist`，只要利用plistutil轉換成一般的xml格式就可以了
```bash
$ plistutil -i Bookmarks.plist | grep "URLString" | wc -l
13
```

:::spoiler Flag
Flag: `13`
:::

## ==Q4==
> What's the content of the note titled "Passwords"? 

#### Recon
這一題是參考[^wp-1]，mac會把使用者的Note放在`./root/Users/hansel.apricot/Library/Group Containers/group.com.apple.notes`中的==NoteStore.sqlite==

#### Exploit
可以看到Title是Passwords但沒有內容，依照[^wp-1]的說明，他是覺得答案應該是視title為content的一部份
![圖片](https://hackmd.io/_uploads/ryf4P6kVa.png)

:::spoiler Flag
Flag: `Passwords`
:::

## ==Q5==
> Provide the MAC address of the ethernet adapter for this machine. 

#### Recon
這一題是參考[^wp-1]，就是直接grep search ==en0==

#### Exploit
可以發現`root/private/var/log/daily.out`有符合
```bash
$ grep -i -r "en0"
grep: root/.fseventsd/00000000007f0fb2: binary file matches
root/private/var/log/daily.out:en0   1500  <Link#4>    00:0c:29:c4:65:77   372733     0    73025     0     0
root/private/var/log/daily.out:en0   1500  fe80::8c8:8 fe80:4::8c8:87c2:   372733     -    73025     -     -
root/private/var/log/daily.out:en0   1500  184.171.151/2 stu-181-151-171   372733     -    73025     -     -
root/private/var/log/daily.out:en0   1500  <Link#4>    00:0c:29:c4:65:77      790     0      694     0     0
root/private/var/log/daily.out:en0   1500  fe80::1cba: fe80:4::1cba:cac8      790     -      694     -     -
root/private/var/log/daily.out:en0   1500  184.171.151/2 stu-181-151-171      790     -      694     -     -
grep: root/private/var/log/DiagnosticMessages/2020.04.19.asl: binary file matches
grep: root/Users/hansel.apricot/Library/Safari/CloudAutoFillCorrections.db: binary file matches
grep: root/Users/sneaky/.Trash/silenteye-0.4.1b-snowleopard.dmg: binary file matches
```

:::spoiler Flag
Flag: `00:0c:29:c4:65:77`
:::

## ==Q6==
> Name the data URL of the quarantined item. 

#### Recon
這一題是參考[^wp-1]
> Quarantined Events are a log of all downloaded items on MacOS.

#### Exploit
主要macOS會把==com.apple.LaunchServices.QuarantineEventsV2==放在`./root/Users/sneaky/Library/Preferences/`，目前只有一個quarantined目標

:::spoiler Flag
Flag: `https://futureboy.us/stegano/encode.pl`
:::

## ==Q7==
> What app did the user "sneaky" try to install via a .dmg file? (one word)

#### Exploit
我是直接翻`./root/Users/sneaky/.Trash`就直接看到了
![圖片](https://hackmd.io/_uploads/H1Hk-Vo7T.png)

:::spoiler Flag
Flag: `silenteye`
:::

## ==Q8==
> What was the file 'Examplesteg.jpg' renamed to?

#### Recon
這一題是參考[^wp-1]，必須使用`mac_apt`這套工具中的==FSEVENTS==幫忙parse `.fseventsd`中所有的event logs files
> FSEVENTS: Reads file system event logs (from .fseventsd)

#### Exploit
```bash
$ ./mac_apt_artifact_only.exe -i .fseventsd -o ./ FSEVENTS
Output path was : ./
MAIN-INFO-Started macOS Artifact Parsing Tool - Artifact Only mode, version 1.5.8.dev (20230617)
MAIN-INFO-Dates and times are in UTC unless the specific artifact being parsed saves it as local time!
MAIN-INFO---------------------------------------------------
MAIN-INFO-Running plugin FSEVENTS
MAIN-INFO---------------------------------------------------
MAIN.FSEVENTS-INFO-Module Started as standalone
MAIN.FSEVENTS-INFO-Writing 231662 fsevent(s)
MAIN.FSEVENTS-INFO-The source_date field on the fsevents are from the individual file modified date (metadata not data)! This may have changed if you are not on a live or read-only image.
MAIN.FSEVENTS-INFO-231662 logs found
MAIN-INFO---------------------------------------------------
MAIN-INFO-Finished in time = 00:00:04
MAIN-INFO-Review the Log file and report any ERRORs or EXCEPTIONS to the developers
```
command結束會吐一個db file和一個log file，分析db file後就直接filter `Examplesteg.jpg`這張圖片
![圖片](https://hackmd.io/_uploads/ry1oHAkEa.png)

此時我們可以複製該file的ID，再接續filter
File ID: `12885043806`
![圖片](https://hackmd.io/_uploads/SJeaBC1Ea.png)

:::spoiler Flag
Flag: `GoodExample.jpg`
:::

## ==Q9==
> How much time was spent on mail.zoho.com on 4/20/2020? 

#### Recon
這一題是參考[^wp-1]，有關於screentime這個資訊會放在`./root/private/var/folders/bf/r04p_gb17xxg37r9ksq855mh0000gn/0/com.apple.ScreenTimeAgent/Store/`的==RMAdminStore-Local.sqlite== db file中，也是一樣透過mac_apt幫忙parse(SCREENTIME)
:::info
記得要把`RMAdminStore-Local.sqlite-wal`和`RMAdminStore-Local.sqlite`這個檔案放在一起再執行
:::

#### Exploit
```bash
$ ls
RMAdminStore-Local.sqlite-shm mac_apt_artifact_only.exe RMAdminStore-Local.sqlite  RMAdminStore-Local.sqlite-wal  mac_apt.exe  mac_apt_mounted_sys_data.exe
$ ./mac_apt_artifact_only.exe -i RMAdminStore-Local.sqlite -o . SCREENTIME
Output path was : .
MAIN-INFO-Started macOS Artifact Parsing Tool - Artifact Only mode, version 1.5.8.dev (20230617)
MAIN-INFO-Dates and times are in UTC unless the specific artifact being parsed saves it as local time!
MAIN-INFO---------------------------------------------------
MAIN-INFO-Running plugin SCREENTIME
MAIN-INFO---------------------------------------------------
MAIN.SCREENTIME-INFO-Module Started as standalone
MAIN.SCREENTIME-INFO-Processing file RMAdminStore-Local.sqlite
MAIN-INFO---------------------------------------------------
MAIN-INFO-Finished in time = 00:00:00
MAIN-INFO-Review the Log file and report any ERRORs or EXCEPTIONS to the developers
```
接下來就是設定filter就知道他在4/20有兩次的request
![圖片](https://hackmd.io/_uploads/SktS5Rk4a.png)

:::spoiler Flag
Flag: `20:58`
:::

## ==Q10==
> What's hansel.apricot's password hint? (two words) 

### Recon
這一題是參考[^wp-1]
> Password information can be found in the user plist, in private/db/dslocal/nodes/Default/users/(username).plist

### Exploit
```bash
$ plistutil -i hansel.apricot.plist -o hansel.apricot.plist.txt
$ vim hansel.apricot.plist.txt
```
![圖片](https://hackmd.io/_uploads/B17MpgGV6.png)

:::spoiler Flag
Flag: `Family Opinion`
:::

## ==Q11==
> The main file that stores Hansel's iMessages had a few permissions changes. How many times did the permissions change? 

### Recon
直覺是承接第8題，看他的event log，而根據[^wp-1]的說明
> The mail file storing iMessages in MacOS is `chat.db`

### Exploit
![圖片](https://hackmd.io/_uploads/HkTk4-fNa.png)

:::spoiler Flag
Flag: `7`
:::

## ==Q12==
> What's the UID of the user who is responsible for connecting mobile devices? 

### Recon
這一題是參考[^wp-1]，主要是找到位於`root/private/var/db/dslocal/nodes/Default/users/`的`_usbmuxd.plist`，這個file主要是:
> The process responsible for connecting iPhones/iPads with MacOS is lockdown

但就算不找到這個file，應該還是有其他file是可以擷取出UID的資訊

### Exploit
![圖片](https://hackmd.io/_uploads/S1R8U-f4a.png)

:::spoiler Flag
Flag: `213`
:::

## ==Q13==
> Find the flag in the GoodExample.jpg image. It's hidden with better tools. 

#### Exploit
這個直接用steghide隱藏起來，密碼為空，解出來的file內容如下
```bash
$ steghide extract -sf GoodExample.jpg
Enter passphrase:
wrote extracted data to "steganopayload27635.txt".
$ cat steganopayload27635.txt
Our latest phone will have flag<helicopter> blades and 6 cameras on it. No
other phone has those features!%
```

:::spoiler Flag
Flag: `helicopter`
:::

## ==Q14==
> What was exactly typed in the Spotlight search bar on 4/20/2020 02:09:48 

### Recon
因為本身不是mac使用者，所以不知道Spotlight功能具體功用為何
[在 Mac 上使用 Spotlight 搜尋](https://support.apple.com/zh-tw/guide/mac-help/mchlp1008/mac)
> Spotlight 可協助你快速找到 Mac 上的 App、文件、電子郵件和其他項目

感覺有點類似windows的cortona?
根據[ChatGPT的說明](https://chat.openai.com/c/0279d872-547b-4ebd-b0fd-2ae9096b6b96)，兩者有部分功能類似，不過Cortana比較像是智能助理的感覺，而spotlight只是能夠快速找到一些使用者像要找的file/app/email之類的個人資訊

### Exploit
```bash
$ grep -r -i '2020-04-20' *
grep: macOS Catalina - Data [volume_0]/root/private/var/log/powermanagement/2020.04.19.asl: binary file matches
macOS Catalina - Data [volume_0]/root/Users/sneaky/Library/Application Support/com.apple.spotlight/com.apple.spotlight.Shortcuts:               <date>2020-04-20T02:44:27Z</date>
macOS Catalina - Data [volume_0]/root/Users/sneaky/Library/Application Support/com.apple.spotlight/com.apple.spotlight.Shortcuts:               <date>2020-04-20T02:09:48Z</date>
macOS Catalina - Data [volume_0]/root/Users/sneaky/Library/Application Support/com.apple.touristd/com.apple.touristd.plist:     <date>2020-04-20T02:04:09Z</date>
macOS Catalina - Data [volume_0]/root/Users/sneaky/Library/Application Support/CrashReporter/Intervals_564D2904-54C9-8D99-F8CA-9D7111C46577.plist:              <date>2020-04-20T02:04:08Z</date>
macOS Catalina - Data [volume_0]/root/Users/sneaky/Library/Application Support/CrashReporter/Intervals_564D2904-54C9-8D99-F8CA-9D7111C46577.plist:      <date>2020-04-20T02:04:08Z</date>
macOS Catalina - Data [volume_0]/root/Users/sneaky/Library/Application Support/CrashReporter/Intervals_564D2904-54C9-8D99-F8CA-9D7111C46577.plist:      <date>2020-04-20T02:04:08Z</date>
macOS Catalina - Data [volume_0]/root/Users/sneaky/Library/Application Support/CrashReporter/Intervals_564D2904-54C9-8D99-F8CA-9D7111C46577.plist:              <date>2020-04-20T04:29:01Z</date>
macOS Catalina - Data [volume_0]/root/Users/sneaky/Library/Preferences/com.apple.security.KCN.plist:    <date>2020-04-20T03:19:33Z</date>
```
直接用grep search找到位於`./root/Users/sneaky/Library/Application Support/com.apple.spotlight/`的==com.apple.spotlight.Shortcuts==
```bash
$ cat macOS\ Catalina\ -\ Data\ \[volume_0\]/root/Users/sneaky/Library/Application\ Support/com.apple.spotlight/com.apple.spotlight.Shortcuts
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>silent</key>
        <dict>
                <key>DISPLAY_NAME</key>
                <string>silenteye-0.4.1b-snowleopard_installer</string>
                <key>LAST_USED</key>
                <date>2020-04-20T02:44:27Z</date>
                <key>URL</key>
                <string>/Applications/silenteye-0.4.1b-snowleopard_installer.app</string>
        </dict>
        <key>term</key>
        <dict>
                <key>DISPLAY_NAME</key>
                <string>Terminal</string>
                <key>LAST_USED</key>
                <date>2020-04-20T02:09:48Z</date>
                <key>URL</key>
                <string>/System/Applications/Utilities/Terminal.app</string>
        </dict>
</dict>
</plist>
```
從結果來看，使用者在`2020-04-20 02:44:27`輸入過==silent==這個關鍵字，並且顯示silenteye-0.4.1b-snowleopard_installer這個strings，同樣的在`2020-04-20 02:09:48`時，使用者輸入了==term==這個關鍵字，並且系統回傳Terminal這個strings

:::spoiler Flag
Flag: `term`
:::

## ==Q15==
> What is hansel.apricot's Open Directory user UUID? 

### Recon
這一題還是參考[^wp-1]，主要是承接第10題的結果，可以在下面看到generateduid的strings
![圖片](https://hackmd.io/_uploads/HkQyHfzV6.png)

:::spoiler Flag
Flag: `5BB00259-4F58-4FDE-BC67-C2659BA0A5A4`
:::

## Reference
[^wp]:[Spotlight Blue Team Challenge](https://medium.com/@nishadbabu1015/spotlight-blue-team-challenge-f3edaea5dba3)
[^wp-1]:[CyberDefenders: Spotlight](https://forensicskween.com/ctf/cyberdefenders/spotlight/)