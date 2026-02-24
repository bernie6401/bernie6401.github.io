---
title: "How to use Mailgun/Resend as SMTP server"
tags: [Tutorial]

category: "Tutorial"
date: 2024-11-26
---

# How to use Mailgun/Resend as SMTP server
會有這個紀錄是因為deploy Mastodon Instance時需要用到SMTP Server，雖然是Optional，但還是嘗試建立一個試看看
<!-- more -->

## Prerequisite
* 有一台具有domain的device

## Mailgun Step 
1. 先到[官網](https://app.mailgun.com)註冊帳號
2. 在Sending > Domains中新增Domain，我是只有domain name，而不是包含subdomain
    ![圖片](https://hackmd.io/_uploads/HygMAixKM1g.png)
    其他參數不用改
    ![圖片](https://hackmd.io/_uploads/SyrSnlKG1l.png)
3. 進入到DNS records並且查看有哪些東西需要加進去到DNS的紀錄，以我的為例，因為我有開啟automatic sender security，所以有以下6個
    ![圖片](https://hackmd.io/_uploads/HkHA2gKM1x.png)
    包含3個CNAME，2個MX，一個TXT
    接著就到當初申請domain的網站，以我的為例是namesilo，新增這幾個紀錄，就是複製貼上，最後新增完如下
    ![圖片](https://hackmd.io/_uploads/r1CLpgYGkg.png)
4. 接著就一直等，由於DNS更新也會需要時間，所以mailgun要verify也可能要等很久，我大概是等了半小時才好，在Mailgun的Domain Setting頁面，會顯示所有的紀錄為Verified或是Active的字樣(如上上圖)
5. 接著就看哪一個service需要用到SMTP，以我的為例就是Mastodon Instance，他會建立一個.env.production，裡面就要放SMTP會用到的環境變數，如下
    ```
    SMTP_SERVER=smtp.mailgun.org
    SMTP_PORT=587
    SMTP_LOGIN=postmaster@sbk6401.sbs
    SMTP_PASSWORD=<your SMTP Password>
    SMTP_AUTH_METHOD=plain
    SMTP_OPENSSL_VERIFY_MODE=none
    SMTP_ENABLE_STARTTLS=auto
    SMTP_FROM_ADDRESS='Mastodon <notifications@mastodon.sbk6401.sbs>'
    ```
    首先解釋一下上面的變數
    SMTP_SERVER和SMTP_PORT建議不要改，login如果沒有特別指定，就是使用postmaster@\<your domain name\>，而password要到Mailgun的SMTP Credentials中，利用Reset Password並且複製新的密碼就可以貼上
    ![圖片](https://hackmd.io/_uploads/HyWxlWKfJx.png)
    而auto_method、openssl_verify和enable_starttls則是有其他的選項可以選，可以視情況自行使用，from_address則是看要用什麼身份傳送mail，我是直接使用mastodon的預設模式
6. Done!!!
    通常這樣沒有什麼問題的話就完成了，只要mastodon有出現任何被Follow、登入、被tag發文等操作，都應該要發送信件通知才對

## Resend Step
我發現在設定Bluesky的SMTP的時候，無法用mailgun當作server，不確定是什麼原因，但官方doc說建議用[Resend](https://resend.com)或是[SendGrid](https://sendgrid.com/)，然後和Mailgun設定的差不多，先新增一個自己的domain，然後他會給4個DNS config的紀錄(3個TXT和1個MX)
![image](https://hackmd.io/_uploads/ryI8KTzX1g.png)
就直接到自己當初申請domain的DNS Server設定，接下來就是等DNS server更新
![image](https://hackmd.io/_uploads/ByPKYaf7yx.png)
等到更新成功後，先申請API key，到API Keys > Create API Keys 建立SMTP的API，然後就可以開始填寫pds.env
```bash
$ vim /pds/pds.env

# Add the following to pds.env
PDS_EMAIL_FROM_ADDRESS="admin@bluesky.sbk6401.sbs"
PDS_EMAIL_SMTP_URL="smtps://resend:<my resend api key>@smtp.resend.org:465/"

$ systemctl restart pds
```