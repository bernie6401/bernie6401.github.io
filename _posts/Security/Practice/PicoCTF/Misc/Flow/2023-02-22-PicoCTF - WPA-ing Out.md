---
title: PicoCTF - WPA-ing Out
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/Flow"
---

# PicoCTF - WPA-ing Out
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [WPA-ing Out](https://play.picoctf.org/practice/challenge/206?category=4&page=2)

## Background
[Day 26 Wireless Attacks-無線攻擊(aircrack-ng)](https://ithelp.ithome.com.tw/articles/10280033)

## Description & Hint
> I thought that my password was super-secret, but it turns out that passwords passed over the AIR can be CRACKED, especially if I used the same wireless network password as one in the <font color="FF0000">`rockyou.txt`</font> credential dump. Use this [`pcap file`](https://artifacts.picoctf.net/c/8/wpa-ing_out.pcap) and the `rockyou` wordlist. The flag should be entered in the `picoCTF{XXXXXX}` format.

Hint 1: Finding the IEEE 802.11 wireless protocol used in the wireless traffic packet capture is easier with `wireshark`, the JAWS of the network.
Hint 2: `Aircrack-ng` can make a `pcap` file catch big air...and crack a password.

## Exploit - [`aircrack-ng`](https://linuxhint.com/install_aircrack-ng_ubuntu/)
```bash!
$ aircrack-ng wpa-ing_out.pcap -w ./rockyou.txt
Reading packets, please wait...
Opening wpa-ing_out.pcap
Read 23523 packets.

   #  BSSID              ESSID                     Encryption

   1  00:5F:67:4F:6A:1A  Gone_Surfing              WPA (1 handshake)

Choosing first network as target.

Reading packets, please wait...
Opening wpa-ing_out.pcap
Read 23523 packets.

1 potential targets

                               Aircrack-ng 1.6

      [00:00:00] 1183/10303727 keys tested (22306.13 k/s)

      Time left: 7 minutes, 41 seconds                           0.01%

                          KEY FOUND! [ mickeymouse ]


      Master Key     : 61 64 B9 5E FC 6F 41 70 70 81 F6 40 80 9F AF B1
                       4A 9E C5 C4 E1 67 B8 AB 58 E3 E8 8E E6 66 EB 11

      Transient Key  : 26 85 7B AC DD 2C 44 E6 06 18 03 B0 0F F2 75 A2
                       32 63 F7 35 74 2D 18 10 1C 25 F9 14 BC 41 DA 58
                       52 48 86 B0 D6 14 89 F6 77 00 67 E0 AD 10 1B 00
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

      EAPOL HMAC     : 65 2F 6C 0E 75 F0 49 27 6A AA 6A 06 A7 24 B9 A9
```
So...The flag is `picoCTF{mickeymouse}`

## Reference
[Install tshark](https://tshark.dev/setup/install/)
[Some error you may encounter](https://www.cnblogs.com/liqinglucky/p/16989773.html)
[ubuntu下安装lex,yacc](https://blog.csdn.net/hitwhylz/article/details/25342271)
[WU1 - WPA-ing Out](https://cscbinus.com/articles/WU1-WPA-ing_Out)