---
title: 'PicoCTF - Pitter, Patter, Platters'
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/Disk"
---

# PicoCTF - Pitter, Patter, Platters
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [Pitter, Patter, Platters](https://play.picoctf.org/practice/challenge/87?category=4&page=2)

## Background
[sda](https://blog.gtwang.org/linux/linux-add-format-mount-harddisk/)

## Source code

## Exploit - Use FTK Imager
* I use Autopsy but find nothing except a txt file
![](https://i.imgur.com/7IXjuMn.png)
So I follow [write up video](https://youtu.be/P0wvFs02oKY) to use `FTK imager` and it can parse files completely.
![](https://i.imgur.com/FdC9k3V.png)

ORRRR...

* Use `HxD` as auxiliary tool to find flag
![](https://i.imgur.com/RTIOn1G.png)

ORRRR...

* Just use string search
    ```bash!
    $ strings -e l Pitter,\ Patter,\ Platters.sda1 | rev
    picoCTF{b3_5t111_mL|_<3_ba880921}
    ...
    ```

## Reference
[Pitter, Patter, Platters write up](https://github.com/Dvd848/CTFs/blob/master/2020_picoCTF_Mini/Pitter_Patter_Platters.md)
[pico 2020 mini pitter patter platters](https://youtu.be/P0wvFs02oKY)