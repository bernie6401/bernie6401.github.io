---
title: 如何使用Jekyll架設Blog
date: 2025-04-11
tags: [problem solution]
draft: false
toc: true
comments: true
category: "Problem Solutions"
---

# 如何使用Jekyll架設Blog
<!-- more -->
參考資料: [【種樹】使用 Jekyll 和搭建 Github Pages](https://hackmd.io/@CynthiaChuang/Setting-Up-a-GitHub-Pages-Site-with-Jekyll)

## Install Jekyll
1. Install [Ruby](https://rubyinstaller.org/)
    務必要安裝MSYS2，這是一個在 Windows 上提供 Unix-like 開發環境 的套件系統，它是許多 Windows 上的開發工具（尤其是 Ruby、Python、Node.js 的原生編譯擴充套件）運作的關鍵。安裝的時候只要按照rubyinstaller的流程就會看到，如果在安裝ruby的時候跳過了，可以直接`$ ridk install`並按照guide進行安裝
    ```bash
    $ gcc --version
    gcc (MinGW.org GCC-6.3.0-1) 6.3.0
    Copyright (C) 2016 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    $ ruby --version
    ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x64-mingw-ucrt]
    ```
2. 安裝Jekyll
    ```bash
    $ gem install jekyll
    $ gem install bundler
    $ bundler -v
	Bundler version 2.6.7
    $ cd myblog
    $ jekyll server
    ```
    之後就可以request http://localhost:4000 查看目前的網站

## 改Themes
和hugo差不多，網路上也是有很多種themes，看哪一種順眼，我是使用[NexT](https://github.com/Simpleyyt/jekyll-theme-next.git)([Official Guide](https://theme-next.simpleyyt.com/getting-started.html))，把該repo下載下來後解壓縮，把全部的內容複製到myblog folder，建議刪除Gemfile.lock，因為他使用的bundler version是1.17.1，現在有一些function已經廢棄了，可能會出現一些問題
```bash
$ bundle install
$ bundle exec jekyll server --incremental
```
`--incremental`的意思是只重新生成有變動的檔案，而不是每次都從零開始建整個網站。是 Jekyll 的一種加速機制
* (Optional) 解決大括號的問題
	因為Jekyll是支援Liquid語言並render成靜態的網站，因此在文章中如果出現{}語法，e.g., 嵌入YT的影片之類的，在啟動jekyll server時會出現error，解決的方式可以參考[解決Jekyll將大括號識別成Liquid語言](https://hackmd.io/@CynthiaChuang/Raw-in-Jekyll)，只要在大括號前後加入raw標籤就可以了
	```liquid
	{% raw %}{%youtube 27fBCKKZdpY %}{% endraw %}
	```

## 改Github Pages Setting
因為之前使用Hugo的時候是使用actions script，讓github使用Hugo，而不是預設的Jekyll，但現在就非常簡單，只要把`Setting > Pages > Build and deployment`中的Branch改回main就可以了，另外如果之前是使用Hugo並且有寫actions script的要把workflow folder刪掉

## (Optional) 新增 Disqus / LeanCloud / Gitalk / Swiftype
* [在Jekyll上使用LeanCloud統計訪問人數](https://brian90191.github.io/blog/2018-04-04/leancloud-In-Jekyll/)
* [使用 Disqus 在 Jekyll 增加留言區塊](https://mmiooimm.github.io/2018/09/19/2018-09-19-add-disqus-to-jekyll/)
* [利用Gitalk在靜態網頁裡面新增留言區](https://wjohn1483.github.io/2021/02/07/gitalk-introduction/)
* [使用SWIFTYPE為jekyll部落格新增搜尋引擎](https://www.cnblogs.com/dapenson/p/12822539.html)

## (Optional) Fine Tune Website
如果有其他需要，例如製作alert或是highlight之類的，可以參考Cynthia的其他文章，幫助很大
* [【種樹】顯示文章最後修改時間](https://hackmd.io/@CynthiaChuang/Show-the-Last-Modified-Time-in-Jekyll-NextT-Theme)
* [【種樹】修改 Jekyll 生成的靜態網址](https://hackmd.io/@CynthiaChuang/Controlling-Permalinks-in-Jekyll)
* [解決 Jekyll 將大括號識別成 Liquid 語言](https://hackmd.io/@CynthiaChuang/Raw-in-Jekyll)
* [【種樹】在時間軸上顯示完整日期](https://hackmd.io/@CynthiaChuang/Show-Full-Timestamp-on-Timeline)
* [【種樹】複製網頁文字時，加上網站的作者與網址](https://hackmd.io/@CynthiaChuang/Copy-Text-to-Clipboard-and-Append-Source-Hyperlink)
* [【種樹】HTML Mark Tag 實作 Highlighting](https://hackmd.io/@CynthiaChuang/Mark-Element-is-Used-to-Highlight-Content)
* [【種樹】新增版權訊息](https://hackmd.io/@CynthiaChuang/Add-Post-Copyright)
* [【種樹】實作 CSS 凸顯文字內容： Alert 與 Highlighting](https://hackmd.io/@CynthiaChuang/Accent-the-Text-by-CSS-Alert-and-Highlighting)