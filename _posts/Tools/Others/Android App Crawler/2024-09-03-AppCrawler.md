---
title: AppCrawler
tags: [Tools]

category: "Tools > Others > Android App Crawler"
---

# AppCrawler
前面踩了超多坑，所以一切都以底下最新的配置為主
## Infra
1. Appium - 1.22.3
    一定要是2.0.0以下(未包含)，所以不要用default latest version，可以用CLI也可以用Desktop，因為Desktop Version預設已經no longer supported，所以一定是1.22.3，而CLI安裝就需要指定(以下是已經安裝npm為前提)
    ```bash
    $ npm install -g appium@1.22.3
    $ npm install -g appium-doctor
    ```
2. 設定ANDROID_HOME和JAVA_HOME
    到Windows環境變數設定
    ![圖片](https://hackmd.io/_uploads/BkmODXjqR.png)
    然後去看appium-doctor看necessary的部分是不是都有，一般來說可能會apkanalyzer.bat會沒有，這方面就慢慢到網路上去載android studio下載tools
    ![圖片](https://hackmd.io/_uploads/BkZsw7j9R.png)
4. AppCrawler - latest (2.7.4)
    就直接到github release去下載build好的jar file，不需要看其他教學是用2.4.0或是2.3.1去用stb或是maven build原本的專案
    Official Link: https://github.com/seveniruby/AppCrawler/releases/tag/2.7.4
## 測試前
1. app activity name
    如果已經在手機安裝好，就直接看dumpsys中該package的main activity是哪一個
    ```bash
    $ adb shell dumpsys package com.spotify.music | grep -B 2 "android.intent.action.MAIN" -n
    279-          Action: "com.google.android.meet.ADDONS_SUPPORT"
    280-          Category: "android.intent.category.DEFAULT"
    281:      android.intent.action.MAIN:
    282-        553d29 com.spotify.music/.SpotifyMainActivity filter 3a3b8ae
    283:          Action: "android.intent.action.MAIN"
    --
    286-          Category: "android.intent.category.APP_MUSIC"
    287-        7cd1a0c com.spotify.music/.main.AppIconEmeraldGreen filter 18bef55
    288:          Action: "android.intent.action.MAIN"
    --
    290-          Category: "android.intent.category.DEFAULT"
    291-        c3efd6a com.spotify.music/.MainActivity filter 204625b
    292:          Action: "android.intent.action.MAIN"
    --
    307-      android.intent.action.MUSIC_PLAYER:
    308-        553d29 com.spotify.music/.SpotifyMainActivity filter 3a3b8ae
    309:          Action: "android.intent.action.MAIN"
    ```
    另外一種方式就是用apktool反編譯後去看AndroidManifest.xml，一樣就是string search ==android.intent.action.MAIN==，但反編譯後會有一大堆files，可能會很佔空間
    ```bash
    $ apktool d your_app.apk
    ```
2. app package name
    如果已經安裝了，就直接list package
    ```bash
    $ adb shell pm list package | grep spotify
    package:com.spotify.music
    ```
    要不然就要用aapt去看
    ```bash
    $ aapt d badging Spotify.apk | findstr package
    package: name='com.spotify.music' versionCode='116658084' versionName='8.9.58.572' platformBuildVersionName='14' platformBuildVersionCode='34' compileSdkVersion='34' compileSdkVersionCodename='14'
    uses-permission: name='com.sec.android.app.clockpackage.permission.READ_ALARM'
    ```
3. 開啟appium
    如何檢視有正確開啟並且有連線到
    ```bash
    $ appium
    [Appium] Welcome to Appium v1.22.3
    [Appium] Appium REST http interface listener started on 0.0.0.0:4723
    $ curl http://127.0.0.1:4723/wd/hub/status
    {"value":{"build":{"version":"1.22.3"}},"sessionId":null,"status":0}
    ```
## 實際測試
```bash
$ java -jar appcrawler-2.7.4-hogwarts.jar --capability "appPackage=com.spotify.music,appActivity=MainActivity"
```
## 注意事項
:::danger
基本上這個tool還是依照大量截圖的方式判斷有無換頁，所以依照現在android版本的更新，開發商如果設定成無法截圖的方式，就無法做後續的測試
:::
:::danger
根據以上的步驟，還是非常有可能會遇到問題，我自己在用physical device時，最常遇到[java.lang.RuntimeException: Error creating extended parser class: Could not determine whether class ‘org.pegdown.Parser$$parboiled’ has already been loaded](https://ceshiren.com/t/topic/16293)，在使用emulator的時候，也會遇到[Exception in thread “main” java.awt.image.RasterFormatException: (y + height) is outside of Raster](https://ceshiren.com/t/topic/31983)

但通通得不到解決的方式
:::