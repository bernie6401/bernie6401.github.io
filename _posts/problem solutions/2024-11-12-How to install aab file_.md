---
title: How to install aab file?
tags: [problem solution]

category: "Problem Solutions"
---

# How to install aab file?

## Problem Statement
有時候我們會直接拿到aab檔案而非apk，尤其是用React Native寫的專案，但又無法直接安裝這個aab檔案，他需要經過一些步驟才能轉成apk

## Solution
先確保本機有安裝keytool和bundletool，keytool一般會在`C:\Program File\Java\jdk-17\bin`中，只要設定環境變數就可以直接使用；而bundletool則是要另外[下載](https://github.com/google/bundletool/releases)，有關於如何寫成bat，可以參考[bundletool 工具使用詳解](https://blog.csdn.net/yingaizhu/article/details/119545459)
```bash
$ keytool -genkeypair -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias
# 填寫基本資訊
$ bundletool build-apks --bundle=<your aab filename> --output=app.apks --ks=./my-release-key.jks --ks-key-alias=my-key-alias
$ bundletool install-apks --apks=app.apks
```