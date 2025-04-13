---
title: PicoCTF - Trivial Flag Transfer Protocol
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/Flow"
---

# PicoCTF - Trivial Flag Transfer Protocol
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [Trivial Flag Transfer Protocol](https://play.picoctf.org/practice/challenge/103?bookmarked=0&category=4&page=1&search=&solved=0)

## Background
* [TFTP協定是什麼？](https://tw511.com/a/01/2927.html)

* [Wireless router中的UPnP是做什麼用的?](https://www.mobile01.com/topicdetail.php?f=110&t=921577)
    > UPnP 是一種通訊協定，其主要功能是供家中的設備可以輕易的且自動的連結到網路並完成網路相關設定。
不需要您本人手動去設定就可以使用的意思。
所以你的 router 有支援並打開這項功能後，您家中的視訊設備（大部分都是支援UPnP）接上網路、打開電源。
接著你的 作業系統也支援的話，以winodws 為例，「我的電腦」中就會看到您新增的設備，如無線router、media server等等。

* [SSDP - 通訊協定 ?](https://ithelp.ithome.com.tw/questions/10002825)
    > SSDP的全寫是「Simple Service Discovery Protocol」，使用在Universal Plug and Play (UPnP)網絡環境中。SSDP使用UDP1900連接埠搜尋互聯網上的數據。當SSDP開啟時，其他設置會曝露自己到所有UPnP的用戶端中。

* [`steghide` instruction](https://ithelp.ithome.com.tw/articles/10278964)


## Exploit - TFTP + steghide
1. Save files
According to the article: [TFTP協定是什麼？](https://tw511.com/a/01/2927.html), we can aware that this protocol is aim to transfer the data without authentication. So, we can download the files using wireshark.
![](https://i.imgur.com/rETlGmm.png)

2. Check files
Check `instructions.txt` first.
Seems encoding by `rot13` $\to$ `TFTP DOESNT ENCRYPT OUR TRAFFIC SO WE MUST DISGUISE OUR FLAG TRANSFER. FIGURE OUT A WAY TO HIDE THE FLAG AND I WILL CHECK BACK FOR THE PLAN`.

Check `plan` file next.
Seems encoded by `rot13` again $\to$ `I USED THE PROGRAM AND HID IT WITH - DUEDILIGENCE. CHECK OUT THE PHOTOS`.
The author seems hide some files in transferred photos.

3. `steghide`
    ```bash!
    $ steghide info picture1.bmp
    "picture1.bmp":
      format: Windows 3.x bitmap
      capacity: 33.5 KB
    Try to get information about embedded data ? (y/n) y
    Enter passphrase:
    steghide: could not extract any data with that passphrase!
    $ steghide info picture2.bmp
    "picture2.bmp":
      format: Windows 3.x bitmap
      capacity: 1.5 MB
    Try to get information about embedded data ? (y/n) y
    Enter passphrase:
    steghide: could not extract any data with that passphrase!
    $ steghide info picture3.bmp
    "picture3.bmp":
      format: Windows 3.x bitmap
      capacity: 59.6 KB
    Try to get information about embedded data ? (y/n) y
    Enter passphrase:
      embedded file "flag.txt":
        size: 40.0 Byte
        encrypted: rijndael-128, cbc
        compressed: yes
    ```
    * Note that the passphrace must enter `DUEDILIGENCE` that author gave us.
    Seems `picture3.bmp` has something
    ```bash
    $ steghide extract -sf picture3.bmp
    Enter passphrase:
    wrote extracted data to "flag.txt".
    $ cat flag.txt
    picoCTF{h1dd3n_1n_pLa1n_51GHT_18375919}
    ```

## Reference
[picoCTF 2021 Trivial Flag Transfer Protocol](https://youtu.be/VmSgalNMw_Y)