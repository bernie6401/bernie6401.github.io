---
title: Identifying vulnerabilities of SSL/TLS certificate verification in Android apps with static and dynamic analysis
tags: [Meeting Paper, NTU]

category: "Survey Papers/Android + Security"
---

# Identifying vulnerabilities of SSL_TLS certificate verification in Android apps with static and dynamic analysis
<!-- more -->
:::info
Wang, Y., Xu, G., Liu, X., Mao, W., Si, C., Pedrycz, W., & Wang, W. (2020). Identifying vulnerabilities of SSL/TLS certificate verification in Android apps with static and dynamic analysis. Journal of Systems and Software, 167, 110609.
:::
這一篇論文對我要做的東西非常類似，雖然本質上不一樣但有很多的觀點以及解決方式是可以參照的

## Introduction
這篇文章探討了在Android應用程式中SSL/TLS憑證驗證的弱點，並提出了一種名為DCDroid的工具來偵測這些弱點。作者結合靜態和動態分析，分析了來自Google Play和360app的2213個應用程式，發現其中有20.65%可能存在弱點。透過DCDroid在兩部Android智慧手機上執行這些應用程式，最終確認了11.07%的應用程式對MITM和釣魚攻擊存在真正的弱點。

## Background
* SSL/TLS and Android
    一般來說，正確的驗證憑證的步驟為
    1. 在憑證鏈中的所有憑證有無過期
    2. 憑證或憑證鏈中的根憑證由客戶端的憑證授權單位（CA）簽署
    3. 證書中的網域名稱與所連接的伺服器的網域名稱相符
    
    但是基於一些原因(例如: 使用self-signed certificate/伺服器的root憑證不在手機的CA list中/糾正某些第三方庫的不安全實作)導致開發者會自行實做一個憑證驗證的方法，而這時候就有可能會產生一些漏洞發生，例如:
    :::warning
    1. 信任具有 X509TrustManager 介面的所有證書(有關的說明可以參考[官網](https://developer.android.com/privacy-and-security/risks/unsafe-trustmanager?hl=zh-tw))
    2. HostnameVerifier 未檢查Domain Name(有關的說明可以參考[官網](https://developer.android.com/privacy-and-security/risks/unsafe-hostname?hl=zh-tw))
    3. 使用setHostnameVerifier（透過使用ALLOW_ALL_HOSTNAME_VERIFIER）方法接受任何網域名稱(範例如[證書不安全解決HttpClient 如何忽略證書驗證 - ALLOW_ALL_HOSTNAME_VERIFIER](https://blog.csdn.net/tiantianchuqiji/article/details/76639796))
    4. 當WebView元件發生憑證驗證錯誤時，直接在onReceivedSslError()方法中呼叫proceed()方法可以忽略憑證驗證錯誤。
        補充: 根據[\[Android\] WebView without HTTPS](https://myoceane.fr/index.php/android-webview-without-https/)
        > 在設定 webView 的時候需要設定 WebViewClient ,這個方法是重新調整當 SslError 時的反應方法,在 Android9.0 之後 onReceivedSslError 的預設方法是handler.cancel()，如此會將 WebView 變成空白頁，將handler.cancel()改成handler.proceed() 之後就可以成功顯示沒有 SSL 的網頁
    :::

## Problem Statement
1. 如何定義潛在的易受攻擊代碼並觸發它們
2. 如何模擬人類操作
    作者有提出很多工具，例如MonkeyRunner、Appium、FlowDroi、DroidScope、Dynodroid、Smart Droid、Brahmastra
    1. MonkeyRunner: 它的執行沒有特殊用途，主要依賴於隨機點擊。因此，很難觸發易受攻擊的代碼
    2. Appium: 可以使用特定的腳本來精確運行 UI 元素。但是，它沒有通用性，需要針對每個應用程式進行自定義。
    3. FlowDroi、DroidScope: 可以跟蹤方法調用關係。但是，它們無法觸發動態漏洞
    4. Dynodroid: 專注於處理自動輸入
    5. Smart Droid、Brahmastra: 無法處理 Web UI
3. 如何高效運行
    這個就和老師說的有關，在一個App的activity中，有很多是類似的UI elements，而這些類似的UI對應到的handler其實差不多甚至一樣，那這樣的話如果要進行測試只要測試一個就好
4. 如何有效運行
    意思是雖然proxy可以攔截所有流量，但是我們怎麼確認這個流量是來自我們要偵測的那個App所發出來的呢?背景程式中有很多其他的App也在發出package，要怎麼辨認呢?

## Proposed Method
整體的分析流程如下，首先給定一個App，然後先進行靜態分析，並且分析取得的smali code，用一開始定義的演算法以及漏洞方法，找到潛在的漏洞，並且把vulnerable activity給動態分析，實際安裝與執行後，利用MITM工具攔截流量，並使用VPNService捕獲智能手機上的流量。最後，我們通過比較智慧手機和攻擊工具之間的流量來確認那些真正易受攻擊的應用程式。
![圖片](https://hackmd.io/_uploads/SkfW7I6SC.png)
'

### 如何定義潛在的易受攻擊代碼並觸發它們

#### 如何定義vulnerable method
1. X509TrustManager: 如果開發者有擴充這個class，他就會實際的看==checkClientTrusted==和==checkServerTrusted==這兩個method，如果這兩個method只有`return void`這一行code，那就代表這個App信任具有X509TrustManager 介面的所有證書，那當然就是有問題的地方
2. HostNameVerifier: 先檢查HostNameVerifier有沒有被實作，如果有就往下檢查==verify== method，他直接查看這個方法如果第一行是const開頭，第二行直接return的話，就代表他沒有檢查Domain Name，也一樣是有問題的
4. X509HostnameVerifier: 先檢查X509TrustManager extend class的類別中是否有sget-object的指令。如果有，我們檢查它是否以 ==ALLOW_ALL_HOSTNAME_VERIFIER Lorg/apache/http/conn/ssl/X509Hostname Verifier== 結尾。如果還是成立，我們檢查下一指令是否為 ==-> setHostname Verifier (Lorg/apache/ http/n/ssl/X509Hostname Verifier);V== 。如果存在，我們就認為該方法有漏洞。
3. WebViewClient sslError: 先檢查程式有無擴充WebVieClient這個class，如果有就檢查==onReceivedSslError==這個方法，如果這個method只有兩個instructions，而且第一行是invoke-virtual開頭、Landroid/webkit/SslErrorHandler;->proceed()V結尾，另外第二行就直接return void的話，代表這個method是有問題的

#### 如何判斷這些vulnerable method會被觸發
1. Vulnerable Method最後會被誰call到
    這段演算法的目的是通過遍歷Method Call Graph，找到所有可能調用Vulnerable Method的入口點方法，這些入口點方法是應用啟動時首先執行的方法或初始化方法。這樣可以幫助開發者了解潛在的Vulnerable Method是如何被call的，在動態分析階段優先考慮這些entry point，以便執行它們。這個演算法的概念是，從vulnerable method的角度出發一直往上走(看誰有call到)，比方說A call B, B call C, C call vulnerable method v1，而因為A是最後一個和VM有關係的class，那就直接看A裡面的constructor，並且向剛剛一樣，不斷往上看誰call了這個class method，找到最後，如果有一個class constructor是沒有被app任何一個code所呼叫，代表他一定是被系統所呼叫，這樣的話這個constructor就是我們要找的entry point
    演算法:
    ```=
    Require: MCG : Method Call Graph,VM : Vulnerable Method 
    Ensure: Result : Set of Entry Point Methods 
    function FindFinalCaller ( MCG, VM ) 
        if method_callers of VM not null then 
            for each method_caller in method_callers do 
                FindFinalCaller(MCG, method_caller) 
            end for 
        else 
            for each method in class(method_callers) do 
                if method is class' constructor and method is not in Result then 
                    Result.append(method) 
                    FindFinalCaller (MCG, method) 
                else method is in Result 
                    return 
                end if 
            end for 
        end if 
    end function
    ```
2. 取得Entry Activity: 建立Activity Call Graph(ACG)
    這個psuedo code的主要目的是構建一個Activity Call Graph，識別從任意Activity到包含潛在Vulnerable View的Activity的所有可能路徑。這對於安全分析和優化應用程序的設計非常有用。通過這樣的Call Graph，開發者可以清晰地了解應用程序的Activity之間的跳轉關系，尤其是涉及到Vulnerable View的路徑，從而有針對性地進行安全防護和性能優化。一些複雜的事件（如Swipe和長按）會被忽略，因為它們不太可能觸發 HTTPS 連接
    演算法: 
    ```=
    Input: AndroidManifest.xml potientalVulnerableViews
    Output: ActivityCallGraph(ACG)
    function BuildACG(potientalVulnerableViews, AndroidManifest.xml)
        ACG = φ
        for each views in potientalVulnerableViews do
            EntryActivity = findActivityByViewID(views.getId)
            ActivitySet = initActivity(AndroidManifest.xml)
            ACG = Fun(EntryActivity, AvtivitySet, ACG)
        end for
        return ACG
    end function
    function Fun(EntryActivity, AtivitySet, ACG)
        for each activity in ActivitySet do
            if activity == MainActivity then
                return ACG
            end if
            if activity jump to EntryActivity By method.Event(such as Button.click) then
                ACG ∪ (activity → EntryActivity)
                fun(activity, ActivitySet, ACG)
            end if
        end for
    endfunction
    ```

### 如何模擬人類操作
UI自動化元件有三個任務:
1. 取得UI元素並操作它們
2. 減少UI元素並確定優先級
3. 運行App並管理UI狀態

當應用程式進入一個Activity時，需要取得該Activity的每一個元素，並提取該元素的屬性，例如按鈕的文字、文字方塊的輸入形式等。根據所獲得的信息，系統創建適當的事件來操作元素，以便Activity可以正常地從一個元素跳到另一個元素。例如，為複選框建立選擇事件，為文字方塊建立輸入事件。為了實現這個目標，我們使用[AndroidViewClient](https://github.com/dtmilano/AndroidViewClient)來管理元件。它可以取得UI元素，為UI元素建立適當的事件並執行特定應用程式的動態操作

### 如何高效運行-加速
為了避免相似的view重複被執行，所以用了另外一個演算法找出類似的view，以及最多只取前四個
![螢幕擷取畫面 2024-06-17 161914](https://hackmd.io/_uploads/B1A1zOTrA.png)
如果一個元件繼承自同一個父元件，並且具有相同的屬性（例如相同的大小、顏色等），那麼我們就認為它們是相同的
```=
Require: Views 
Ensure: Set of Vulnerable Views 
function SimilarViewsFinder (Views) 
    for each view in Views do 
        viewSize=view.getSize(); 
        if viewSize in viewWithSameParentAndSize then 
            viewWithSameParentAndSize[viewSize].append(view); 
        else 
            for each exitView in viewWithSameParentAndSize do 
                if difference (exitView, view ) < threshold then 
                    viewWithSameParentAndSize[exitView].append(view); 
                else 
                    viewWithSameParentAndSize[view].append(view); 
                end if 
            end for 
        end if 
    end for 
    for key in viewWithSameParentAndSize.keys do 
        if len (viewWithSameParentAndSize [ key ]) < 4 then 
            potientalVulnerableViews[key].append(viewWithSameParentAndSize[key]); 
        else 
            potientalVulnerableViews[key].append(viewWithSameParentAndSize[key][1.4]); 
        end if 
    end for 
    return potientalVulnerableViews 
end function
```

### 如何有效運行
這就回到一開始的問題，要如何保證proxy所攔截到的流量是我們正在測試的App所發出去的，作者使用Android內建的VPNService解決這個問題
![圖片](https://hackmd.io/_uploads/r1qzUdar0.png)

1. App透過socket把資料送到NIC(network interface card，網卡)
2. NIC把所有的packet都送到虛擬網卡(Virtual NIC)
3. VPN打開`/dev/tun`並且讀取裡面的data，此時data可以儲存或是改變
4. 最後，VPN將資料發送到NIC。VPN應用使用的socket必須顯式綁定到NIC，以避免data packet的無限迴圈

方法是讀取`/proc/net/tcp`和`/proc/net/tcp6`檔案來取得PID的IP及其URL。使用UsageStatsManager class可以取得目前正在執行的應用程式的PID。 PackageManager class可以取得PID和app之間的對應關係。這樣我們就可以得到每個HTTPS流量和應用程式之間的對應關係。透過比較智慧型手機和MITM攻擊工具所獲得的HTTPS流量，可以確認存在漏洞的應用程式。我們開發了一款Android流量抓取工具來實現這個功能。

## Experiment

### Dataset
從360app和google play商店中分別於2018/12以及2016/06取得1253 apps和960 apps，特別說明，他們把超過100M的app刪除，因為大部分這些app都是複雜的遊戲程式，在動態測試時會頻繁的crash
![圖片](https://hackmd.io/_uploads/HkY1KOaHA.png)

### Static Analysis
:::warning
這個table在設計上有誤，他把360app和google play下面的底線標錯了，360app應該是包含前面的count和他底下的percentage，而圖片上包含的count是屬於google play，至於google paly包含的count則是360app和google play兩者相加的結果
:::
靜態分析的結果如下，總共有30/2213(1.36%)的App無法disassembly，並且有 457 個 （20.65%） 應用程式具有潛在的易受攻擊代碼，這些應用程式被認為具有潛在的證書驗證漏洞。
![圖片](https://hackmd.io/_uploads/rJFitdaHA.png=500x)
作者把以上的結果和之前的工具AndroBugs, kingkong and appscan進行比較，結果如下，AndroBugs 在靜態檢測的檢測精度方面略優於DCDroid。但是，在沒有動態檢測的情況下，它會生成大量誤報。至於kingkong和appscan，DCDroid在靜態檢測的檢測精度方面更好。此外，他們無法檢測到 HostNameVerifier 漏洞。這兩個工具還包含許多誤報。因此，DCDroid 在靜態檢測階段並不是最好的。但是，DCDroid 的**主要優點是我們可以動態運行應用程式並刪除誤報**
![圖片](https://hackmd.io/_uploads/H1Rm6_prA.png =600x)

### Dynamic Analysis
在動態分析中，我們使用AndroidViewClient操作兩部 Android 智慧手機並運行應用程式。平均而言，每個應用程序花費 183 秒。動態檢測結果如表1所示。可以看出，來自 360app 和 Google Play 的 245 個應用被識別為存在證書驗證漏洞，占潛在漏洞代碼的 53.61%，佔所有應用的 11.07%。這表明我們數據集中有 11.07% 的應用存在證書驗證漏洞。從表中可以看出，360app中的證書驗證漏洞佔比為12.05%，Google Play中的證書驗證漏洞佔比為9.79%。360app中的易受攻擊的應用程式比Google Play中的應用程式更多。
![圖片](https://hackmd.io/_uploads/Sk8aK_TSA.png =600x)

## Discusion
1. DCDroid這套工具是有效地，但仍存在局線性
2. 在靜態分析中，判斷是vulnerable method的方式比較簡單粗暴，但是搞不好其實那些有複雜實作的method到最後也沒有安全的進行驗證工作，但這類的app，dcdroid是沒辦法分析出來的
3. 在動態測試中，為了加速而把一些相似的view捨棄，但不能保證false negative的數量有多少