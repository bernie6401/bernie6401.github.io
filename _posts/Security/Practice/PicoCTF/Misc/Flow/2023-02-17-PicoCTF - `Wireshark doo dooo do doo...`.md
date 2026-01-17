---
title: PicoCTF - `Wireshark doo dooo do doo...`
tags: [PicoCTF, CTF, Misc]

category: "Security｜Practice｜PicoCTF｜Misc｜Flow"
date: 2023-02-17
---

# PicoCTF - `Wireshark doo dooo do doo...`
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: https://play.picoctf.org/practice/challenge/115?category=4&page=1


## Exploit - strings + rot13
```bash!
$ strings shark1.pcapng | grep "{"
...
Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
...
```
Obviously a encrypted flag $\to$ use rot13
flag: `picoCTF{p33kab00_1_s33_u_deadbeef}`