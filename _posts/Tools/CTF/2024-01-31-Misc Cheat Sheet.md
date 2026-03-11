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