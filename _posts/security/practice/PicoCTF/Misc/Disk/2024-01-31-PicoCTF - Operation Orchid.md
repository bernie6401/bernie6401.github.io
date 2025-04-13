---
title: PicoCTF - Operation Orchid
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/Disk"
---

# PicoCTF - Operation Orchid
<!-- more -->

## Recon
這一題過於簡單

## Exploit - Forensics / Openssl
1. Find Encryption Flag File(Autopsy)
可以在/root中找到，然後.ash_history的command紀錄中知道加密的password phrase
    ![](https://hackmd.io/_uploads/rJdlBhLgp.png)
    
    ```bash
    touch flag.txt
    nano flag.txt 
    apk get nano
    apk --help
    apk add nano
    nano flag.txt 
    openssl
    openssl aes256 -salt -in flag.txt -out flag.txt.enc -k unbreakablepassword1234567
    shred -u flag.txt
    ls -al
    halt
    ```
2. Script
    ```bash
    $ openssl aes-256-cbc -in flag.txt.enc -d
    enter aes-256-cbc decryption password:
    *** WARNING : deprecated key derivation used.
    Using -iter or -pbkdf2 would be better.
    bad decrypt
    140342062343488:error:06065064:digital envelope routines:EVP_DecryptFinal_ex:bad decrypt:crypto/evp/evp_enc.c:612:
    picoCTF{h4un71ng_p457_5113beab}%
    ```