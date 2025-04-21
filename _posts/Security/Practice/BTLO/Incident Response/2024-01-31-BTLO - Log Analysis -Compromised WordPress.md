---
title: BTLO - Log Analysis -Compromised WordPress
tags: [BTLO, Incident Response]

category: "Security/Practice/BTLO/Incident Response"
---

# BTLO - Log Analysis -Compromised WordPress
<!-- more -->
Challenge: https://blueteamlabs.online/home/challenge/log-analysis-compromised-wordpress-ce000f5b59

:::spoiler TOC
[TOC]
:::

## Scenario
> One of our WordPress sites has been compromised but we're currently unsure how. The primary hypothesis is that an installed plugin was vulnerable to a remote code execution vulnerability which gave an attacker access to the underlying operating system of the server. 

## Tools
Grep
Sort
Uniq
Apache Log Analyzer 

## ==Q1==
> Identify the URI of the admin login panel that the attacker gained access to (include the token)

### Recon
這個算是有用過wordpress就會知道的事情，預設的admin login的file name通常是`wp-login.php`，所以可以用這個當作key word

### Exploit
```bash
$ cat access.log | grep "wp-login.php" | more | grep "token" -n --color=auto
15:172.21.0.1 - - [12/Jan/2021:16:09:43 +0000] "GET /wp-login.php?itsec-hb-token=adminlogin HTTP/1.1" 200 2738 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
16:172.21.0.1 - - [12/Jan/2021:16:09:43 +0000] "GET /wp-includes/css/buttons.min.css?ver=5.6 HTTP/1.1" 200 1788 "http://172.21.0.3/wp-login.php?itsec-hb-token=adminlogin" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
17:172.21.0.1 - - [12/Jan/2021:16:09:43 +0000] "GET /wp-includes/css/dashicons.min.css?ver=5.6 HTTP/1.1" 200 36064 "http://172.21.0.3/wp-login.php?itsec-hb-token=adminlogin" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
...
```

:::spoiler Flag
Flag: `/wp-login.php?itsec-hb-token=adminlogin`
:::

## ==Q2==
> Can you find two tools the attacker used?

### Recon
這一題我是參考[^wp1]，因為access.log內部資料的格式都一樣，所以可以用cut這個指令切出每一塊相同的部分，再用`-f {number}`的參數挑出要哪一塊

### Exploit
```bash
$ cat access.log | cut -d '"' -f 6 | sort | uniq > aaa.txt
```
仔細觀察aaa.txt，會發現幾個熟悉的工具，包含sqlmap和wpscan，如果最後還是很多的話，還是可以搭配`$ grep -v {filter key word} -E {multi key word}`的方式減少結果

```bash
$ cat access.log | cut -d '"' -f 6| sort | uniq | grep -v -E "AH01276|Mozilla" --color=auto


-
Apache/2.4.38 (Debian) PHP/7.4.13 (internal dummy connection)
Apache/2.4.38 (Debian) PHP/7.4.14 (internal dummy connection)
Opera/9.00 (Windows NT 5.1; U; de)
WPScan v3.8.10 (https://wpscan.org/)
WordPress/5.6; http://172.21.0.3
[Thu Jan 14 06:04:08.466086 2021] [php7:error] [pid 84] [client 168.22.54.119:0] PHP Fatal error:  Uncaught Error: Call to undefined function Kadence\\get_header() in /var/www/html/wp-content/themes/kadence/index.php:10\nStack trace:\n#0 {main}\n  thrown in /var/www/html/wp-content/themes/kadence/index.php on line 10, referer: http://172.21.0.3/
[Thu Jan 14 06:05:30.750084 2021] [php7:error] [pid 99] [client 168.22.54.119:0] PHP Fatal error:  Uncaught Error: Call to undefined function Kadence\\get_header() in /var/www/html/wp-content/themes/kadence/index.php:10\nStack trace:\n#0 {main}\n  thrown in /var/www/html/wp-content/themes/kadence/index.php on line 10, referer: http://172.21.0.3/
[Thu Jan 14 07:42:17.055410 2021] [php7:error] [pid 22] [client 172.21.0.1:44924] script '/var/www/html/wp-login.php' not found or unable to stat
[Thu Jan 14 07:42:19.321162 2021] [php7:error] [pid 22] [client 172.21.0.1:44924] script '/var/www/html/wp-login.php' not found or unable to stat
[Thu Jan 14 07:42:22.533632 2021] [php7:error] [pid 22] [client 172.21.0.1:44924] script '/var/www/html/wp-login.php' not found or unable to stat
[Thu Jan 14 07:42:34.921671 2021] [php7:error] [pid 26] [client 172.21.0.1:44944] script '/var/www/html/wp-login.php' not found or unable to stat
[Thu Jan 14 07:42:37.012631 2021] [php7:error] [pid 26] [client 172.21.0.1:44944] script '/var/www/html/wp-login.php' not found or unable to stat
[Thu Jan 14 07:42:42.193155 2021] [php7:error] [pid 27] [client 172.21.0.4:59472] script '/var/www/html/wp-cron.php' not found or unable to stat, referer: http://172.21.0.3/wp-cron.php?doing_wp_cron=1610610161.9074409008026123046875
http://www.w3.org/1999/xhtml
python-requests/2.24.0
sh: 1: /usr/sbin/sendmail: not found
sqlmap/1.4.11#stable (http://sqlmap.org)
```

