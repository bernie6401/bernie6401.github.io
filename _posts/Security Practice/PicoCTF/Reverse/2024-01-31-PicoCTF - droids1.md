---
title: PicoCTF - droids1
tags: [PicoCTF, CTF, Reverse]

category: "Security Practice｜PicoCTF｜Reverse"
date: 2024-01-31
---

# PicoCTF - droids1
<!-- more -->

## Backgroud
[ Android App 逆向入門之一：拆開與重組 apk ](https://blog.huli.tw/2023/04/27/android-apk-decompile-intro-1/): 強烈建議新手在打之前可以先看一下這篇，稍微了解一下整體怎麼包apk以及比要檔案有哪些，或是他們儲存的資料類型之類的

## Tools
* [apktool](https://ibotpeaches.github.io/Apktool/)
跟著[installation guide](https://apktool.org/docs/install)就可以安裝成功，此工具目的在於拆解apk，我們知道apk就是一個壓縮檔，如果直接用unzip這種指令，也可以打開，只不過一些經過編譯後的byte code就還是byte code，而apktool可以在解壓縮的同時還原這些byte code
* [Android Studio](https://developer.android.com/studio): 此工具目的在於利用emulator把該軟體安裝後跑起來
* [JADX](https://github.com/skylot/jadx): 和ApkTool一樣，可以反編譯apk，但有GUI(Recommended)
    ```bash!
     $ wget https://github.com/skylot/jadx/releases/download/v1.1.0/jadx-1.1.0.zip
     $ unzip jadx-1.1.0.zip -d jadx
     $ cd jadx
     $ cd ./bin
     $ ./jadx-gui
    ```

## Recon
這一題有兩種方法可以反編譯apk，一種是利用ApkTool，另外一個是JADX，兩者差在有無GUI(JADX有)，主要是參考[^pico-reverse-droids1-wp-haydenhousen]的WP

## Exploit

### ApkTools
```bash
$ apktool d one.apk
I: Using Apktool 2.8.1 on one.apk
I: Loading resource table...
I: Decoding AndroidManifest.xml with resources...
I: Loading resource table from file: C:\Users\Bernie\AppData\Local\apktool\framework\1.apk
I: Regular manifest package...
I: Decoding file-resources...
I: Decoding values */* XMLs...
I: Baksmaling classes.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...
```
如果有按照上面的guide把apktool裝起來，就可以直接下指令，參數`d`代表decode，對於比較熟Android架構的人來說應該綽綽有餘，畢竟要到哪邊找code/strings之類的，通常都會是那幾個地方，例如：
Code會放在`./smali/com/hellocmu/picoctf/`(PS: 只不過code很醜，畢竟是smali)
Strings會放在`./res/values/strings.xml`

根據[^android-teach-2]的教學:
> 在我們利用 apktool d 拆開的內容中，有一個資料夾叫做 smali，裡面存放著的就是從 classes.dex 還原出來的東西，也就是程式碼
> Smali 是跑在 Android Dalvik VM 上的 byte code，有著自己的一套語法規則，如果想要看到我們熟悉的 Java 程式碼，必須要將 smali 還原成 Java。

### JADX
其實用jadx也可以直接反編譯，而且還有GUI可以看，不香ㄇ
![](https://hackmd.io/_uploads/B1i_mB1xT.png)
用JADX一樣可以在相同的地方找到code，只是這一些code已經被還原成java
```java!
package com.hellocmu.picoctf;

import android.content.Context;

/* loaded from: classes.dex */
public class FlagstaffHill {
    public static native String fenugreek(String str);

    public static String getFlag(String input, Context ctx) {
        String password = ctx.getString(R.string.password);
        return input.equals(password) ? fenugreek(input) : "NOPE";
    }
}
```
可以看到FlagstaffHill這個class有兩個member(fenugreek/getFlag)，所以看起來他會把我們輸入的東西和password這個variable做比較，如果一樣就會去call fenugreek(input)，否則回傳NOPE
而password是從R.string.password來的，可以看到password的值是0x7f0b002f應該是一個offset?或是一個地址，不是很確定
![](https://hackmd.io/_uploads/HJ3jNr1la.png)
反正最後取strings的地方在`./Resource/resources.arsc/res/values/strings.xml`
![](https://hackmd.io/_uploads/rkmrrSkea.png)

然後我們就可以利用Android Studio或是直接在自己的手機安裝這個apk，接著輸入password(opossum)就可以拿到flag了
![](https://hackmd.io/_uploads/HyyTBByxp.png)

Flag: `picoCTF{pining.for.the.fjords}`

## Reference
[^pico-reverse-droids1-wp-haydenhousen]:[droids1](https://picoctf2019.haydenhousen.com/reverse-engineering/droids1)
[^android-teach-2]:[ Android App 逆向入門之二：修改 smali 程式碼 ](https://blog.huli.tw/2023/04/27/android-apk-decompile-intro-2/)