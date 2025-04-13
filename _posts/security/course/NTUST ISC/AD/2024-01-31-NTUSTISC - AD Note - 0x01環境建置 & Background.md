---
title: NTUSTISC - AD Note - 環境建置 & Background
tags: [AD, information security, NTUSTISC]

category: "Security/Course/NTUST ISC/AD"
---

# NTUSTISC - AD Note - 環境建置 & Background
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=SycYwgWohlu97dc3)

## Background
* What is Directory Service?[^fei-directory-service]
    > ![](https://i.imgur.com/QVJYCoG.jpg)
    > Windows Server 系統使用的目錄服務 就是 Active Directory
* What is Active Directory(AD)?[^wiki-Active-Directory]
    > Windows的Windows Server中，負責架構中大型網路環境的集中式目錄管理服務(Directory Services)，他處理在組織中的網路物件，物件可以是<font color="FF0000">使用者、群組、電腦、網域控制站、郵件、設定檔、組織單元、樹系</font>等等，只要是在AD結構定義檔(Schema)中定義的物件，就可以儲存在AD資料檔中，並利用AD Service Interface來存取

* What is Domain Service?[^fei-directory-service]
    > ![](https://i.imgur.com/k2ma2Nf.jpg)
    > 執行 AD DS 的伺服器稱為 domain controllers (DCs)
* What is LDAP?[^aws-what-is-ldaps]
    :::info
    > 輕量型目錄存取協定 (LDAP) 是用來從 Active Directory 讀取資料，及將資料寫入 Active Directory 的標準協定。某些應用程式使用 LDAP 新增、移除或搜尋 Active Directory 中的使用者和群組，或是傳輸登入資料來驗證 Active Directory 中的使用者。每個 LDAP 通訊都包括用戶端 (如應用程式) 和伺服器 (例如 Active Directory)。
    :::
* What is Organization Units(OU)?[^fei-organization-units]
    > 容區(Container)：屬性集合，跟物件不同是容器可以包含多個「物件」
    > 組織單位(Organization Units)：特殊容區，可包含其他物件、組織單位、群組原則
* What is Group Policy Object(GPO)?[^upas1030-gpo]
    > 群組原則是透過群組原則物件(Group Policy Object,GPO)來設定，你要只要將GPO連結到指定的網域，此GPO內的設定值就會影響到該網域內的所有使用者與電腦。
    > ### 內建GPO
    > AD DS網域有兩個內建的GPO
    > 1. Default Domain Policy:此GPO預設已備連結到網域，因此其設定值會套用到整個網域內的所有使用者與電腦。
    > 2. Default Domain Controller Policy:此GPO預設已被連到組織單位Domain Controllers，因此其設定值會被套用到Domain Controllers內所有的使用者與電腦
    > (Domain Controllers 內預設只有網域控制站的電腦帳戶。)


## 環境建置
:::info
這一整個lab雖然是從講師的drive下載下來的(連結爛掉了，有需要可以跟我拿)，但還是可以從網路中自己創一個有這麼多漏洞的lab環境。可以先安裝win2016的虛擬機，然後到[WazeHell/vulnerable-AD](https://github.com/WazeHell/vulnerable-AD)下載script，在該環境中跑起來，就可以了，不果因為跑完之後的所有帳號或密碼都是隨機的，所以如果要看別人或是後續我寫的WP會有點困難
:::

### 實驗環境拓樸
![](https://hackmd.io/_uploads/B14swTr62.png)

### 帳號密碼
* Win10(Client)
帳號：administrator
密碼：1qaz@WSX3edc
    * 一般的網域帳號
    帳號：bear
    密碼：1qaz@WSX3edc
    * 低權限帳號
    帳號：low
    密碼：<無>
* Win2016(DC)
帳號：administrator
密碼：1qaz@WSX3edc
* ==Note==
    :::info
    如果要指定本機端的帳戶進行登入，可以在帳號前面加入`.\`的符號或是直接寫主機名稱，強制用本地端的帳號登入，這個帳戶就是沒有加入AD domain底下
    :::

### 詳細步驟
1. 把講師提供的兩支VM(win10/win2016)灌起來並自行下載[kali2022](https://old.kali.org/kali-images/kali-2022.4/)，==建議用VMware==
2. 啟用Neo4j & BloodHound
    因為環境目前預設的JDK version是1.8，所以如果啟用後續會用到的Neo4j會出問題，所以我們要先改java版本，改成JDK-11，比較詳細的流程可以參考[^neo4j-java-error]
    1. Uninstall JDK-1.8
    2. Download JDK-11 & Install it([Link](https://www.oracle.com/tw/java/technologies/javase/jdk11-archive-downloads.html))
        * 下載之前會需要你登入Oracle帳號
        * 如果想要知道哪一個版本的JAVA對應到哪一個版本的Neo4j，可以從這邊[^neo4j-java]找，照法就是在網址的地方中間有一個neo4j的版本，打上你的neo4j版本，他就會到對應的頁面告訴你JAVA的版本應該是多少，例如我的版本是4.3，就打上`https://neo4j.com/docs/operations-manual/4.3/installation/requirements/`，不過他也只有分3.x和4.x
        ![](https://hackmd.io/_uploads/r1_7srupn.png)
    3. Modify Environment Variable
        * 更改環境變數這件事情一定要在Win10加入AD之前做的原因是，只要加入AD就無法改變環境變數的系統變數(如下圖)，那我有想過把Win10直接退掉AD的網域，不過過程困難重重，所以我想還是直接開一個新的Win10從頭來會比要快，而且加入AD後還不能連網，畢竟DNS都被改掉了，會很不方便
        ![](https://hackmd.io/_uploads/rJOVhBda3.png)
        * 首先要在系統變數的地方新增JAVA_HOME然後value就是當初安裝JDK-11的位置
        ![](https://hackmd.io/_uploads/Sy-fTr_a2.png)
        * 並在Path中新增`%JAVA_HOME%\bin`和`<JDK-11 path to bin>`並按下確定後到Command Prompt確認有沒有成功
        ![](https://hackmd.io/_uploads/BkbYTHOp2.png)
        ![](https://hackmd.io/_uploads/Syb-0BOa2.png)
    4. Activate Neo4j
        在neo4j的目錄中進到bin，然後打開cmd，輸入`$ neo4j.bat console`，理論上前面有做對，應該就會開啟Neo4j的服務
        :::spoiler Activate Neo4j Log
        ```bash
        C:\tools\neo4j-community-4.3.4\bin>neo4j.bat console
        Directories in use:
        home:         C:\tools\neo4j-community-4.3.4
        config:       C:\tools\neo4j-community-4.3.4\conf
        logs:         C:\tools\neo4j-community-4.3.4\logs
        plugins:      C:\tools\neo4j-community-4.3.4\plugins
        import:       C:\tools\neo4j-community-4.3.4\import
        data:         C:\tools\neo4j-community-4.3.4\data
        certificates: C:\tools\neo4j-community-4.3.4\certificates
        licenses:     C:\tools\neo4j-community-4.3.4\licenses
        run:          C:\tools\neo4j-community-4.3.4\run
        Starting Neo4j.
        2023-08-27 03:48:08.068+0000 INFO  Starting...
        2023-08-27 03:48:10.649+0000 INFO  ======== Neo4j 4.3.4 ========
        2023-08-27 03:48:12.832+0000 INFO  Initializing system graph model for component 'security-users' with version -1 and status UNINITIALIZED
        2023-08-27 03:48:12.848+0000 INFO  Setting up initial user from defaults: neo4j
        2023-08-27 03:48:12.848+0000 INFO  Creating new user 'neo4j' (passwordChangeRequired=true, suspended=false)
        2023-08-27 03:48:12.870+0000 INFO  Setting version for 'security-users' to 3
        2023-08-27 03:48:12.870+0000 INFO  After initialization of system graph model component 'security-users' have version 3 and status CURRENT
        2023-08-27 03:48:12.870+0000 INFO  Performing postInitialization step for component 'security-users' with version 3 and status CURRENT
        2023-08-27 03:48:13.274+0000 INFO  Bolt enabled on 127.0.0.1:7687.
        2023-08-27 03:48:14.472+0000 INFO  Remote interface available at http://localhost:7474/
        2023-08-27 03:48:14.472+0000 INFO  Started.
        2023-08-27 03:51:44.289+0000 WARN  The client is unauthorized due to authentication failure.
        ```
        :::
        接著進到`http://localhost:7474/`，輸入預設帳密`neo4j/neo4j`，最後改密碼就好了
        ![](https://hackmd.io/_uploads/Syof1Uupn.png)
    5. Activate BloodHound
        進到BloodHound/bin目錄然後執行`BloodHound.exe`輸入neo4j的帳密，就可以進到一個全新的bloodhound頁面
        ![](https://hackmd.io/_uploads/S1O51Idp2.png)

3. 把Win10加入AD
    1. Check Win2016 IP - `192.168.183.129`
        ![](https://hackmd.io/_uploads/SJds2L8p3.png)
    2. 將Win10的DNS指向AD
    主要目的就是把Win10網卡的DNS指向前面找到的Domain，在`設定/網路和網際網路/狀態/變更介面卡選項/乙太網路/內容/網際網路通訊協定第4版(TCP/IPV4)/內容`就可以找到更改的地方，然後把Win2016的IP填入
    ![](https://hackmd.io/_uploads/SkcaAU8T2.png)
    3. 更改Win10網域
    從`控制台/系統及安全性/系統/變更設定/變更`中更改網域成<font color="ff0000">`kuma.org`</font>，填入帳密按確定就可以了
    ![](https://hackmd.io/_uploads/rkJPJD86n.png)
    4. Restart Win10
    5. 使用網域帳號登入
    用bear這個帳號登入Win10
        :::spoiler Result
        ![](https://hackmd.io/_uploads/rktozsvph.png)
        可以看到系統資訊中，網域的部分已經變成kuma.org
        :::

## Reference
[^fei-directory-service]:[AD Security - [Day2] 一起來學 AD 安全吧！：什麼是 AD(1) ](https://ithelp.ithome.com.tw/articles/10292831)
[^wiki-Active-Directory]:[Active Directory](https://zh.wikipedia.org/zh-tw/Active_Directory)
[^aws-what-is-ldaps]:[啟用安全 LDAP (LDAPS)](https://docs.aws.amazon.com/zh_tw/directoryservice/latest/admin-guide/ms_ad_ldap.html)
[^fei-organization-units][AD Security - [Day5] 一起來學 AD 安全吧！：什麼是 AD(3) Container & OU & Security Group ](https://ithelp.ithome.com.tw/articles/10295116)
[^upas1030-gpo]:[GPO概念](https://upas1030.pixnet.net/blog/post/116192137)
[^neo4j-java]:[
System requirements
](https://neo4j.com/docs/operations-manual/4.0/installation/requirements/)
[^neo4j-java-error]:[當安裝Neo4j後，在cmd中輸入neo4j遇到(ERROR!Neo4j cannot be started using java version 1.8.0_211](https://blog.csdn.net/Linsice/article/details/129748823)