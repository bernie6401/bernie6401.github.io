---
title: Crypto Cheat Sheet
tags: [Tools, CTF, Crypto]

---

# Crypto Cheat Sheet
## Online Tools - Classic Crypto
| Complex| Substitution Cipher| Vigenère Cipher|
| - | - | - |
| [CyberChef](https://gchq.github.io/CyberChef/) | [Substitution Cipher Solver Tool](https://www.boxentriq.com/code-breaking/cryptogram) | Known Key </br>Python - `pycipher` library</br>[online - Vigenère cipher](https://planetcalc.com/2468/)</br>CAP4|
| [quipqiup](https://quipqiup.com/)|| Unknown Key</br>[Vigenère Cipher Codebreaker](https://www.mygeocachingprofile.com/codebreaker.vigenerecipher.aspx)</br>[Vigenere Solver](https://www.guballa.de/vigenere-solver) |

## RSA相關攻擊
其實整裡的文章內容都差不多
* [【技術分享】CTF中RSA的常見攻擊方法](https://www.anquanke.com/post/id/84632)
* [Mod相關攻擊](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_module_attack/)
* [CTF RSA](https://zhuanlan.zhihu.com/p/76228394)

## Coding Tools
* 大數運算: [gmpy2](https://blog.csdn.net/m0_52842062/article/details/117852175)/[sage math online - cocalc](https://cocalc.com/features/sage)/[sage math online - sagecell](https://sagecell.sagemath.org/)/[WolframAlpha](https://www.wolframalpha.com/):這是一個線上的搜索引擎，但凡和數學相關的都能進行運算，使用解說可以看[這裡](https://youtu.be/9JD3EzbAjH4?si=fmL7rOXK0u__Mf3u)
    ```bash!
    $ sudo apt install sagemath
    # or
    $ conda create --name sageenv sage=10.0 -c conda-forge -y # just only for wsl
    ---
    # 想要在sage中安裝python library
    $ sage -pip install {library name}
    ```
    :::spoiler To address Discrete Log Problem
    ```python
    p = 117635180960139721127318189832610714114593440637486157582828661167364276581210599344857316369131977790468647533227778603367761815400416396281259234299247850289710613080530669849409358755399675041263469367135430665518150110493389671646158566214130516002949975036799297119111385228596853422400303735447298026283
    q = 163800729847029979711295941089800020300275211671661376396219775666688832353701752860857691086339595920419175562271802936423756228938551439950541873798393442729921516031775531740506399414675546114663346731428381174638773512946351966471041847661507898143967764453261943807056370639171597924004988320983393199599
    c = 0x8788542cefd7490c9282c06b8d24280d56c6706b996bdf580290cdf2cb90e45efd2ce185fc07d2b916c24b0512d38ca14de0ee608a9d6003f258859bbbed97dad15c1d07410a34fd55cd8305eb43418d38f1ca6e024725b97fd9da701a39c23fe55a13d43b4bf9a3d9ebb44d7fe67bd60beffc29ec27bb4baf05ec5b250bfa68360df0d1379c066297a7878e59d27e68cf6a0da90755450827623e54e4f3d9f280fef53c7620d58decfbd10dd64e9d1d5507b5460603c58f5be70c82e2a8e613d730a950caea4c4389c5fc0521f8207ead5fb26c04eb6d0486fd6fe8d015fdabbda00139b42163acc86ffb30c12988058c6247344c42b8f3cdc984c06f4276f8
    g = Mod(3,p)
    m = discrete_log(c,g)
    print(hex(m))
    g2 = Mod(3,q)
    m2 = discrete_log(c,g2)
    print(m2)
    print(hex(m2)[2:])
    ```
    :::
* Crypto常用library: pycryptodom
    `$ pip install pycryptodome`
    :::spoiler pycryptodome generate PEM file
    ```bash
    >>> from Crypto.PublicKey import RSA
    >>> n = 0xb4f98200f1309e8a486824051051ac80790f8e66dac4744e2ce5134fb432121f41c5471e3459d01e56e64befd2034c65eb300ebf0045342221bff206b6cdda7f3349c17b08563a576731f95a64e2f00af70b5cbb2f4f388d49ce82da76ca609a6ec1529f29b0fa0bedc5764b86472e2c5ac5198cedb6f5e1e8e0ca950ea11bc4cf5e5a0497db3ad96f5a745cf902d56be394a259068fe198bc9de8fe8d034a71013f46c2ac72451211eb1127286c19467eaf3a10049942d46b0f49f3c51c01c06a2f8c94416cc1aadaeb191de959f0241ce8f32575c848bd2f4f8f84dab46e2aa7ad45de1c6060fbbee9668f8e9cb6d366b8cd6ce99f78bbef145f2b7b7e5222f762ccb95f17b1538260c2ea45571061b0d873fbe60d61dd87aa4833ac71b802f2b91d30f38e30ae9da39fbd1c53e80496f511521285b3bb1da3dc79931463d278d1fe28a77880a9f2368029c4cefffebbbd6904f85291b3606d0b5ed3efd8c1ee14538dc051274665f4b0f55d6c6e12d2cb728ac15f7a6572b71a5bd6fa01bddb0af211091bff4c8ec7e93efae4654b2abae09e35be29afbfc3f4df8e4348c525b9d8662a1ac344dadb15b953905f639b48fec7cfcfdf27cc0ad82b936d5efe7c0d891bf9752d3fb0857d38337df033e4b681d19ec8603535504d05a421036c077694482eee919a44b3296e2a4c272cbf7bbf14b6d62eb194e4ee83ba227fed
    >>> e = 0x10001
    >>> d = 0x737efcd1df1b7942a53d1927c62769a0c022066e6bd58ea8498c948b7c63ac1f18996f6ebe584732e5a0a9fbce9ade49f913bd857605b464c80738cdc22293fc33de314574a79b2a26a8c50b447174627b115c47f5c46841fb45794b351ea91245f6c8e4dcf59e4eb89b1988cf9463ca58cf8b23de9db2444f9c0e8d9c3d837c521f53f1b47c6c0d523c7720d2a655503a78a4378eb18a773080d2ae898dfd172b8597822c0ded38c008b5f4b89e6c6f09f0886caa92a90ce99a6346d897ac2281620124a8b060d4ca4bd9c6b622f8d8033f43d5b75a6fd994f50091f805c87d1e6fbdb42785f6bf1332df8a64a86d21736023720b9303b964b62a9a9480a4a7ab5fac794f583109d5663998ccc893590ebe26ae076e17c2b93c2238106612094fd4c6a56ec84ca5fa6ee3608ba3422f931828772e6732c337fcd6d4e6cb4a907d2e978227423d783c112f7a7d3e6d7c91ac7c540f0095d39842a6be534321a67d7a3fcb1c62c0f9e8a6d6e10281e10ff957449770d19f939153692c73f940450eab03f58ef55d2adf98c3f8479d05bb02997667381d3583c8f0eba6ea91bce512b001a27788309a4aa15952c73572a329b2f3acd6a11f43e3ae00532ccfbe9f157702162b534d26ca1e668d4cdbfd0116b7cb724603ea99e8aa08c90410534dd681b59350542c59523cb1259428e05e1fe0aab479c4b5af2a44d18ef713cd61
    >>> p = 0xd73e2ef8f2e4f1de44ee80070beef39943d4fa89a7a7ab4b0061e851aca7deb4f717f2baf4a0c018f3dcdab92148596bc50800fd6eb2f2e7757e0343534aea2241f0a2d34795a08f8e5ccc7959184b9cf8e3007a8ad63acd7d4b350dbf2d4caf04f4bc98d74a3b01d3b1aced745133186fd8460a2dff536a74ee4d041c988d5743cc9355144f48fe5f52db0449a46ba7c15c04001a5cb141796b5b42d9d72c36cca6d6bb8f177aee1699a47ba5d87c7ee886467af18403dbd84e102a952ebee03cc70bcf072c26b1b1f0f5094be08470c6c1769b417feffd5c89a0c373f75a350d177309618bfeb16316c660c6b2a341a984c8845081ede7c42e22cc9272aa15
    >>> q = 0xd73e2ef8f2e4f1de44ee80070beef39943d4fa89a7a7ab4b0061e851aca7deb4f717f2baf4a0c018f3dcdab92148596bc50800fd6eb2f2e7757e0343534aea2241f0a2d34795a08f8e5ccc7959184b9cf8e3007a8ad63acd7d4b350dbf2d4caf04f4bc98d74a3b01d3b1aced745133186fd8460a2dff536a74ee4d041c988d5743cc9355144f48fe5f52db0449a46ba7c15c04001a5cb141796b5b42d9d72c36cca6d6bb8f177aee1699a47ba5d87c7ee886467af18403dbd84e102a952ebee03cc70bcf072c26b1b1f0f5094be08470c6c1769b417feffd5c89a0c373f75a350d177309618bfeb16316c660c6b2a341a984c8845081eded2ff580f9f582ac79
    >>> key_params = (n, e, d, p, q)
    >>> key = RSA.construct(key_params)
    >>> f = open('./rsaprivatekey.pem', 'w')
    >>> f.write(key.exportKey().decode())
    >>> f.close()
    ```
    :::
* [openssl - RSA(很清楚)](https://www.mkssoftware.com/docs/man1/openssl_rsa.1.asp)
    :::spoiler Cheat Sheet
    ```bash!
    '''AES / DES'''
    $ openssl des-ecb –e –in xxx.txt –out yyy.out –k password (DES encrypt)
    $ openssl des-ecb –d –in yyy.out –out xxx.txt –k password (DES decrypt)
    $ openssl des-ede3 –d –in yyy.out –out xxx.txt –k password (TDES encrypt)
    $ openssl aes-128-ecb –d –in yyy.out –out xxx.txt –k password (AES decrypt)
    
    '''RSA'''
    $ openssl genrsa –out rsa_privatekey.pem –passout pass:password –des3 1024
    # (generate RSA private key)
    $ openssl rsa –in rsa_privatekey.pem –passin pass:password –pubout –out
    rsa_publickey.pem (generate RSA public key)
    $ openssl rsautl –encrypt –pubin –inkey rsa_publickey.pem –in xxx.txt –out yyy.txt
    # (use public key to encrpt)
    $ openssl rsaut –decrypt –ik i k n ey rsa_privatekey.pem –in yyy.txt –out xxx.txt
    
    #  To print out the components of a private key to standard output
    $ openssl rsa -in key.pem -text -noout
    
    # 把certificate轉成pem file
    $ openssl openssl x509 -in cert -pubkey -noout
    -----BEGIN PUBLIC KEY-----
    MCIwDQYJKoZIhvcNAQEBBQADEQAwDgIHEaTUUhKxfwIDAQAB
    -----END PUBLIC KEY-----
    
    # 把單純public key的內容(n, e)(就是上面的東西)印出來
    $ openssl rsa -pubin -in public.pem -text
    RSA Public-Key: (53 bit)
    Modulus: 4966306421059967 (0x11a4d45212b17f)
    Exponent: 65537 (0x10001)
    writing RSA key
    -----BEGIN PUBLIC KEY-----
    MCIwDQYJKoZIhvcNAQEBBQADEQAwDgIHEaTUUhKxfwIDAQAB
    -----END PUBLIC KEY-----
    
    // 產出私鑰
    openssl genrsa -out key.pem 2048

    // 用同一把私鑰，產出兩組不同的憑證
    openssl req -x509 -new -key key.pem -sha256 -nodes -keyout key.pem -out cert1.pem -days 30
    openssl req -x509 -new -key key.pem -sha256 -nodes -keyout key.pem -out cert2.pem -days 30

    // 顯示公鑰是一樣
    openssl x509 -pubkey -noout -in cert1.pem
    openssl x509 -pubkey -noout -in cert2.pem

    // 顯示憑證內容是不一樣
    openssl x509 -inform pem -in cert2.pem
    openssl x509 -inform pem -in cert1.pem
    ```
    :::
## Factoring Tools
* [Factor DB](http://factordb.com/index.php)
* [Yafu](https://github.com/DarkenCode/yafu)
* [Prime Factorization Online](https://www.alpertron.com/ECM.HTM)