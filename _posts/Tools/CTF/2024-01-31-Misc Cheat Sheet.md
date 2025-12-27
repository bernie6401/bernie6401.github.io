---
title: Misc Cheat Sheet
tags: [Tools, CTF, Misc]

category: "Tools｜CTF"
---

# Misc Cheat Sheet
<!-- more -->

## Online Tools

| Encode & Decode |
| -------- |
|[Free Online Barcode Reader](https://online-barcode-reader.inliteresearch.com/)|
|[QR Code Barcode Reader Online](https://products.aspose.app/barcode/recognize/qr#/recognized)|
| [Encoding](https://emn178.github.io/online-tools/index.html)|
| [獸語](https://roar.iiilab.com/)|

## Check file info
```bash!
$ binwalk [-e] [filename] # or binwalk --dd=".*" [filename]
$ exiftool [filename]
$ pngcheck [filename]
$ stat [filename]
$ file [filename]
```
* `$ binwalk -e` 的範例可以參考[Deadface - Electric Steel ](https://hackmd.io/@SBK6401/BJgwrxWM6#Electric-Steel)

## Steganography
* text: [zsteg](https://github.com/zed-0xff/zsteg)(just for `bmp` and `png` files), [Quick Crypto](http://quickcrypto.com/download.html)
* file: steghide(`sudo apt-get install steghide`)(`$ steghide extract -sf atbash.jpg`)
* 進階的steghide$\to$[stegseek](https://github.com/RickdeJager/stegseek)
    ```bash
    $ wget https://github.com/RickdeJager/stegseek/releases/download/v0.6/stegseek_0.6-1.deb
    $ sudo apt install ./stegseek_0.6-1.deb -y
    $ stegseek [stegofile.jpg] [wordlist.txt]
    ```

## Disk Analysis
* [Foremost](https://darkranger.no-ip.org/archives/v5/document/linux/foremost_recovery.htm): 針對所支援的檔案結構去進行資料搜尋與救援
    `$ foremost -v {filename}`
* [Sleuth kit/Autopsy](https://blog.csdn.net/wxh0000mm/article/details/99447206)
* [FTK Imager](https://www.exterro.com/ftk-imager)
* [Logontracer](https://hackmd.io/@SBK6401/SJOwGrUfa): Just use GUI to present event log traced on windows
    `$ python logontracer.py -r -o 8000 -u neo4j -p neo4j -s localhost`

## Memory Forensics
* 建議直接使用[windown protable version](https://www.volatilityfoundation.org/releases)會比較穩定而且不需要處理環境的問題
* [Volatility - Cheat Sheet](https://hackmd.io/@TuX-/BymMpKd0s)
* [Volatility 3](https://github.com/volatilityfoundation/volatility3)
    :::spoiler Set up & How2Use
    [Windows Volatility 3 Problems & Solutions](https://blog.csdn.net/u011250160/article/details/120461405)
    [Windows Set up Tutorials](https://volatility3.readthedocs.io/en/latest/getting-started-windows-tutorial.html)
    ```bash!
    $ git clone https://github.com/volatilityfoundation/volatility3
    $ cd volatility3
    $ pip install -r requirement.txt
    $ python vol.py -f <path to memory image> plugin_name plugin_option
    $ python vol.py -h # For help
    ```
    :::
* [Volatility 2](https://github.com/volatilityfoundation/volatility)
    :::spoiler Set up & How2Use
    [Windows Set up Tutorials](https://volatility3.readthedocs.io/en/latest/getting-started-windows-tutorial.html)
    ```bash!
    $ conda create --name py27 python=2.7
    $ conda activate py27
    $ git clone https://github.com/volatilityfoundation/volatility
    $ cd volatility
    $ pip install pycrypto
    $ pip install distorm3
    $ python vol.py -f <path to memory image> plugin_name plugin_option
    $ python vol.py -h # For help
    ```
    :::

## Package
* [Wireshark cheat sheet](https://packetlife.net/blog/2008/oct/18/cheat-sheets-tcpdump-and-wireshark/)
* [`nmap`](http://www.osslab.tw/books/linux-administration/page/nmap-%E5%B8%B8%E7%94%A8%E6%8C%87%E4%BB%A4%E9%9B%86):
    `$ sudo apt-get install nmap`
* [`ntpdc`](https://www.ibm.com/docs/zh-tw/aix/7.3?topic=n-ntpdc4-command)
    `$ sudo apt-get install ntpdc`
* tcpflow
    `$ sudo tcpflow -r {pcap file}`

## Brute Force Password
* for WPA/Wifi based: [`aircrack-ng`](https://linuxhint.com/install_aircrack-ng_ubuntu/), [Wifite](https://ithelp.ithome.com.tw/articles/10280928)
* for system user: [John the Ripper](https://ithelp.ithome.com.tw/articles/10300529)

## Sound
* hide files: [MP3stego](https://www.petitcolas.net/steganography/mp3stego/)
    ```bash
    $ ./encode -E hidden_text.txt -P pass svega.wav svega_stego.mp3
    $ ./decode -X -P pass svega_stego.mp3
    ```
* sound to image:
    * [How to convert a SSTV audio file to images using QSSTV - en](https://ourcodeworld.com/articles/read/956/how-to-convert-decode-a-slow-scan-television-transmissions-sstv-audio-file-to-images-using-qsstv-in-ubuntu-18-04)
    * [How to convert a SSTV audio file to images using QSSTV - zh-cn](https://www.srcmini.com/62326.html)
* hide message: [silenteye](https://sourceforge.net/projects/silenteye/)

## Mail
* [PST Viewer](https://goldfynch.com/goldfynch-pst-viewer)
* [eml Viewer](https://products.groupdocs.app/zh-hant/viewer/eml)
* [ThunderBird Client](https://www.thunderbird.net/zh-TW/)

## Overall
* [All stego decrypt tools](https://aperisolve.fr/)
* [All stego encrypt tools](https://tools.miku.ac/)
* [ctf tool](http://www.ctftools.com/)
* [Other people's note](https://w1a2d3s4q5e6.blogspot.com/2016/06/blog-post.html)


