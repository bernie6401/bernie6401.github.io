---
title: A&D of Network Security - Lab 14
tags: [NTU, NTU_PADNS]

category: "Security Course｜NTU PADNS"
date: 2023-05-30
---

# A&D of Network Security - Lab 14
<!-- more -->
###### tags: `Practicum of A&D of NS` `NTU`

## Video
* [Class Description](https://files-1.dlc.ntu.edu.tw/cool-video/202305/f4f0b276-7211-448a-812b-89b3d194ccde/transcoded.mp4?AWSAccessKeyId=C6ueMrUe5JyPkWQJAyKp&Expires=1685444669&Signature=XXKzQ0FHD31E%2FdKWhlcyX%2BcLQXg%3D)
* [Lab Implementation](https://files-1.dlc.ntu.edu.tw/cool-video/202305/b494d4d3-0d67-4672-95ab-37a8c35b70b3/transcoded.mp4?AWSAccessKeyId=C6ueMrUe5JyPkWQJAyKp&Expires=1685432006&Signature=sJvf4b%2BWXnkZY3dCFmX4vHCcyy0%3D)

## Background
* snort Rule
    * Rule Screenshot
    * Format
    ![](https://hackmd.io/_uploads/S1pKEV7Ln.png)
    * Action
    ![](https://hackmd.io/_uploads/HygsNEXI2.png)
    * Option
    ![](https://hackmd.io/_uploads/By83VNQUh.png)
    * Option - Payload
    ![](https://hackmd.io/_uploads/rJ6p44QI2.png)

## Lab
### Lab 1: Packet sniffer Mode show出 sniff ICMP封包的結果
Payload:
```bash
$ sudo snort -vd -i eth0 -q
```
![](https://hackmd.io/_uploads/BJVrHN78h.png)

---

### Lab 2: Attacker SSH爆破攻擊，利用 Snort偵測攻擊行為是否發生，show出偵測結果 ，並說明snort rule
#### Threat Model
![](https://hackmd.io/_uploads/SkDltNQU3.png)
* Attacker use SSH brute force attack and try to log in the victim snort
* Need to write rule to detect attacker’s SSH brute force attack

#### Lab Process
1. Set up environment - <font color="FF0000">Host Only</font>
    * In Kali-Linux 1(Attacker) - `192.168.56.129`
        ![](https://hackmd.io/_uploads/Hkd6FEmI3.png)
    * In Kali-Linux 2(Victim) - `192.168.56.104`
        ![](https://hackmd.io/_uploads/HkoYt4QU2.png)
        
2. Write your rule and Test it in victim VM
    
    Payload:
    ```bash
    $ sudo vim /etc/snort/rules/local.rules

    # Insert rules below in this file
    alert tcp any any -> any 22 ( msg:"SSH Brute Force Attempt"; flow:established,to_server; content:"SSH"; nocase; offset:0; depth:4; detection_filter:track by_src, count 2, seconds 1; sid:1000001; rev:1;)

    # Test the rule if success
    $ sudo snort -T -c /etc/snort/snort.conf
    ...
    Snort successfully validated the configuration!
    Snort exiting
    ```

3. Check SSH Connection if turn on (From inactive to active)
    ```bash
    $ sudo systemctl status ssh
    ● ssh.service - OpenBSD Secure Shell server
         Loaded: loaded (/lib/systemd/system/ssh.service; disabled; vendor preset: disabled)
         Active: inactive (dead)
           Docs: man:sshd(8)
                 man:sshd_config(5)
    $ sudo systemctl start ssh
    $ sudo systemctl status ssh
    ● ssh.service - OpenBSD Secure Shell server
         Loaded: loaded (/lib/systemd/system/ssh.service; disabled; vendor preset: disabled)
         Active: active (running) since Tue 2023-05-30 05:04:10 EDT; 2s ago
           Docs: man:sshd(8)
                 man:sshd_config(5)
        Process: 2670 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
       Main PID: 2671 (sshd)
          Tasks: 1 (limit: 9466)
         Memory: 1.1M
            CPU: 15ms
         CGroup: /system.slice/ssh.service
                 └─2671 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
    ```
4. Run snort in victim
    ```bash
    $ sudo snort -A console -q -c /etc/snort/snort.conf -i eth0
    ```

5. Activate Attacking in Attacker VM
    ```bash
    $ sudo hydra -l root -P /usr/share/wordlists/rockyou.txt 192.168.56.104 -t 4 ssh
    ```
6. Result Screenshot in Victim VM
    ![](https://hackmd.io/_uploads/SJ0U0VmUh.png)

---

### Lab 3-1: 使用Nmap進行攻擊並使用 Wireshark側錄封包分析可能可以成為snort的規則
#### Threat Model
![](https://hackmd.io/_uploads/H1LrJHQ83.png)
1. Nmap to the snort machine. (Any Nmap scan command is available)
2. Write your own Rules on the snort machine
3. Screenshot the output alert

#### Lab Process
1. Open Wireshark and Record the packets and choose `any` to record
    ```bash
    $ sudo wireshark
    ```
    ![](https://hackmd.io/_uploads/S1WJxrmLn.png)

2. Try to attack in attacker VM
    ```bash
    $ sudo nmap sS 192.168.56.129
    ```
    ![](https://hackmd.io/_uploads/rk3cCEQIn.png)

---

###  Lab 3-2: 撰寫snort rule並偵測出攻擊，偵測的 lert需包含你的學號
From the result above, try to observe the common rules of these <font color="FF0000">Red</font> packets(unsuccessful packets) $\to$ The length of each packets are $0$

Thus, we can use it to construct the snort payload as below(just insert the payload to `/etc/snort/rules/local.rules`):
```bash
alert tcp any any -> any any (msg: "<student id>: TCP Scan Alert"; sid:1000002;dsize:<5;)
```

#### Try to attack
In victim VM:
```bash
$ sudo snort -A console -q -u snort -g snort -c /etc/snort/snort.conf -i eth0
```

In attacker VM:
```bash
$ sudo nmap sS 192.168.56.104
```

![](https://hackmd.io/_uploads/Sy8hCNQI2.png)