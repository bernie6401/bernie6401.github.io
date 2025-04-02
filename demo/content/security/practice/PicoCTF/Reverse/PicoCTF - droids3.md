---
title: PicoCTF - droids3
tags: [PicoCTF, CTF, Reverse]

---

# PicoCTF - droids3
## Background
[ Android App 逆向入門之一：拆開與重組 apk ](https://blog.huli.tw/2023/04/27/android-apk-decompile-intro-1/)
[ Android App 逆向入門之二：修改 smali 程式碼 ](https://blog.huli.tw/2023/04/27/android-apk-decompile-intro-2/)
## Source code
```java=
package com.hellocmu.picoctf;

import android.content.Context;

/* loaded from: classes.dex */
public class FlagstaffHill {
    public static native String cilantro(String str);

    public static String nope(String input) {
        return "don't wanna";
    }

    public static String yep(String input) {
        return cilantro(input);
    }

    public static String getFlag(String input, Context ctx) {
        String flag = nope(input);
        return flag;
    }
}
```
## Recon
利用前一題學到的工具(JADX)，先decompiler一下原本的程式在幹嘛(source code如上)，會發現getFlag這個method所呼叫的nope只會吐出`don't wanna`，而真正會print出flag的是yep這個method，所以我們可以修改一下，不過修改之前還是要知道一下流程
Apktool decode apk file$\to$修改必要的地方$\to$Apktool重新打包$\to$簽名$\to$Align$\to$Done，這一個部分在[ Android App 逆向入門之二：修改 smali 程式碼 ](https://blog.huli.tw/2023/04/27/android-apk-decompile-intro-2/)有詳細的說明
## Exploit
1. 修改smali(`./three/smali/com/hellcmu/picoctf/FlagstaffHill.smali`)
只要把
`invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->nope(Ljava/lang/String;)Ljava/lang/String;`
修改成
`invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->yep(Ljava/lang/String;)Ljava/lang/String;`
2. 打包並簽名
這個真的找很久，需要align又要先簽名，雖然android studio把簽名的部分整合進去了，但algin的部分也是頗麻煩，所幸透過[^pico-reverse-droids3-wp]的說明，直接使用[^apk-signer-tool]這個tool，就可以省掉不少時間，真香
```bash!
$ apktool b three -o three_new.apk
$ wget https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar
$ java -jar uber-apk-signer-1.3.0.jar --apks three_new.apk
```
3. Android Studio安裝並執行
最後就直接在android studio執行emulator然後灌已經修改過的apk就好了，此時隨便輸入一些東西，就會噴flag
![](https://hackmd.io/_uploads/Hk3kHQbeT.png)

Flag: `picoCTF{tis.but.a.scratch}`
## Reference
[^pico-reverse-droids3-wp]:[droids3](https://picoctf2019.haydenhousen.com/reverse-engineering/droids3)
[^apk-signer-tool]:[Uber Apk Signer](https://github.com/patrickfav/uber-apk-signer)