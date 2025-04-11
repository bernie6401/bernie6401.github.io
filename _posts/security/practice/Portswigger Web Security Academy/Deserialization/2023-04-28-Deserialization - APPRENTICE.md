---
title: Deserialization - APPRENTICE
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/Deserialization"
---

# Deserialization - APPRENTICE
###### tags: `Portswigger Web Security Academy` `Web`

## Lab: Modifying serialized objects
* Description: This lab uses a serialization-based session mechanism and is vulnerable to privilege escalation as a result.
* Goal: To solve the lab, edit the serialized object in the session cookie to exploit this vulnerability and gain administrative privileges. Then, delete Carlos's account.
You can log in to your own account using the following credentials: wiener:peter

### Recon
1. Login First & Recon the package
According to the description, we know that the user verification has insecure deserialization. Therefore, we can recon the package first as below.
![](https://i.imgur.com/zuKHXRF.png)
You can notice the session is a base64-encoded string and we use the built-in feature in burp suite to decode it.
Session: `Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d`
Decoded String: `O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}`
2. How about Modify the session directly
![](https://i.imgur.com/Ent5yuu.png)


### Exp - Change Directly
1. We can use the built-in feature to change our session to `admin=1` directly to then send it forward.
    :::info
    Each package may contain the session that should be modified. So, pay attention to before sending it forward
    :::
2. Delete Carlos
![](https://i.imgur.com/9KGxgZD.png)

:::spoiler Success Screenshot
![](https://i.imgur.com/eQEfiaw.png)
:::