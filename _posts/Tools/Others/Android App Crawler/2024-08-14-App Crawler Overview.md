---
title: App Crawler Overview
tags: [Tools]

category: "Tools｜Others｜Android App Crawler"
date: 2024-08-14
---

# Android App Crawler
<!-- more -->
目前僅針對以下功能進行查找
1. 可以自行判斷目前activity有哪些可以interact
2. 自行與這些interactable的view進行interact，不管是DFS或是BFS，反正就是全部都互動就對了

## 比較常見的
* [App Crawler](https://developer.android.com/studio/test/other-testing-tools/app-crawler) [^app_crawler-1][^app_crawler-2][^app_crawler-3] - 無法使用
* [seveniruby/AppCrawler](https://github.com/seveniruby/AppCrawler) [^appcrawler-0][^appcrawler-1][^appcrawler-2][^appcrawler-3][^appcrawler-4][^appcrawler-5] - 無法使用
* [zhangzhao4444/Maxim](https://github.com/zhangzhao4444/Maxim) - 無法使用
* [Eaway/AppCrawler](https://github.com/Eaway/AppCrawler)
* [isonic1/Appium-Native-Crawler](https://github.com/isonic1/Appium-Native-Crawler)

## 根據Paper Related Work
1. [Stoat](https://github.com/tingsu/Stoat)
    :::info
    Ting Su, Guozhu Meng, Yuting Chen, Ke Wu, Weiming Yang, Yao Yao, Geguang Pu, Yang Liu, and Zhendong Su. 2017. Guided, stochastic model-based GUI testing of Android apps. In Proceedings of the 2017 11th Joint Meeting on Foundations of Software Engineering (ESEC/FSE 2017). Association for Computing Machinery, New York, NY, USA, 245–256. https://doi.org/10.1145/3106237.3106298
    :::
    詳細的說明(包含Demo影片、比較的工具、測試的App)，都可以參考 https://tingsu.github.io/files/stoat.html
2. [UI/Application Exerciser Monkey](https://developer.android.com/studio/test/other-testing-tools/monkey) - 不會採用
    這是上一篇所比較的對象之一，可以想像成一個猴子正在對一個手機上的App進行隨機互動，可能包含簡單的click, double click, long click或是swipe等等
    ```bash
    $ adb shell monkey -p com.music.spotify -v 50000
    ```
    最後面的數字代表隨機丟出多少的event給特定的App
3. [a3e](https://github.com/tanzirul/a3e) - 年代久遠不採用
    也是第一篇的比較對象之一
4. [Sapienz](https://github.com/Rhapsod/sapienz) - 無法使用
    也是第一篇的比較對象之一
5. [APE - official webpage](http://gutianxiao.com/ape/) / [APE - github](https://github.com/tianxiaogu/ape) - github star太少且年代久遠不採用
    這是第一篇有提到的工具之一
6. [Fastbot Android](https://github.com/bytedance/Fastbot_Android) - 可採用
    這是前一個APE官網有提到的工具，而且開發時間還蠻近的，github star也很多，也有[CSDN教學](https://blog.csdn.net/u010698107/article/details/127347704)
7. [Droidbot](https://github.com/honeynet/droidbot) - 可能採用
    :::info
    Li, Y., Yang, Z., Guo, Y., & Chen, X. (2017, May). Droidbot: a lightweight ui-guided test input generator for android. In 2017 IEEE/ACM 39th International Conference on Software Engineering Companion (ICSE-C) (pp. 23-26). IEEE.
    :::
    年代有點久遠，但網路上的[教學](https://juejin.cn/post/7316582773434204171)也蠻多的，官網也有提供[範例](http://honeynet.github.io/droidbot/report_com.yelp.android/)
8. [Androidenv](https://github.com/google-deepmind/android_env) - 可能採用
    :::info
    Toyama, D., Hamel, P., Gergely, A., Comanici, G., Glaese, A., Ahmed, Z., ... & Precup, D. (2021). Androidenv: A reinforcement learning platform for android. arXiv preprint arXiv:2105.13231.
    :::
    年代較近，也有教學

## 實驗的來源以及標準
如果僅僅是要app本身是開源的可以從[F-Droid](https://f-droid.org/zh_Hant/)當中去找，這個網站就是一個免費的Google Play Store，但是我要找的除了是app本身開源，後端本身也要開源，k因為這樣我才知道後端的URL有多少，如果想要知道有哪些可能可以拿來實驗的App，可以看`Guided, stochastic model-based GUI testing of Android apps.`這一篇論文(就是前面提到的第一篇)

### 透過CodePilot幫我找
* [awesome-appwrite](https://github.com/appwrite/awesome-appwrite)
* [FoodMagic](https://github.com/Sameerkash/FoodMagic):
    > 這是一個使用 Flutter 和 Appwrite 構建的應用程式
* [ao](https://github.com/klaudiosinani/ao):
    > 這是一個使用 Ionic 和 Appwrite 構建的待辦事項應用程式

## Reference
[^app_crawler-1]:[如何使用Android官方提供的自動進行UI掃描測試? (AppCrawler)](https://jefflin1982.medium.com/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8android%E5%AE%98%E6%96%B9%E6%8F%90%E4%BE%9B%E7%9A%84%E8%87%AA%E5%8B%95%E9%80%B2%E8%A1%8Cui%E6%8E%83%E6%8F%8F%E6%B8%AC%E8%A9%A6-appcrawler-a05c9ac3c07)
[^app_crawler-2]:[How to run Android “App Crawler” testing tool](https://medium.com/@denysiakimov/how-to-run-android-app-crawler-testing-tool-a0d6f387e89e)
[^app_crawler-3]:[Android testing “monkey” tool](https://medium.com/@denysiakimov/android-testing-monkey-tool-6f2457abec2b)
[^appcrawler-0]:[ 自動化測試的理想境界：AppCrawler自動遍歷工具 ](https://juejin.cn/post/6844903660795723789?searchId=202408021423471F784573A4037DEC4905)
[^appcrawler-1]:[ 初探自動遍歷測試工具-AppCrawler ](https://juejin.cn/post/6844903573864595463?searchId=202408021423471F784573A4037DEC4905)
[^appcrawler-2]:[ 以AppCrawler的設定檔完成客製化的自動遍歷測試(基礎)-01 ](https://juejin.cn/post/6844904008906178567?searchId=202408021423471F784573A4037DEC4905)
[^appcrawler-3]:[ 以AppCrawler的設定檔完成客製化的自動遍歷測試(實操)-02 ](https://juejin.cn/post/6844904013528301576?searchId=202408021423471F784573A4037DEC4905)
[^appcrawler-4]:[利器| AppCrawler 自動遍歷測試工具實務（一）](https://juejin.cn/post/7194260503743430715)
[^appcrawler-5]:[AppCrawler自動遍歷測試 ](https://blog.csdn.net/u010698107/article/details/111438820)