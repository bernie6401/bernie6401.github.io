---
title: PicoCTF - droids4
tags: [PicoCTF, Reverse, CTF]

category: "Security Practice｜PicoCTF｜Reverse"
date: 2024-01-31
---

# PicoCTF - droids4
<!-- more -->

## Background
[ Android App 逆向入門之一：拆開與重組 apk ](https://blog.huli.tw/2023/04/27/android-apk-decompile-intro-1/)
[ Android App 逆向入門之二：修改 smali 程式碼 ](https://blog.huli.tw/2023/04/27/android-apk-decompile-intro-2/)

## Source code
```java
package com.hellocmu.picoctf;

import android.content.Context;

/* loaded from: classes.dex */
public class FlagstaffHill {
    public static native String cardamom(String str);

    public static String getFlag(String input, Context ctx) {
        StringBuilder ace = new StringBuilder("aaa");
        StringBuilder jack = new StringBuilder("aaa");
        StringBuilder queen = new StringBuilder("aaa");
        StringBuilder king = new StringBuilder("aaa");
        ace.setCharAt(0, (char) (ace.charAt(0) + 4));
        ace.setCharAt(1, (char) (ace.charAt(1) + 19));
        ace.setCharAt(2, (char) (ace.charAt(2) + 18));
        jack.setCharAt(0, (char) (jack.charAt(0) + 7));
        jack.setCharAt(1, (char) (jack.charAt(1) + 0));
        jack.setCharAt(2, (char) (jack.charAt(2) + 1));
        queen.setCharAt(0, (char) (queen.charAt(0) + 0));
        queen.setCharAt(1, (char) (queen.charAt(1) + 11));
        queen.setCharAt(2, (char) (queen.charAt(2) + 15));
        king.setCharAt(0, (char) (king.charAt(0) + 14));
        king.setCharAt(1, (char) (king.charAt(1) + 20));
        king.setCharAt(2, (char) (king.charAt(2) + 15));
        String password = "".concat(queen.toString()).concat(jack.toString()).concat(ace.toString()).concat(king.toString());
        return input.equals(password) ? "call it" : "NOPE";
    }
}
```

## Recon
基本上用眼睛看應該看的出來password是啥，不過他最後只會print出`call it`或是`NOPE`，所以我們要像上一題一樣改造一下smali，可以對照一下前一題的smali是怎麼call的

## Exploit
* 前一題的FlagstaffHill和smali
    ```java
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
    :::spoiler smali
    ```smali!
    .class public Lcom/hellocmu/picoctf/FlagstaffHill;
    .super Ljava/lang/Object;
    .source "FlagstaffHill.java"


    # direct methods
    .method public constructor <init>()V
        .locals 0

        .line 6
        invoke-direct {p0}, Ljava/lang/Object;-><init>()V

        return-void
    .end method

    .method public static native cilantro(Ljava/lang/String;)Ljava/lang/String;
    .end method

    .method public static getFlag(Ljava/lang/String;Landroid/content/Context;)Ljava/lang/String;
        .locals 1
        .param p0, "input"    # Ljava/lang/String;
        .param p1, "ctx"    # Landroid/content/Context;

        .line 19
        invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->yep(Ljava/lang/String;)Ljava/lang/String;

        move-result-object v0

        .line 20
        .local v0, "flag":Ljava/lang/String;
        return-object v0
    .end method

    .method public static nope(Ljava/lang/String;)Ljava/lang/String;
        .locals 1
        .param p0, "input"    # Ljava/lang/String;

        .line 11
        const-string v0, "don\'t wanna"

        return-object v0
    .end method

    .method public static yep(Ljava/lang/String;)Ljava/lang/String;
        .locals 1
        .param p0, "input"    # Ljava/lang/String;

        .line 15
        invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->cilantro(Ljava/lang/String;)Ljava/lang/String;

        move-result-object v0

        return-object v0
    .end method
    ```
    :::
所以我們只要像前一題一樣，把input丟到yep然後在call cardamon這個method應該就可以了，所以具體來說就是新增`yep`這個method
```java!
.method public static yep(Ljava/lang/String;)Ljava/lang/String;
    .locals 1
    .param p0, "input"    # Ljava/lang/String;

    .line 15
    invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->cardamom(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method
```
然後把最後getFlag的return改掉，變成:
```java!
.line 36
    invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->yep(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    return-object v5
```

:::spoiler Completely FlagstaffHill.smali
```java!
.class public Lcom/hellocmu/picoctf/FlagstaffHill;
.super Ljava/lang/Object;
.source "FlagstaffHill.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 6
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static native cardamom(Ljava/lang/String;)Ljava/lang/String;
.end method

.method public static getFlag(Ljava/lang/String;Landroid/content/Context;)Ljava/lang/String;
    .locals 8
    .param p0, "input"    # Ljava/lang/String;
    .param p1, "ctx"    # Landroid/content/Context;

    .line 12
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "aaa"

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 13
    .local v0, "ace":Ljava/lang/StringBuilder;
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 14
    .local v2, "jack":Ljava/lang/StringBuilder;
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 15
    .local v3, "queen":Ljava/lang/StringBuilder;
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    move-object v1, v4

    .line 17
    .local v1, "king":Ljava/lang/StringBuilder;
    const/4 v4, 0x0

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v5

    add-int/lit8 v5, v5, 0x4

    int-to-char v5, v5

    invoke-virtual {v0, v4, v5}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 18
    const/4 v5, 0x1

    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v6

    add-int/lit8 v6, v6, 0x13

    int-to-char v6, v6

    invoke-virtual {v0, v5, v6}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 19
    const/4 v6, 0x2

    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v7

    add-int/lit8 v7, v7, 0x12

    int-to-char v7, v7

    invoke-virtual {v0, v6, v7}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 21
    invoke-virtual {v2, v4}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v7

    add-int/lit8 v7, v7, 0x7

    int-to-char v7, v7

    invoke-virtual {v2, v4, v7}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 22
    invoke-virtual {v2, v5}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v7

    add-int/2addr v7, v4

    int-to-char v7, v7

    invoke-virtual {v2, v5, v7}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 23
    invoke-virtual {v2, v6}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v7

    add-int/2addr v7, v5

    int-to-char v7, v7

    invoke-virtual {v2, v6, v7}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 25
    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v7

    add-int/2addr v7, v4

    int-to-char v7, v7

    invoke-virtual {v3, v4, v7}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 26
    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v7

    add-int/lit8 v7, v7, 0xb

    int-to-char v7, v7

    invoke-virtual {v3, v5, v7}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 27
    invoke-virtual {v3, v6}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v7

    add-int/lit8 v7, v7, 0xf

    int-to-char v7, v7

    invoke-virtual {v3, v6, v7}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 29
    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v7

    add-int/lit8 v7, v7, 0xe

    int-to-char v7, v7

    invoke-virtual {v1, v4, v7}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 30
    invoke-virtual {v1, v5}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v4

    add-int/lit8 v4, v4, 0x14

    int-to-char v4, v4

    invoke-virtual {v1, v5, v4}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 31
    invoke-virtual {v1, v6}, Ljava/lang/StringBuilder;->charAt(I)C

    move-result v4

    add-int/lit8 v4, v4, 0xf

    int-to-char v4, v4

    invoke-virtual {v1, v6, v4}, Ljava/lang/StringBuilder;->setCharAt(IC)V

    .line 33
    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    const-string v5, ""

    invoke-virtual {v5, v4}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    .line 34
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    .line 36
    invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->yep(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    return-object v5
.end method

.method public static yep(Ljava/lang/String;)Ljava/lang/String;
    .locals 1
    .param p0, "input"    # Ljava/lang/String;

    .line 15
    invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->cardamom(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method
```
:::

在用apktool打包，在簽名和align就可以丟到Android Studio了
```bash!
$ apktool b four -o four_new.apk
$ java -jar ./uber-apk-signer-1.1.0.jar --apks four_new.apk
```
![](https://hackmd.io/_uploads/HJQujE-la.png)

Flag: `picoCTF{not.particularly.silly}`