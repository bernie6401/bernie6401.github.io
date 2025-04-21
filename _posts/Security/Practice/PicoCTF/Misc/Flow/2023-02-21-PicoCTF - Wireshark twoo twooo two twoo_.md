---
title: PicoCTF - Wireshark twoo twooo two twoo...
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/Flow"
---

# PicoCTF - Wireshark twoo twooo two twoo...
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [Wireshark twoo twooo two twoo...](https://play.picoctf.org/practice/challenge/110?category=4&page=1)

## Exploit - DNS + sub-domain
1. Statistic
Using statistic to analyze http requests and you'll see that there is `/flag` and `/` in address `18.217.1.57`. Maybe it's a clue or key to find flag
![](https://i.imgur.com/VjobDhE.png)
2. String search technique
    ```bash!
    $ strings shark2.pcapng | grep "pico"
    picoCTF{bfe48e8500c454d647c55a4471985e776a07b26cba64526713f43758599aa98b}
    picoCTF{bda69bdf8f570a9aaab0e4108a0fa5f64cb26ba7d2269bb63f68af5d98b98245}
    picoCTF{fe83bcb6cfd43d3b79392f6a4232685f6ed4e7a789c2ce559cf3c1ab6adbe34b}
    picoCTF{711d3893d90f100c15e10ef4842abeed3a830f8237c1257cd47389646da97810}
    picoCTF{3cf1e22d489fcfb6bb312a34f46c8699989ed043406134331452d11ce73cd59e}
    picoCTF{b4cc138bb0f7f9da7e35085e349555aa6d00bdca3b021c1fe8663c0a422ce0d7}
    picoCTF{41b8a1a796bd8d202016f75bc5b38889e9ea06007e6b22fc856d380fb7573133}
    ...
    ```
    You'll find tons of fake flag. Obviously, it's a trap to distract you.

3. Reanalyze the file
I found that there're many DNS request to `{sub-domain}.reddshrimpandherring.com`. Also, I use the filter `http and ip.addr==18.217.1.57` and follow the http stream.
![](https://i.imgur.com/R8uRJ0n.png)
Seems this address is a clue.


4. <font color="FF0000">通靈</font>: Set new filter
payload: set the filter as `dns and ip.dst==18.217.1.57`
![](https://i.imgur.com/xbveFFN.png)
You'll see that the sub-domain is a sequence base64 strings. Concate them and decode it, you can fetch the flag. $\to$
`cGljb0NURntkbnNfM3hmMWxfZnR3X2RlYWRiZWVmfQ==` $\to$
`picoCTF{dns_3xf1l_ftw_deadbeef}`

## Reference
[Wireshark twoo twooo two twoo...](https://picoctf2021.haydenhousen.com/forensics/wireshark-twoo-twooo-two-twoo...)