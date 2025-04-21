---
title: BTLO - Secrets
tags: [BTLO, Incident Response]

category: "Security/Practice/BTLO/Incident Response"
---

# BTLO - Secrets
<!-- more -->
Challenge: https://blueteamlabs.online/home/challenge/secrets-85aa2bb3a9

:::spoiler TOC
[TOC]
:::

## Scenario
> You’re a senior cyber security engineer and during your shift, we have intercepted/noticed a high privilege actions from unknown source that could be identified as malicious. We have got you the ticket that made these actions.
You are the one who created the secret for these tickets. Please fix this and submit the low privilege ticket so we can make sure that you deserve this position.
Here is the ticket:
>
> eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiQlRMe180X0V5ZXN9IiwiaWF0Ijo5MDAwMDAwMCwibmFtZSI6IkdyZWF0RXhwIiwiYWRtaW4iOnRydWV9.jbkZHll_W17BOALT95JQ17glHBj9nY-oWhT1uiahtv8 

## ==Q1==
> Can you identify the name of the token? (Format: String)

### Recon
看到三段用`.`拼起來就直覺是jwt

:::spoiler Flag
Flag: `jwt`
:::

## ==Q2==
> What is the structure of this token? (Format: Section.Section.Section)

### Recon
Common Sense就是header + payload + signature
![圖片](https://hackmd.io/_uploads/rk--WjCva.png)

:::spoiler Flag
Flag: `header.payload.signature`
:::

## ==Q3==
> What is the hint you found from this token? (Format: String)

### Recon
這一題真的不知道在衝三小，最後參考[^wp1]才知道，但實在是太隱晦了，不管是問題還是答案出乎意料

:::spoiler Flag
Flag: `_4_Eyes`
:::

## ==Q4==
> What is the Secret? (Format: String)

### Recon
這個直覺就是要爆破簽署的secrets，因為看來看去都沒有其他地方有leak出來，所以可以用hashcat或是john爆破出來

### Exploit
* Hashcat - [Hacking JWT Tokens: Bruteforcing Weak Signing Key (Hashcat)](https://blog.pentesteracademy.com/hacking-jwt-tokens-bruteforcing-weak-signing-key-hashcat-7dba165e905e)
    ```bash
    $ echo 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiQlRMe180X0V5ZXN9IiwiaWF0Ijo5MDAwMDAwMCwibmFtZSI6IkdyZWF0RXhwIiwiYWRtaW4iOnRydWV9.jbkZHll_W17BOALT95JQ17glHBj9nY-oWhT1uiahtv8'> jwt.txt
    $ hashcat -a 3 -m 16500 jwt.txt ?a?a?a?a
    hashcat (v6.2.6) starting

    OpenCL API (OpenCL 3.0 PoCL 4.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 15.0.7, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
    ==================================================================================================================================================
    * Device #1: cpu-sandybridge-Intel(R) Core(TM) i7-10700F CPU @ 2.90GHz, 2910/5884 MB (1024 MB allocatable), 4MCU

    Minimum password length supported by kernel: 0
    Maximum password length supported by kernel: 256

    Hashes: 1 digests; 1 unique digests, 1 unique salts
    Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates

    Optimizers applied:
    * Zero-Byte
    * Not-Iterated
    * Single-Hash
    * Single-Salt
    * Brute-Force

    Watchdog: Temperature abort trigger set to 90c

    Host memory required for this attack: 1 MB

    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiQlRMe180X0V5ZXN9IiwiaWF0Ijo5MDAwMDAwMCwibmFtZSI6IkdyZWF0RXhwIiwiYWRtaW4iOnRydWV9.jbkZHll_W17BOALT95JQ17glHBj9nY-oWhT1uiahtv8:bT!0

    Session..........: hashcat
    Status...........: Cracked
    Hash.Mode........: 16500 (JWT (JSON Web Token))
    Hash.Target......: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiQl...iahtv8
    Time.Started.....: Sun Dec 31 03:50:45 2023 (7 secs)
    Time.Estimated...: Sun Dec 31 03:50:52 2023 (0 secs)
    Kernel.Feature...: Pure Kernel
    Guess.Mask.......: ?a?a?a?a [4]
    Guess.Queue......: 1/1 (100.00%)
    Speed.#1.........:  2621.9 kH/s (6.10ms) @ Accel:128 Loops:47 Thr:1 Vec:8
    Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
    Progress.........: 16902144/81450625 (20.75%)
    Rejected.........: 0/16902144 (0.00%)
    Restore.Point....: 177664/857375 (20.72%)
    Restore.Sub.#1...: Salt:0 Amplifier:0-47 Iteration:0-47
    Candidate.Engine.: Device Generator
    Candidates.#1....: s5VH -> RT^a
    Hardware.Mon.#1..: Util: 95%

    Started: Sun Dec 31 03:50:44 2023
    Stopped: Sun Dec 31 03:50:53 2023
    ```
* John - [Hacking JWT Tokens: Bruteforcing Weak Signing Key (JohnTheRipper)](https://blog.pentesteracademy.com/hacking-jwt-tokens-bruteforcing-weak-signing-key-johntheripper-89f0c7e6a87)
    這要取決於wordlist有沒有，所以我只是先以secret=1234，然後用john爆破
    ![圖片](https://hackmd.io/_uploads/rkTfhsRDT.png)
    ```bash
    $ echo 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiQlRMe180X0V5ZXN9IiwiaWF0Ijo5MDAwMDAwMCwibmFtZSI6IkdyZWF0RXhwIiwiYWRtaW4iOnRydWV9.2kwB24fBrrmotFu9cdeRb1EMg1kRfGlLQPvhE1OUtp0'> jwt.txt
    $ john jwt.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=HMAC-SHA256                                                                                                                 
    Using default input encoding: UTF-8
    Loaded 1 password hash (HMAC-SHA256 [password is key, SHA256 128/128 AVX 4x])
    Will run 4 OpenMP threads
    Press 'q' or Ctrl-C to abort, almost any other key for status
    1234             (?)     
    1g 0:00:00:00 DONE (2023-12-31 03:46) 100.0g/s 409600p/s 409600c/s 409600C/s 123456..oooooo
    Use the "--show" option to display all of the cracked passwords reliably
    Session completed. 
    ```

:::spoiler Flag
Flag: `bT!0`
:::

## ==Q5==
> Can you generate a new verified signature ticket with a low privilege? (Format: String.String.String)

### Recon
我們知道了secrets===bT!0==，所以我們可以用這個secrets簽章新的payload
![圖片](https://hackmd.io/_uploads/ByhNToRvT.png)

:::spoiler Flag
Flag: `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiQlRMe180X0V5ZXN9IiwiaWF0Ijo5MDAwMDAwMCwibmFtZSI6IkdyZWF0RXhwIiwiYWRtaW4iOmZhbHNlfQ.nMXNFvttCvtDcpswOQA8u_LpURwv6ZrCJ-ftIXegtX4`
:::

## Reference
[^wp1]:[BTLO — Secrets Walkthrough](https://medium.com/@prajjwal029/btlo-secrets-5314312e4aef)