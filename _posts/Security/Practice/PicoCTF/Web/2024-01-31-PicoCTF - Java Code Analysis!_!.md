---
title: PicoCTF - Java Code Analysis!?!
tags: [PicoCTF, CTF, Web]

category: "Security｜Practice｜PicoCTF｜Web"
---

# PicoCTF - Java Code Analysis!?!
<!-- more -->

## Background
JWT

## Source code
Too Much to list

## Hint
* Maybe try to find the JWT Signing Key ("secret key") in the source code? Maybe it's hardcoded somewhere? Or maybe try to crack it?
* The 'role' and 'userId' fields in the JWT can be of interest to you!
* The 'controllers', 'services' and 'security' java packages in the given source code might need your attention. We've provided a README.md file that contains some documentation.
* Upgrade your 'role' with the new (cracked) JWT. And re-login for the new role to get reflected in browser's localStorage.

## Recon
這一題在AIS3 pre-exam的時候也有看到，但當時根本沒想法，只要題目看起來一複雜我就沒辦法分析了，所以還是看了Martin大的WP才知道解法，但有時候真的很考驗耐心，先看hint發現應該是考跟JWT有關
1. 先用user/user登入觀察整個網站
發現書架上只有三本書，而且個別的權限都標註在上面(Free/Premium/Admin)，看起來我們的目標是把自己的權限變成admin然後查看flag這本書
![](https://hackmd.io/_uploads/BJJYLGuO3.png)
2. JWT Token
用[online tool](https://jwt.io/)查看的結果如下，首要目標是找到HS256的secret key
![](https://hackmd.io/_uploads/SkMdvf__3.png)


## Exploit - JWT
1. 找Secret key
隨便找找，發現在`./src/main/java/io/github/nandandesai/pico/security/models/SecretGenerator.java`的SecretGenerator class
    :::spoiler Source Code
    ```java!
    package io.github.nandandesai.pico.security;

    import io.github.nandandesai.pico.configs.UserDataPaths;
    import io.github.nandandesai.pico.utils.FileOperation;
    import org.slf4j.Logger;
    import org.slf4j.LoggerFactory;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.stereotype.Service;

    import java.io.IOException;
    import java.nio.charset.Charset;

    @Service
    class SecretGenerator {
        private Logger logger = LoggerFactory.getLogger(SecretGenerator.class);
        private static final String SERVER_SECRET_FILENAME = "server_secret.txt";

        @Autowired
        private UserDataPaths userDataPaths;

        private String generateRandomString(int len) {
            // not so random
            return "1234";
        }

        String getServerSecret() {
            try {
                String secret = new String(FileOperation.readFile(userDataPaths.getCurrentJarPath(), SERVER_SECRET_FILENAME), Charset.defaultCharset());
                logger.info("Server secret successfully read from the filesystem. Using the same for this runtime.");
                return secret;
            }catch (IOException e){
                logger.info(SERVER_SECRET_FILENAME+" file doesn't exists or something went wrong in reading that file. Generating a new secret for the server.");
                String newSecret = generateRandomString(32);
                try {
                    FileOperation.writeFile(userDataPaths.getCurrentJarPath(), SERVER_SECRET_FILENAME, newSecret.getBytes());
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
                logger.info("Newly generated secret is now written to the filesystem for persistence.");
                return newSecret;
            }
        }
    }

    ```
    :::
    可以發現作者的註解說not so random，secret key是1234，把key拿到jwt online decoder做驗證，發現signature是正確的
    
2. Construct a Fake Token
根據hint的說明，我們應該只要改userId和role這兩個欄位如下，切記也要改token-payload如下，就可以更改自己的權限
![](https://hackmd.io/_uploads/HJWUqfuun.png)
![](https://hackmd.io/_uploads/H1-LjzOdh.png)

    
Flag: `picoCTF{w34k_jwt_n0t_g00d_6e5d7df5}`

## Reference
[ picoCTF 2023 Java Code Analysis?!? ](https://youtu.be/tsTkxWxLTqk)