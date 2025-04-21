---
title: CyberDefender - PsExec Hunt
tags: [CyberDefender, Network Forensics]

category: "Security/Practice/CyberDefender/Network Forensic"
---

# CyberDefender - PsExec Hunt
<!-- more -->
:::spoiler
[TOC]
:::

## Scenario
> Our Intrusion Detection System (IDS) has raised an alert, indicating suspicious lateral movement activity involving the use of PsExec. To effectively respond to this incident, your role as a SOC Analyst is to analyze the captured network traffic stored in a PCAP file.

## ==Q1==
> In order to effectively trace the attacker's activities within our network, can you determine the IP address of the machine where the attacker initially gained access? 

### Recon
我判斷的方式很簡單，就直接從endpoints看封包數量，選最多或是前幾多的IP就對了

### Exploit
![](https://hackmd.io/_uploads/SJA8VgrM6.png)

Flag: `10.0.0.130`

## ==Q2==
> To fully comprehend the extent of the breach, can we determine the machine's hostname to which the attacker pivoted? 

### Recon
這一題找超久，題目要找到攻擊者所轉向的電腦主機名稱，首先聚焦在問題中提到的hostname，我一直以為是Browser的host name，但看起來他不是這個意思
![](https://hackmd.io/_uploads/B16zT8BfT.png)
我先用export看他哪時候把psexec放到該主機上，可見最早放到主機上的時間是packet #192，所以直覺應該是往前找，畢竟要先把該主機compromised才能做後續的操作
![](https://hackmd.io/_uploads/HyGEC8Hza.png)

### Exploit
慢慢找會發現packet #131的target name字數剛好和答案相同，不過也和一開始的猜想大致相同，也就是*-PC代表hostname
Filter: `ntlmssp.challenge.target_name == "SALES-PC"`
![](https://hackmd.io/_uploads/BJHgP-rz6.png)

Flag: `SALES-PC`

## ==Q3==
> After identifying the initial entry point, it's crucial to understand how far the attacker has moved laterally within our network. Knowing the username of the account the attacker used for authentication will give us insights into the extent of the breach. What is the username utilized by the attacker for authentication? 

### Recon
這一題是找最久的，因為沒有和前面連起來，不然其實應該很快就找到，如果把filter去掉，然後看packet #131左右的其他packet會發現NTLM的authentication user name，這就是這一題的答案，我找到最後還想說用regular expression dump出英文字母六碼的所有結果，最後當然也是沒有然後
![](https://hackmd.io/_uploads/SkPvZDrGT.png)

Flag: `ssales`

## ==Q4==
> After figuring out how the attacker moved within our network, we need to know what they did on the target machine. What's the name of the service executable the attacker set up on the target? 

### Recon
這一題就很簡單了，可以看第二題所得知的export file，他會把所有機器之間通訊的檔案以及hostname/filename都呈現出來，因此這一題很明顯就是`PSEXESVC`

Flag: `PSEXESVC`

## ==Q5==
> We need to know how the attacker installed the service on the compromised machine to understand the attacker's lateral movement tactics. This can help identify other affected systems. Which network share was used by PsExec to install the service on the target machine? 

### Recon
題目想知道攻擊者選擇哪個network share安裝psexec，所以直覺會想到要用看主機之間傳送的檔案紀錄

### Exploit
呈第二題，既然知道最早是從packet #192把該檔案透過\\\ADMIN\$帳號傳送給別台主機，則答案應該就是`ADMIN$`

Flag: `ADMIN$`

## ==Q6==
> We must identify the network share used to communicate between the two machines. Which network share did PsExec use for communication? 

### Recon
題目想知道psexec是用哪個network share進行通訊，也是直覺可以從smb的檔案之間的紀錄下手

### Exploit
可以看到`\\IPC$`所傳送的filename包含stdout/stdin/stderr，所以基本上應該就是該帳號在進行通訊

Flag: `IPC$`

## ==Q7==
> Now that we have a clearer picture of the attacker's activities on the compromised machine, it's important to identify any further lateral movement. What is the machine's hostname to which the attacker attempted to pivot within our network? 

### Recon
題目想知道後續的橫向移動的目標是哪一題主機，並指出hostname為何，所以可以從packet #192往後找，或是我們可以直接下filter:`ntlmssp.ntlmv2_response.nb_domain_name`，就可以知道

### Exploit
要注意的是，NTLM中的NetBIOS Domain Name貌似和SMB2 Host是不一樣的，NTLM中的domain name應該是連接smb的那台主機所處的domain name為何，而smb2 host應該是被連接的那台機器所處的domain，可能是一台印表機之類的，這樣想就蠻合理的，而題目要我們找的是ntlm domain的hostname
![](https://hackmd.io/_uploads/BJkUUvHMT.png)

Flag: `MARKETING-PC`
