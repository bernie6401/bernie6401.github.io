---
layout: post
title: "Add Third-Party Service to Jekyll"
date: 2025-04-15
category: "Tutorial"
tags: [Tutorial]
draft: false
toc: true
comments: true
---

# Add Third-Party Service to Jekyll
<!-- more -->

## Google Analytics

### 主要用途
使用者行為追蹤、流量分析，和Google Search Console主要不同在於，GSC關心的是SEO、哪些頁面出現在搜尋、誰點進來、網站可見性等等**點進網站前發生的事情**；而GA關心的是**進來後怎麼使用網站**，看了什麼、使用者的行為、網站體驗等等

### 說明
在原本的`_includes/_layout.html`中就可以看到，head label中有包含`_third-party/analytics/index.html`，先說`_includes/_layout.html`在幹麻，他就像是生成網站中所有page的最外圍的html，凡是about, post, tags, archive, category等等頁面，都會套用到這個file，所以不論是google analytics還是其他**需要套用到所有頁面的服務**，都是直接改這個就可以直接approach。
而直接細看`_third-party/analytics/index.html`這個file，會發現他就只是include一大堆第三方的code segment，可能是用於驗證有可能是直接提供服務，所以看起來就是直接改這裡，另外，因為這個主題的作者本來就有提供GA的腳本，但由於Google Analytics已經從原本的UA版本改成GA4，所以早期的腳本要換掉，就是GA網站提供給你的程式碼片段，要如何取得這個片段也很簡單
1. 註冊[Google Analytics](https://analytics.google.com/analytics/web)
2. 建立串流
3. 確認是否有被追蹤

詳細的說明可以參考[GA分析是什麼？最主流網站分析工具你學會沒？](https://welly.tw/blog/google-analytics-instruction)

另外，在`_config.yml`中，我是有把google_analytics給uncomment，不確定是不是一定要做這件事，不過我也沒有給任何value

## Google Adsense
可以直接看[小咪同學的文章](https://freespiritmi.com/google-adsense-step-by-step-guide/)，不過Google Adsense只能註冊main domain而不是subdomain，所以假設把blog設定在`https://blog.sbk6401.sbs`，系統會無法判斷，必須先deploy在`https://sbk6401.sbs`

### 驗證方式
和前面提到的google analytics的方式一樣，建立`_include/third-party/analytics/adsense.html`，再把Google提供的AdSense Code Segment放在這個file中，並且在`_third-party/analytics/index.html`新增`{% include _third-party/analytics/adsense.html %}`就可以了

## Google Webmaster (Google Search Console)
在`_config.yml`中也有，但我猜這應該也是早期版本才會需要的parameter，現在其實只需要在GSC的網站中新增資源就可以了
