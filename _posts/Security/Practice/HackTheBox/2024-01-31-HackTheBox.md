---
title: HackTheBox
tags: [CTF, hackthebox]

category: "Security｜Practice｜HackTheBox"
date: 2024-01-31
---

# HackTheBox
<!-- more -->
[TOC]

## [Web Requests-GET](https://academy.hackthebox.com/module/35/section/247)

### Background
cURL - GET/Header

### Exploit
```bash
$ curl 'http://144.126.206.249:31846/search.php?search=flag' -H 'Authorization: Basic YWRtaW46YWRtaW4='
flag: HTB{curl_g3773r}
```

## [Web Requests-POST](https://academy.hackthebox.com/module/35/section/224)

### Background
cURL - POST/Cookie/Json Data/Header

### Exploit
```bash!
$ curl 'http://142.93.47.151:30718/search.php' -b 'PHPSESSID=darsv7lbe3aa22nv4v82h039p6' -X POST -d '{"search":"flag"}' -H 'Content-Type: application/json'
["flag: HTB{p0$t_r3p34t3r}"]%
```

## [Web Requests-CRUD](https://academy.hackthebox.com/module/35/section/227)

### Background

### Exploit
```bash!
# Read all the city
$ curl -s http://165.232.44.246:31084/api.php/city/ \| jq
[{"city_name":"London","country_name":"(UK)"},{"city_name":"Birmingham","country_name":"(UK)"},{"city_name":"Leeds","country_name":"(UK)"},{"city_name":"Glasgow","country_name":"(UK)"},{"city_name":"Sheffield","country_name":"(UK)"}...,{"city_name":"Baltimore","country_name":"(US)"}]%

# Update city Baltimore to flag
$ curl -X PUT http://165.232.44.246:31084/api.php/city/Baltimore -d '{"city_name":"flag", "country_name":"(US)"}' -H 'Content-Type: application/json'

# Delete any city
$ curl -X DELETE http://165.232.44.246:31084/api.php/city/Detroit

# Read city named flag to get flag
$ curl -s http://165.232.44.246:32034/api.php/city/ \| jqcurl -s http://165.232.44.246:31084/api.php/city/flag
[{"city_name":"flag","country_name":"HTB{crud_4p!_m4n!pul4t0r}"}]%
```

## [JavaScript Deobfuscation-Decoding](https://academy.hackthebox.com/module/41/section/445)

### Exploit
Use CypherChef First to decode `N2gxNV8xNV9hX3MzY3IzN19tMzU1NGcz`
```bash!
$ curl -s http://144.126.206.249:31094/serial.php -X POST -d "serial=7h15_15_a_s3cr37_m3554g3"
HTB{ju57_4n07h3r_r4nd0m_53r14l}
```

## [JavaScript Deobfuscation-Skills Assessment](https://academy.hackthebox.com/module/41/section/519)

### Exploit
1. Ans: `api.min.js`
2. Ans: `HTB{j4v45cr1p7_3num3r4710n_15_k3y}`
Use [online tool](http://jsnice.org/) to deobfuscate the code
3. Ans: `HTB{n3v3r_run_0bfu5c473d_c0d3!}`
Use [online tool](http://jsnice.org/) to deobfuscate the code
4. Ans: `4150495f70336e5f37333537316e365f31355f66756e`
    ```javascript
    'use strict';
    /**
     * @return {undefined}
     */
    function apiKeys() {
      /** @type {string} */
      var flag = "HTB{n" + "3v3r_" + "run_0" + "bfu5c" + "473d_" + "c0d3!" + "}";
      /** @type {!XMLHttpRequest} */
      var xhr = new XMLHttpRequest;
      /** @type {string} */
      var url = "/keys" + ".php";
      xhr["open"]("POST", url, !![]);
      xhr["send"](null);
    }
    console["log"]("HTB{j" + "4v45c" + "r1p7_" + "3num3" + "r4710" + "n_15_" + "k3y}");
    ```
    This main function is mainly send POST data to URL(`/keys.php`). So, we can simulate this action by burp suite or cURL.
    ![reference link](https://hackmd.io/_uploads/H1KFZyOY3.png)

5. Ans: `HTB{r34dy_70_h4ck_my_w4y_1n_2_HTB}`
Use CypherChef to decode the code we obtained above.
    ```bash
    $  curl -s http://165.232.42.76:32325/keys.php -X POST -d "key=API_p3n_73571n6_15_fun"
    HTB{r34dy_70_h4ck_my_w4y_1n_2_HTB}%
    ```

## [Getting Start-Service Scanning](https://academy.hackthebox.com/module/77/section/726)
:::info
Must use Ubuntu 18.04.6 LTS to connect SMB server
```bash!
$ sudo openvpn {ovpn file}
```
:::

### Background
NMAP/SMB
[Ubuntu SMB Command](https://blog.csdn.net/FruitDrop/article/details/66475465)
[Ubuntu SMB Command 2](https://www.itprotoday.com/linux/linuxs-smbclient-command#close-modal)

### Exploit
1. Ans: Apache Tomcat
2. Ans: 2323
    ```bash!
    $ nmap -sV 10.129.136.29
    Starting Nmap 7.80 ( https://nmap.org ) at 2023-07-10 15:56 CST
    Nmap scan report for 10.129.136.29
    Host is up (0.43s latency).
    Not shown: 993 closed ports
    PORT     STATE SERVICE     VERSION
    21/tcp   open  ftp         vsftpd 3.0.3
    22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
    80/tcp   open  http        Apache httpd 2.4.41 ((Ubuntu))
    139/tcp  open  netbios-ssn Samba smbd 4.6.2
    445/tcp  open  netbios-ssn Samba smbd 4.6.2
    2323/tcp open  telnet      Linux telnetd
    8080/tcp open  http        Apache Tomcat
    Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 55.86 seconds
    ```
3. Ans: `dceece590f3284c3866305eb2473d099`
* Check share name first
    ```bash!
    $ smbclient -N -L \\\\10.129.136.29
    WARNING: The "syslog" option is deprecated

            Sharename       Type      Comment
            ---------       ----      -------
            print$          Disk      Printer Drivers
            users           Disk
            IPC$            IPC       IPC Service (gs-svcscan server (Samba, Ubuntu))
    Reconnecting with SMB1 for workgroup listing.
    protocol negotiation failed: NT_STATUS_INVALID_NETWORK_RESPONSE
    Failed to connect with SMB1 -- no workgroup available 
    ```
* Login by user bob and get flag.txt
    ```bash!
    $ smbclient -U bob \\\\10.129.136.29\\users
    WARNING: The "syslog" option is deprecated
    Enter WORKGROUP\bob's password:
    Try "help" to get a list of possible commands.
    smb: \> dir
      .                                   D        0  Fri Feb 26 07:06:52 2021
      ..                                  D        0  Fri Feb 26 04:05:31 2021
      flag                                D        0  Fri Feb 26 07:09:26 2021
      bob                                 D        0  Fri Feb 26 05:42:23 2021
    cd f
                    4062912 blocks of size 1024. 1124740 blocks available
    smb: \> cd flag\
    smb: \flag\> get flag.txt
    getting file \flag\flag.txt of size 33 as flag.txt (0.0 KiloBytes/sec) (average 0.0 KiloBytes/sec)
    smb: \flag\> exit
    $ cat flag.txt
    dceece590f3284c3866305eb2473d099
    ```