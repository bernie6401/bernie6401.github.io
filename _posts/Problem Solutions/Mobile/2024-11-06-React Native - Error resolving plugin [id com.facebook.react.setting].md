---
title: 'React Native - Error resolving plugin [id: com.facebook.react.settings]'
tags: [problem solution]

category: "Problem Solutions｜Mobile"
date: 2024-11-06
---

# React Native - Error resolving plugin [id: 'com.facebook.react.settings']
## Problem Statement
這個錯誤是發生在我想要創建一個新的React Native專案，但不管是用[Official Document](https://reactnative.cn/docs/environment-setup)還是其他網路文章的分享，我都無法順利創建，確切的錯誤message如下
<!-- more -->
```
$ yarn android
yarn run v1.22.22
$ react-native run-android
(node:13044) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
(Use `node --trace-deprecation ...` to show where the warning was created)
info A dev server is already running for this project on port 8081.
info Installing the app...

info 💡 Tip: Make sure that you have set up your development environment correctly, by running npx react-native doctor. To read more about doctor command visit: https://github.com/react-native-community/cli/blob/main/packages/cli-doctor/README.md#doctor


FAILURE: Build failed with an exception.

* Where:
Settings file 'D:\Downloads\Trash\MyProject\android\settings.gradle' line: 2

* What went wrong:
Error resolving plugin [id: 'com.facebook.react.settings']
> java.io.UncheckedIOException: Could not move temporary workspace (D:\Downloads\Trash\MyProject\android\.gradle\8.8\dependencies-accessors\569c8b261a8a714d7731d5f568e0e5c05babae10-3763ef7e-e78a-4639-821b-3aa92091847a) to immutable location (D:\Downloads\Trash\MyProject\android\.gradle\8.8\dependencies-accessors\569c8b261a8a714d7731d5f568e0e5c05babae10)
```
我是按照官方的文檔進行創建，而錯誤是發生在gradle的setting file中發生問題(MyProject\android\settings.gradle)，具體來說應該是版本上的問題，有嘗試針對以下文章說明的解決方式試看看，但都一無所獲
1. https://stackoverflow.com/questions/78384724/react-native-error-java-io-uncheckedioexception-could-not-move-temporary-work
2. https://github.com/facebook/react-native/issues/46210
3. https://github.com/facebook/react-native/issues/46133

## Before Solution
請先確定不是其他問題造成的，也就是盡量以官方說明的操作為優先，如果都沒問題，可以先用`$ npx react-native doctor`看看有沒有其他的環境變數或是emulator或是sdk沒有裝，如果發現問題，系統會告訴你(必需要在自己的project內執行該command)

## Solution
目前可行的方式是降版本，我一開始所用的React Native版本是0.76，但實際上應該要用0.74.5，然後更改setting.gradle的第3行的gradle version成8.5版本就可以了，原本的版本應該會是8.6
```bash
$ npx @react-native-community/cli init ProjectName --version=0.74.5

# Modify ./android/gradle/wrapper/gradle-wrapper.properties
# -->
distributionUrl=https\://services.gradle.org/distributions/gradle-8.5-all.zip
```