---
title: PicoCTF - Scavenger Hunt
tags: [PicoCTF, CTF, Web]

category: "Security/Practice/PicoCTF/Web"
---

# PicoCTF - Scavenger Hunt
###### tags: `PicoCTF` `CTF` `Web`
Challenge: [Scavenger Hunt](http://mercury.picoctf.net:55079/)

## Background
[.htaccess 使用技巧彙整](https://icodding.blogspot.com/2015/10/htaccess.html)
> .htaccess文件(或者」分佈式配置文件」）提供了針對目錄改變配置的方法， 即，在一個特定的文件目錄中放置一個包含一個或多個指令的文件， 以作用於此目錄及其所有子目錄。作為用戶，所能使用的命令受到限制。管理員可以通過Apache的AllowOverride指令來設置。
概述來說，htaccess文件是Apache伺服器中的一個配置文件，它負責相關目錄下的網頁配置。通過htaccess文件，可以幫我們實現：網頁301重定向、自定義404錯誤頁面、改變文件擴展名、允許/阻止特定的用戶或者目錄的訪問、禁止目錄列表、配置預設文件等功能。
.htaccess 詳解

## Exploit - [Insp3ct0r](/gYsHjI-rSD6Lce-7eF6DyA) + `htaccess` + `DS_Store`
1. HTML + CSS +JS
These files keeps one fragment flag each. Especially `js` file's hint: `/* How can I keep Google from indexing my website? */`
![](https://i.imgur.com/wuX9KLT.png)

2. Apache server $\to$ `.htaccess` file
![](https://i.imgur.com/li2z8l4.png)

3. Mac computer $\to$ `.DS_Store` file
![](https://i.imgur.com/iZfLWZ3.png)

* Combine the fragment
`picoCTF{th4ts_4_l0t_0f_pl4c3s_2_lO0k_74cceb07}`

## Reference
[Scavenger Hunt write up](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Web%20Exploitation/Scavenger%20Hunt/Scavenger%20Hunt.md)