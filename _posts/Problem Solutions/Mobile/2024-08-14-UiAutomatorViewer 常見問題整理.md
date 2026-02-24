---
title: "UiAutomatorViewer 常見問題整理"
tags: [problem solution]

category: "Problem Solutions"
date: 2024-08-14
---

# UiAutomatorViewer 常見問題整理
<!-- more -->

## Java版本不相容
* 參考來源1: [Setting up Appium configuration on windows / Mac](https://khemlall-mangal.medium.com/setting-up-appium-configuration-on-windows-mac-efbc4d4a7bc3)
* 參考來源2: [uiautomatorviewer閃退、提示Could not create the Java Virtual Machine等問題的處理](https://blog.csdn.net/zyself/article/details/124084171)

如果電腦安裝的JAVA version不是JAVA 8的話，有極高的機率會出錯，但又不想要覆蓋掉自己原本安裝的latest version，那參考來源1這個forum可以滿足這樣的事情

1. 下載JAVA 8並安裝 - 參考[(超詳細）2022年最新版java 8（jdk1.8u321）安裝教程](https://blog.csdn.net/JunLeon/article/details/122623465)
    * Official Link: https://www.oracle.com/java/technologies/downloads/#java8-windows
2. 下載完UiAutomatorViewer之後直接改內部的bat file
    1. Open `uiautomatorviewer.bat` with editor by the path - `%USERPROFILE%\AppData\Local\Android\Sdk\tools\bin\uiautomatorviewer.bat`
    2. 搜尋`set java_exe=`並且設定成comment，再更新如下
        ```bash
        $ set java_exe=C:\Program Files\Java\jdk-1.8\bin\java.exe
        ```
        ![圖片](https://hackmd.io/_uploads/BktkRCFcR.png)

## Error while obtaining UI hierarchy XML file: com.android.ddmlib.SyncException: Remote object doesn't exist!
這個的解決方案有很多，我是在使用Spotify的時候出現這個問題，解決的方案是第一個

* 參考來源1: [CSDN - adb常用命令](https://blog.csdn.net/YiLiuF/article/details/109601968)
* 參考來源2: [cnblogs - 【Android】【問題解決記錄】Error obtaining UI hierarchy :Error while obtaining UI hierarchy XML file: com.android.ddmlib.SyncException: Remote object doesn't exist!](https://www.cnblogs.com/lilip/p/11089713.html)
* 參考來源3: [StackOverflow - Error obtaining UI hierarchy Error while obtaining UI hierarchy XML file: com.android.ddmlib.SyncException: Remote object doesn't exist](https://stackoverflow.com/questions/40214342/error-obtaining-ui-hierarchy-error-while-obtaining-ui-hierarchy-xml-file-com-an)
* 參考來源4: [CSDN - Error while obtaining UI hierarchy XML file: com.android.ddmlib.SyncExceptio解決方法](https://blog.csdn.net/weixin_39230341/article/details/90598944)
* 參考來源5: [uiautomatorviewer報錯：Remote object doesn‘t exist Error while obtaining UI hierarchy XML file](https://blog.csdn.net/suncanshine/article/details/124546419)

1. 方法一: 直接斷網再重新測試
2. 方法二: 查看電腦的adb version和手機的sdk version有無符合
    手機sdk版本: `$ adb shell getprop ro.build.version.sdk`
    電腦adb版本: `$ adb version`
    如果電腦的adb版本過高好像也會出錯，因此可以考慮降低版本
4. 方法三: 重新啟動adb
    ```bash
    $ sudo adb kill-server
    $ sudo adb start-server
    ```
4. 重啟手機
5. 如果使用uiautomatorviewer的同時也有使用Appium，可以想辦法把Appium kill掉，好像會出現衝突之類的問題
6. 打開手機開發者權限，將USB Debug按鈕重新啟動