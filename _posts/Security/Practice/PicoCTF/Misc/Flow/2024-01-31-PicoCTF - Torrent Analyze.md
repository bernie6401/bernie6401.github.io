---
title: PicoCTF - Torrent Analyze
tags: [PicoCTF, CTF, Misc]

category: "Security｜Practice｜PicoCTF｜Misc｜Flow"
---

# PicoCTF - Torrent Analyze
<!-- more -->

## Background
[What are seeds, peers and leechers in Torrents’ language?](https://www.techworm.net/2017/03/seeds-peers-leechers-torrents-language.html)
[慎選peer，是加速BT下載的王道！](https://www.mobile01.com/topicdetail.php?f=507&t=1365797)
> 1. seed個數：seed（即一般所說的「種子」）意指擁有完整檔案的BT參與者，是主要的檔案提供者。seed越多，可用的BT分享頻寬就越多，速度當然就快。
> 2. seed與peer的比例：雖然peer（指尚未取得完整檔案的BT參與者）可同時自seed與其他peer下載檔案，但peer間會彼此競爭，以爭取有限的BT下載頻寬。因此，peer個數越多，分配後的BT分享頻寬就越少，速度自然就受影響。

[教你該如何使用bt的info hash特徵碼，下載BT之torrent種子檔](http://zfly9.blogspot.com/2014/10/hashmethod.html)

## Description & Hint
> SOS, someone is torrenting on our network. One of your colleagues has been using torrent to download some files on the company’s network. Can you identify the file(s) that were downloaded? The file name will be the flag, like picoCTF{filename}.
> Hint 1: Download and open the file with a packet analyzer like [Wireshark](https://www.wireshark.org/).
> Hint 2: You may want to enable BitTorrent protocol (BT-DHT, etc.) on Wireshark. Analyze -> Enabled Protocols
> Hint 3: Try to understand peers, leechers and seeds. [Article](https://www.techworm.net/2017/03/seeds-peers-leechers-torrents-language.html)
> Hint 4: The file name ends with `.iso`

## Recon
這是非常有趣的題目，不過完全沒有用過bittorrent或是info hash相關的背景知識，所以看了[^pico-misc-torrent-analyze-almod-force]的WP覺得學到很多
1. 簡單來說，這支pcap紀錄了利用bittorrent下載/上傳的流量，而我們要找出他下載/上傳的file name為何，有趣的地方是利用bittorrent這種P2P的方式，一定會自帶一個file的info hash，驗明正身，所以我們只要找到BT-UDP protocol中，有夾帶info-hash的packet出來，再丟到網路上查詢就可以了
2. Set Filter as `bt-dht contains "info_hash"`
設定filter後，就可以看到每一個bt-dht protocol packets都含有info_hash的keys，不過其中有很多不同的info hash所以要一個一個試很麻煩就寫了一個script dump出來，最後只有8個，不過如果把全部packet不管有沒有重複全部print出來的話，很明顯最後一個`e2467cbf021192c241367b892230dc1e05c0580e`是最多的，那這個應該就是答案，因為.iso通常都很大，所以下載的packets數量應該是比較多的

## Exploit
```python=
import pyshark

capture = pyshark.FileCapture('PicoCTF/Misc/Torrent Analyze/torrent.pcap', display_filter='bt-dht contains "info_hash"')

info_hashs = []
for pkt in capture:
    info_hash = pkt.layers[3].get_field_by_showname('info_hash').showname_value
    if info_hash not in info_hashs:
        print(info_hash)
        info_hashs.append(info_hash)
    
```

```bash
17d62de1495d4404f6fb385bdfd7ead5c897ea22
17c1e42e811a83f12c697c21bed9c72b5cb3000d
d59b1ce3bf41f1d282c1923544629062948afadd
078e18df4efe53eb39d3425e91d1e9f4777d85ac
7af6be54c2ed4dcb8d17bf599516b97bb66c0bfd
17c0c2c3b7825ba4fbe2f8c8055e000421def12c
17c02f9957ea8604bc5a04ad3b56766a092b5556
e2467cbf021192c241367b892230dc1e05c0580e
```

Info Hash: `e2467cbf021192c241367b892230dc1e05c0580e`
File Name: `ubuntu-19.10-desktop-amd64.iso`
Flag: `picoCTF{ubuntu-19.10-desktop-amd64.iso}`
![](https://hackmd.io/_uploads/BJ-y_mPxp.png)

## Reference
[^pico-misc-torrent-analyze-almod-force]:[ picoGym (picoCTF) Exercise: Torrent Analyze ](https://youtu.be/XWQDnY2qaZg?si=LbdCmgY2zJG1e25z)