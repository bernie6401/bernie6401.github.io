---
title: A&D of Network Security - Lab 3
tags: [NTU, NTU_PADNS]

category: "Security｜Course｜NTU PADNS"
date: 2023-05-25
---

# A&D of Network Security - Lab 3
<!-- more -->
###### tags: `Practicum of A&D of NS` `NTU`

## Background
Network setting type in virtual box
![](https://i.imgur.com/g2J83Xg.png)


## Ping two machine in internal mode
:::spoiler Detailed Process
1. Clone another VM
![](https://i.imgur.com/vsI7lWa.png)
2. Setting Network Configuration
![](https://i.imgur.com/OqZ9Owm.png)
Setting 2 VMs' network config as above.
**Note that**, must check MAC address is different, promiscuous mode is `Allow All` and the adapter is the same.
3. Check ifconfig
    ![](https://i.imgur.com/91Ab7Cv.png)

    ![](https://i.imgur.com/kyutuue.png)

4. Ping each other
    ![](https://i.imgur.com/BWKJoNX.png)
    
    ![](https://i.imgur.com/TjgV49I.png)
:::

## Test Communication between bridged VMs on Different Hosts
:::spoiler Detailed Process
1. Setting Bridged Adapter of each VM
![](https://i.imgur.com/yhRpgtB.png)
**Note that**, the adapter must be the same.
2. Check ifconfig
    ![](https://i.imgur.com/N518AnH.png)
    
    ![](https://i.imgur.com/Aglx8eC.png)
    It should be the same of sub-ip as your true machine
    ![](https://i.imgur.com/VVDmB30.png)
3. Ping
![](https://i.imgur.com/mKQyTNe.png)
:::

## Reconstruct ARP cache by iteratively PING all subnet IP addresses
Objective: scanning all the machine in the same LAN

### Note
DO NOT EXECUTE IN DORM... YOU'LL BE BANNED...

### Source Code
```bash=
#!/bin/bash

# ping all ip addresses in the local network
for ip in 192.168.0.{1..254}; do
	# delete old arp records
	sudo arp -d $ip > /dev/null 2>&1
	# get new arp info by ping
	ping -c 5 $ip > /dev/null 2>&1 &
done

# wait for all ping processes to finish
wait

# show scan results (arp table)
arp -n | grep -v incomplete
```

### Detailed Process
:::spoiler Detailed Process
1. Setting to Host-Only Adapter
![](https://i.imgur.com/GFJ1uBY.png)
2. Check ifconfig
It should be the same as your real machine
![](https://i.imgur.com/w5y4LvM.png)

    ![](https://i.imgur.com/Mhrs1sl.png)

    ![](https://i.imgur.com/qPj9gry.png)
3. Setting the code
    ```bash=
    $ sudo dos2unix arpscan.sh
    $ sudo chmod 777 arpscan.sh
    $ vim arpscan.sh
    # modify the sub-ip as the same as your real machine, i.e. 192.168.56.{1..254}
    $ sudo bash arpscan.sh
    ```
    ![](https://i.imgur.com/6IJNeYb.png)
:::

## Testing Communication between VMs on Different Hosts using NAT
Objective: Find another physical computer and open web service on each PC then use port forwarding to connect the web service to each other.

:::spoiler Detailed Process
1. Find another physical computer and connect your own network
2. Set to NAT mode
![](https://i.imgur.com/S0DlK7c.png)
3. Check your physical computer and VM's ip
    ![](https://i.imgur.com/TXTh6SE.png)

    ![](https://i.imgur.com/g3eoBft.png)
4. Turn off VM and set port forwarding
![](https://i.imgur.com/bZA3dYz.png)
5. Open your web service
    ```bash!
    $ sudo service apache2 start
    ```
    Then test if the service is open or not in local host
    ![reference link](https://i.imgur.com/qeRdYEw.png)
6. Start to let somebody else to query your service
![](https://i.imgur.com/GHH2pdr.png)
OR...
You can edit the content of `index.html` and the result is as below.
    ```bash!
    $ cd /var/www/html
    $ sudo rm index.html
    $ sudo touch index.html
    $ sudo vim index.html
    # Just write `It works on VM1!!!` and saved it
    ```
    ![](https://i.imgur.com/qsa8cuM.png)
:::