:::spoiler Flag
Flag: `wpscan sqlmap`
:::

## ==Q3==
> The attacker tried to exploit a vulnerability in ‘Contact Form 7’. What CVE was the plugin vulnerable to? (Do some research!)

### Recon
直接上網找Contact Form 7 CVE就會出現[CVE-2020-35489](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-35489)
> The contact-form-7 (aka Contact Form 7) plugin before 5.3.2 for WordPress allows Unrestricted File Upload and remote code execution because a filename may contain special characters.

:::spoiler Flag
Flag: `CVE-2020-35489`
:::

## ==Q4==
> What plugin was exploited to get access?

### Recon
這一題可以搭配grep做出比較精確的filtering，我們想要找出plugins的部分，所以先grep出`/plugins/`的關鍵字，再用上面新學到的方式進階filter，到最後就只有一小部分的數量而已，
```bash
cat access.log | grep '/plugins/' | cut -d '/' -f 6 | sort | uniq

%20contact-form-7%20
%2e
.
WP_Estimation_Form
accessally
ait-csv-import-export
akismet
basic-contact-form
better-wp-security
contact-form-7
contact-form-7%20
contact-form-7..;
contact-form-7?
contact-form-7??
crelly-slider
indeed-membership-pro
loginizer
plugins
product-lister-walmart
simple-file-list
social-photo-gallery
tinymce
trx_addons
woocommerce-checkout-manager
wordpress-seo
wp-advanced-search
wp-live-chat-support-pro
```
:::info
Format: Plugin Name Here X.X.X
後面的X代表版本號
:::
依序上網搜尋對應的plugin，剛好看到Simple File List有一個版本4.2.2是有任意上傳檔案的洞[Exploit DB - Simple File List](https://www.exploit-db.com/exploits/48979)

:::spoiler Flag
Flag: `Simple File List 4.2.2`
:::

## ==Q5==
> What is the name of the PHP web shell file?

### Recon
透過上一題我們知道該網站有一個任意上傳的洞，所以我們該找的是uploads這個key words，必且搭配前面學的filtering就可以找出奇異的檔案
```bash
$ cat access.log | grep '/uploads/' | cut -d '/' -f 8 | sort | uniq

1.1" 200 1213 "http:
1.1" 200 1295 "-" "Mozilla
1.1" 200 215 "http:
1.1" 200 4672 "http:
1.1" 200 4789 "http:
1.1" 200 5356 "http:
1.1" 200 5357 "http:
1.1" 200 5436 "http:
1.1" 200 5588 "http:
1.1" 200 5754 "http:
1.1" 200 6513 "http:
1.1" 200 84690 "-" "python-requests
1.1" 403 455 "http:
1.1" 404 29045 "http:
1.1" 404 335 "http:
1.1" 404 488 "-" "Mozilla
fr34k.png HTTP
test.png HTTP
```

:::spoiler Flag
Flag: `fr34k.php`
:::

## ==Q6==
> What was the HTTP response code provided when the web shell was accessed for the final time?

### Recon
從前面我們知道了web shell的檔名，那我們就可以針對該檔案進行grep
```bash
$ cat access.log | grep 'fr34k' | cut -d '"' -f 3
 404 29045
 200 84690
 200 1295
 200 1213
 200 1213
 200 5436
 200 5356
 200 5588
 200 4672
 200 5357
 200 5754
 200 5356
 200 6513
 200 5357
 200 5357
 200 4789
 200 5357
 200 215
 404 488
```
可以看到最後一筆是404的狀態

### Exploit
:::spoiler Flag
Flag: `404`
:::

## Reference
[^wp1]:[Log Analysis -Compromised WordPress — BTLO, WriteUp](https://systemweakness.com/log-analysis-compromised-wordpress-btlo-writeup-5effda72462c)