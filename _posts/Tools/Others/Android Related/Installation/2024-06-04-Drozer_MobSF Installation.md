---
title: Drozer/MobSF Installation
tags: [Android, Drozer, MobSF]

category: "Tools｜Others｜Android Related｜Installation"
---

# Drozer/MobSF Installation
<!-- more -->

## Installation - Drozer
我是參考[^drozer-installation-docker]的說明，但其實參考官網的也可以，我是用docker裝
1. Download drozer-agent & Install - [Download](https://github.com/WithSecureLabs/drozer-agent/releases) 
    這是要安裝在手機測試端的類似一個server的概念，而我們的電腦端也要安裝類似的東西(有好幾種方式，我是用Docker)，讓電腦和手機可以互通
    ```bash
    $ adb install drozer-agent.apk
    ```
2. Start a Session
    打開agent app會發現右下角有一個Off，點擊後會變成On，代表這個agent已經準備好要和電腦這邊的server連接
    ![Screenshot_20240603-131808](https://hackmd.io/_uploads/SkPEfC9NC.png =200x)
3. 設定電腦的Port轉發到Android的某個Port
    根據[^adb-forward]的說明，以及官網的要求，我們必須要把電腦31415這個port的封包轉發到手機端的31415這個port
    > Android 的 adb forward 通訊埠轉發的功能，adb forward 的功能是轉發 PC 電腦上某個埠號 (port) 資料到 Android 裝置的某個埠號 (port)，例如：下列 adb forward 指令就是將 PC 端的 port 10000 收到的資料，轉發給到 Android Device 的 port 20000
    ```bash
    $ adb forward tcp:31415 tcp:31415
    ```
4. Install PC Drozer Client
    看到以下畫面就代表成功了
    ```bash
    $ docker run -it --add-host host.docker.internal:host-gateway withsecurelabs/drozer console connect --server host.docker.internal
    Selecting ff762fc058e91df3 (Google Pixel 6a 13)

                ..                    ..:.
               ..o..                  .r..
                ..a..  . ....... .  ..nd
                  ro..idsnemesisand..pr
                  .otectorandroidsneme.
               .,sisandprotectorandroids+.
             ..nemesisandprotectorandroidsn:.
            .emesisandprotectorandroidsnemes..
          ..isandp,..,rotecyayandro,..,idsnem.
          .isisandp..rotectorandroid..snemisis.
          ,andprotectorandroidsnemisisandprotec.
         .torandroidsnemesisandprotectorandroid.
         .snemisisandprotectorandroidsnemesisan:
         .dprotectorandroidsnemesisandprotector.

    drozer Console (v3.0.2)
    dz>
    ```

## Installation - MobSF
可以直接使用[線上的工具](https://mobsf.live/)，也可以用docker架在自己的電腦
```bash!
$ docker pull opensecurity/mobile-security-framework-mobsf:latest
$ docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
```
並透過瀏覽器訪問 http://127.0.0.1:8000 ，default的帳密是==mobsf/mobsf==
# Reference
[^drozer-installation-docker]:[How to Install Drozer using Docker](https://scottc130.medium.com/how-to-install-drozer-using-docker-d0833f0802cb)
[^adb-forward]:[Android adb forward 通訊埠轉發用法教學](https://shengyu7697.github.io/android-adb-forward/)