---
title: App Crawler 無法使用紀錄
tags: [Tools]

category: "Tools/Others/Android App Crawler"
---

# App Crawler 無法使用紀錄
<!-- more -->
根據[Android Studio官網](https://developer.android.com/studio/test/other-testing-tools/app-crawler)的說明
```bash!
$ java -jar crawl_launcher.jar --apk-file path/to/my/app.apk --android-sdk path/to/my/android/sdk
```

我已經有安裝app在手機了，所以實際的command如下
```bash!
$ java -jar crawl_launcher.jar --app-package-name com.xueqiu.android --android-sdk C:\Users\Bernie\AppData\Local\Android\Sdk
Preparing to crawl com.xueqiu.android
Crawl started.
Crawl finished.
Writing logcat to D:\NTU\Paper\MITM Framework\Code\AppCrawler\Google App Crawler\crawl_output\com.xueqiu.android-logcat.txt
SUCCESS: Found 0 crashes.
Timed out waiting for crawl outputs proto file D:\NTU\Paper\MITM Framework\Code\AppCrawler\Google App Crawler\crawl_output\app_firebase_test_lab\crawl_outputs.proto
The output directory is D:\NTU\Paper\MITM Framework\Code\AppCrawler\Google App Crawler\crawl_output
```
但全程就只有大約不到30秒就結束了，不太懂流程到底出錯在哪，而且就算沒有安裝app，再重新跑一次，居然還可以沒有出錯的跑完；又或者是，把在沒有安裝app的情況下，用官網的command跑會直接當掉，無法繼續往下繼續跑，就一整個就很怪，但網路上也沒有比較新的說明