---
title: How to use ZAP/Burp Suite/mitmproxy as Proxy for Android?
tags: [problem solution]

category: "Problem Solutions"
---

# How to use ZAP as Proxy?
* 根據[^zap-turorial]我大概知道怎麼使用，我們通常會使用zap的command line形式進行操作，詳細的參數可以參考[Official Document](https://www.zaproxy.org/docs/desktop/cmdline/)，另外我看ZAP如果要當作Proxy的角色會需要用到ROOT CA憑證，所以如果單純用之前的教學文章會不知到在哪裡產生憑證，他已經移動到Network底下了
![image](https://hackmd.io/_uploads/B11DaMnpT.png =400x)

* 目前我把Proxy架好了，看的是[這篇教學文章-OWASP ZAP操作手冊](https://hackmd.io/@ZLgd0D1pQcyasZhkkWKG4g/HyFZFPDQu)，講的非常詳細
    1. 在Firefox中搜尋憑證或是cert，直接安裝在ZAP產生的憑證檔案
    2. 在Firefox的setting中搜尋Proxy
        ![圖片](https://hackmd.io/_uploads/HJ4NI5Aap.png =400x)
    2. 設定成如下
        ![圖片](https://hackmd.io/_uploads/HJoGB9CTa.png =400x)
    只要ZAP有打開，就可以連線出去，但如果Proxy已經setup，卻沒有打開ZAP會通不到外面喔
## 補充
1. 如果上述的步驟已經執行完但Proxy只能攔截到GET Method的封包，就代表憑證爛掉了，和在手機上一樣，但手機會出現這個問題還有可能是SSL Pinning，網頁端只需要重新安裝ZAP Generate的新憑證就好
2. 如果設定Firefox的Proxy時，是設定成`使用系統Proxy設定`，那就要在電腦的設定中，更改Proxy的config
    ![圖片](https://hackmd.io/_uploads/HJ6STMP1R.png =400x)
    這樣的話ZAP也可以正常運作，但是就不會出現ZAP特定的畫面(功能)
    ![圖片](https://hackmd.io/_uploads/ByAxAfPyA.png =400x)
    只有設定成`手動設定Proxy`才會出現，否則會變成連線不上的畫面
    ![圖片](https://hackmd.io/_uploads/B1vHRzPJ0.png)

# How to use Burp Suite as Proxy?
這個完全是翻譯並且按照[ Intercepting Android App Traffic with BurpSuite ](https://youtu.be/xp8ufidc514?si=4y0JhxW0kbnO1HjF)的影片教學

## Prepare
### (有取得Root實機的情況下)
如果要保險一點零失敗的達成目標，按照影片的步驟和環境比較好，如果是已經有一台取得Root的實機，就可以忽略用VMware開的Emulator
* 取得Burp Suite Cert(在開啟Burp Suite的前提下)
    有關於DER和PEM的背景知識可以參考[[背景知識] 憑證的格式 PEM 與 DER | 自然人憑證開發筆記](https://medium.com/chouhsiang/背景知識-pem-與-der-dad659e0a40d)
    ```bash!
    $ curl localhost:8080/cert -o cert.der

    # 這一段是強制把der檔案轉換成pem檔案
    $ openssl x509 -inform der -in cert.der -out cert.pem
    ```
* 丟到手機端後直接在手機安裝憑證
* 接著就要參考[How to Root Android Phone & Install AlwaysTrustUserCert.zip Module?](https://hackmd.io/nAJIgt13TjSZ5nqLR4-BiQ#Install-AlwaysTrustUserCertzip-Module)這篇文章下面註解的地方重新安裝AlwaysTrustUserCert.zip這個plugin，最保險的做法是
    先把之前所有安裝的憑證刪除→
    重新啟動→
    重新安裝"所有"的憑證→
    重新安裝Magisk模組→
    Reboot
    接著就直接跳到下一段(實際攔截前)
### (利用VMware開Emulator)
* VMware 記得啟動 Virtualization
* 安裝Genymotion, virtualbox, adb
    安裝前先到Genymotion官網註冊帳號
    ```bash!
    $ wget https://dl.genymotion.com/releases/genymotion-3.6.0/genymotion-3.6.0-linux_x64.bin
    $ chmod +x genymotion-3.6.0-linux_x64.bin
    $ ./genymotion-3.6.0-linux_x64.bin
    $ sudo apt install virtualbox adb -y
    $ cd genymotion
    $ ./genymotion # login to genymotion
    ```
* 選擇Emulator的手機型號就可以開啟一個全新的Emulator
* 取得Burp Suite Cert(在開啟Burp Suite的前提下)
    有關於DER和PEM的背景知識可以參考[[背景知識] 憑證的格式 PEM 與 DER | 自然人憑證開發筆記](https://medium.com/chouhsiang/背景知識-pem-與-der-dad659e0a40d)
    ```bash!
    $ curl localhost:8080/cert -o cert.der

    # 這一段是強制把der檔案轉換成pem檔案
    $ openssl x509 -inform der -in cert.der -out cert.pem

    # 這一段是顯示cert.pem這個檔案Subject的MD5 Hash Value，至於他怎麼做hash的，可以參考https://github.com/spacemonkeygo/openssl/issues/112#issuecomment-443313713，他解釋該hash的標的為哪些，並不是針對這整個file做hash
    $ openssl x509 -inform PEM -subject_hash_old -in cert.pem
    9a5ba575
    -----BEGIN CERTIFICATE-----
    MIIDpzCCAo+gAwIBAgIEdz+xgjANBgkqhkiG9w0BAQsFADCBijEUMBIGA1UEBhML
    UG9ydFN3aWdnZXIxFDASBgNVBAgTC1BvcnRTd2lnZ2VyMRQwEgYDVQQHEwtQb3J0
    U3dpZ2dlcjEUMBIGA1UEChMLUG9ydFN3aWdnZXIxFzAVBgNVBAsTDlBvcnRTd2ln
    Z2VyIENBMRcwFQYDVQQDEw5Qb3J0U3dpZ2dlciBDQTAeFw0xNDA4MjgxMzUxMzda
    Fw0zMzA4MjgxMzUxMzdaMIGKMRQwEgYDVQQGEwtQb3J0U3dpZ2dlcjEUMBIGA1UE
    CBMLUG9ydFN3aWdnZXIxFDASBgNVBAcTC1BvcnRTd2lnZ2VyMRQwEgYDVQQKEwtQ
    b3J0U3dpZ2dlcjEXMBUGA1UECxMOUG9ydFN3aWdnZXIgQ0ExFzAVBgNVBAMTDlBv
    cnRTd2lnZ2VyIENBMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwCM2
    OEX9sby5W3ck1djqnohtIpNKIkBWw0qvwDfi17Hvyc0YIUPzQE+6o/a1KRgCS6Ni
    2SgcJ/soKcRkMn5nmI5Mh+6w0NGEd13VmIcSkd97RghpeNivd5u0LOHW4KVYmxh9
    0pDlt+6DD2zQIShM0hxUTGpaaPaRk9S9z0kWHNyJ9cfy627IWDSl1oNrQvNYTWU4
    DhjBa0AOQUjCrTqkCALwCEAErZRGgjeonkola117DFG8twdjdA+55Iegw2Bd8ogd
    JafibIUutXwGFiaAxx/ckapkqUKFnjBbXwyfoFmeiuiHqB3oy8Y8tduSh1e9lJNq
    bMWW+UDG/4H5kXNOgwIDAQABoxMwETAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3
    DQEBCwUAA4IBAQAn4BB23JUP0EThzsQY/299zJW0Z1AquMwYRYtWhhno+OoQ8gHu
    zKNQHdV2RHr/Ns4z7tP7aNyWiCgSmmOwJ/0l7pY74NjxbZPdqVnHMy5Vg6ehggOH
    ShKk6N561W4856G2AaiOqtY1a84wj1l5GtAtSbfVJtu3SdOvdiR2oD8C8IWx71VN
    EGjEuIkbWdyysVQkhXkn1GAl8E3CRPqDrqJL4HA9CSAPEvvhbpUvJ/j+dqp+bH68
    kPBVOVVKdzUBbngYeRpSwGm2WlbZ8RiWoeodsixPKiK2tSqtGG+D1H/bOKH/aq8x
    PVGwpBZqfagUIDw+E1x1zmbtUkpY5nHCAcEo
    -----END CERTIFICATE-----
    
    # 複製cert.pem並改名成9a5ba575.0，會改成這樣是因為手機當中儲存憑證的方式就是這樣
    $ cp cert.pem 9a5ba575.0
    
    # 這一段是print出9a5ba575.0的subject，也就是上面做hash的標的就是下面這一串東西，所以只要是PortSwigger的憑證，只要他們沒有改subject，基本上做hash得到的結果都會是9a5ba575
    $ openssl x509 -inform PEM -subject -in 9a5ba575.0
    subject=C = PortSwigger, ST = PortSwigger, L = PortSwigger, O = PortSwigger, OU = PortSwigger CA, CN = PortSwigger CA
    ```
* 丟到手機端中儲存憑證的絕對位址
    如果直接用adb push到該位置，會發現錯誤，原因是該位置是read only的狀態，所以我們要進到su進到root權限改變read only的狀態，再把東西丟進去就完成安裝了
    ```bash!
    $ adb shell
    # su
    # mount -o remount,rw /
    # exit
    # exit
    $ adb push 9a5ba575.0 /system/etc/security/cacerts/
    ```
## 實際攔截前
1. 打開的Burp Suite一定要把Bind to address改成All interfaces
    ![圖片](https://hackmd.io/_uploads/B1HBnVVPR.png =400x)
2. 設定手機端的網路Proxy
    這一部分就跟ZAP當初設定的時候一模一樣，當然也是可以像教學影片那樣用CLI的方式處理
    ```bash!
    $ adb shell settings put global http_proxy <proxy server ip>:8080 # set phone proxy
    $ adb shell settings put global http_proxy :0 # unset phone proxy
    ```
3. 接下來就可以實際攔截了

## Bypass SSL Pinning by Frida
還記得之前做的實驗[論文筆記](https://hackmd.io/@SBK6401/r155hduCT#無法使用)中有提到，有一部分的app就算安裝了SSL Unpinning的Plugin還是無法攔截到流量，根據[Defeating Android Certificate Pinning with Frida](https://httptoolkit.com/blog/frida-certificate-pinning/)文章的說明，Facebook各式各樣的App所使用的憑證標準和實作方式都是自定義的，而不是用標準API，這樣的話用一般的SSL Unpinning就還是不會成功
> Notably some apps which will go above and beyond, by implementing their own custom certificate pinning techniques from scratch, to make disabling it as difficult as possible. The prime example of this is the various Facebook apps, which all use their own custom reimplementation of TLS rather than the standard platform APIs.
>
> It's definitely possible to automatically remove certificate pinning features from that too within the same Frida script in theory (contributions very welcome!), but it's significantly more difficult than mocking out a well-known common library, so I haven't done that yet, and so this script won't work for Facebook, Facebook Messenger, Instagram, or similar.

所以通過上述教學影片，我們可以用Frida搭配特定App的腳本去Hook特定App中的特定Function，讓我們能夠在Proxy中攔截到流量
1. 安裝Frida-tools和Frida-server
    ```bash
    $ conda create --name proxy python=3.11 -y
    $ pip install frida-tools
    ```
    接著按照[官網](https://frida.re/docs/android/)的說明安裝frida-server
    1. 先從手機看架構
        以我的Google Pixel 6a來說，架構是aarch64
        ```bash!
        $ adb shell uname -a
        Linux localhost 5.10.157-android13-4-00001-g914e947b041d-ab10144456 #1 SMP PREEMPT Tue May 16 08:47:42 UTC 2023 aarch64 Toybox
        ```
    2. 再到[github releases](https://github.com/frida/frida/releases)下載最新的server
        此時我要選的版本就是frida-server-{version number}-android-arm64.xz
        ![圖片](https://hackmd.io/_uploads/S1S234ND0.png)
    3. 解壓縮後放到手機端上並且啟動這個frida-server
        ```bash!
        $ mv frida-server-16.2.5-android-arm64 frida-server # rename it
        $ adb push frida-server /data/local/tmp/
        $ adb shell "chmod 755 /data/local/tmp/frida-server"
        $ adb shell "/data/local/tmp/frida-server &"
        ```
2. 下載Instagram的腳本
同樣根據影片教學，到[Eltion/Instagram-SSL-Pinning-Bypass](https://github.com/Eltion/Instagram-SSL-Pinning-Bypass?tab=readme-ov-file)下載最關鍵的.js script，他裡面還有其他的App Script，包含threads和messager之類的
    ```bash!
    $ wget https://raw.githubusercontent.com/Eltion/Instagram-SSL-Pinning-Bypass/main/instagram-ssl-pinning-bypass.js
    ```
4. 啟動Burp Suite和腳本
    **Run腳本之前把Instagram的App強制停止**
    ```bash!
    $ frida -U -l ./instagram-ssl-pinning-bypass.js -f com.instagram.android
         ____
        / _  |   Frida 16.2.1 - A world-class dynamic instrumentation toolkit
       | (_| |
        > _  |   Commands:
       /_/ |_|       help      -> Displays the help system
       . . . .       object?   -> Display information about 'object'
       . . . .       exit/quit -> Exit
       . . . .
       . . . .   More info at https://frida.re/docs/home/
       . . . .
       . . . .   Connected to Pixel 6a (id=24121JEGR04513)
    Spawning `com.instagram.android`...
    [*][*] Waiting for libliger...
    Spawned `com.instagram.android`. Resuming main thread!
    [Pixel 6a::com.instagram.android ]-> [*][+] Hooked checkTrustedRecursive
    [*][+] Hooked SSLContextInit
    [*][+] Found libliger at: 0x76a3404000
    [*][+] Hooked function: _ZN8proxygen15SSLVerification17verifyWithMetricsEbP17x509_store_ctx_stRKNSt6__ndk112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEPNS0_31SSLFailureVerificationCallbacksEPNS0_31SSLSuccessVerificationCallbacksERKNS_15TimeUtilGenericINS3_6chrono12steady_clockEEERNS_10TraceEventE
    ```
    `-U`代表目標是USB連接的Device
    `-l`代表要運行的Script
    `-f`代表腳本的目標為何
5. 查看Burp Suite
    此時如果Burp Suite有開Intercept，並且App有送出一些東西，理論上都會被攔截到
## 對比
### 沒有使用Frida的時候
會得到以下截圖
![Screenshot_20240523-101015](https://hackmd.io/_uploads/Bk7aFN37R.png#pic_center =200x)
並且Burp Suite沒有得到任何關於instagram的封包
### 有使用Frida的時候
例如我在前面的登入介面輸入一些東西，可以在封包紀錄中找到我輸入的Username和Password
![Screenshot_20240523-120440](https://hackmd.io/_uploads/H1-tlBhXR.png =200x)
可以在傳輸的封包中找到這個json parameter body，而我輸入的Username: testqqqqqqwwwwww也的確在其中
![圖片](https://hackmd.io/_uploads/SygolHnm0.png)
```jsonld
{
  "client_input_params": {
    "device_id": "android-70ea1739c3d78fb5",
    "login_attempt_count": 1,
    "secure_family_device_id": "",
    "machine_id": "Zk6_IgABAAFG881bw25QVFTkQhJH",
    "accounts_list": [],
    "auth_secure_device_id": "",
    "has_whatsapp_installed": 0,
    "password": "#PWD_INSTAGRAM:1:1716436802:ASkUVtbquYjqR+MxW5sAAQJv9IFYeA7RM5r8OEvSkEDf6+0YsJ0oKKAkfx7o9AM5hpZW1TQV6POf1fg8uLC1E+gCgyqCwZiyCHYgqO3XDol2g2HFrwpNMwMn1S15LGjT9i8TEfh+k8hPuNFwGkEpLll6ycMur34gdx2V0vewuHlDOZapFmVetj+odQVW0u4WLwJybvKcFMdGGYWH7BqhmSsMjCFOBPzeflgf5fHQdxV14NWekpCWHED3LVwdISxa/yHvaYoc1EICz/O3wJO56aU3Y2zNQttBxKxuhCeS59sexNwaiz10hFMe9mb/0BD158z5Nn9x+3b5XDy24v3mNNHA4F6jkdiGwy8pAI0a/4X+yiOt5bVOCsinfGbso22kC6YnYq8dbBlUHD5zKTlKow8E",
    "sso_token_map_json_string": "",
    "family_device_id": "23045e76-6a5c-4886-8eca-0936fdb5f76b",
    "fb_ig_device_id": [],
    "device_emails": [],
    "try_num": 1,
    "lois_settings": {
      "lois_token": "",
      "lara_override": ""
    },
    "event_flow": "login_manual",
    "event_step": "home_page",
    "headers_infra_flow_id": "",
    "openid_tokens": {},
    "client_known_key_hash": "",
    "contact_point": "testqqqqqqwwwwww",
    "encrypted_msisdn": ""
  },
  "server_params": {
    "should_trigger_override_login_2fa_action": 0,
    "is_from_logged_out": 0,
    "should_trigger_override_login_success_action": 0,
    "login_credential_type": "none",
    "server_login_source": "login",
    "waterfall_id": null,
    "login_source": "Login",
    "is_platform_login": 0,
    "INTERNAL__latency_qpl_marker_id": 36707139,
    "offline_experiment_group": null,
    "is_from_landing_page": 0,
    "password_text_input_id": "0:96",
    "ar_event_source": "login_home_page",
    "username_text_input_id": "0:95",
    "layered_homepage_experiment_group": null,
    "should_show_nested_nta_from_aymh": 1,
    "device_id": null,
    "INTERNAL__latency_qpl_instance_id": 217,
    "reg_flow_source": "cacheable_aymh_screen",
    "is_caa_perf_enabled": 1,
    "credential_type": "password",
    "caller": "gslr",
    "family_device_id": null,
    "INTERNAL_INFRA_THEME": "harm_f",
    "is_from_logged_in_switcher": 0
  }
}
```
# How to use mitmproxy as Proxy?
這有點小複雜，我看網路上的教學有時候都東漏西漏，
1. 安裝mitmrproxy
    我是直接用`$ pip install mitmproxy`，並且直接run起來，`$ mitmweb`
2. 下載憑證
    如果一開始拿到的手機就是已經Rooted，那就直接下載憑證就好，我是用電腦版下載，首先把電腦上的proxy設定起來
    ![圖片](https://hackmd.io/_uploads/HJ5drE4wC.png =300x)
    並且在瀏覽器上打 http://mitm.it 然後就會看到以下畫面
    ![圖片](https://hackmd.io/_uploads/Bk-cINNP0.png =300x)
    如果沒有先設定電腦上的proxy，他預設並不會走mitmproxy，這時候再瀏覽同一個網站就會出現以下畫面
    ![圖片](https://hackmd.io/_uploads/H1dmI4NPC.png)
    這時我們們就可以直接選取android要得憑證
3. 把憑證放到手機上並且依照[How to Root Android Phone & Install AlwaysTrustUserCert.zip Module?](https://hackmd.io/@SBK6401/r1pDCcqCT#注意事項)中最後的注意事項進行安裝，也就是先把之前所有安裝的憑證刪除→重新啟動→重新安裝"所有"的憑證→重新安裝Magisk模組→Reboot，就可以了
    此時檢查手機中的的Trusted credentials應該就會發現mitmproxy的憑證已經被信任
    ![Screenshot_20240704-225258](https://hackmd.io/_uploads/B1v_PE4vC.png =200x)
4. 設定手機的Proxy IP
    我是直接用電腦的hot spot來測試，所以手機就填電腦IP和8080的Port
5. 攔截流量
    此時一切幾乎準備就緒，但有個小問題，如果按照前面的command，會一直出現以下問題
    ![圖片](https://hackmd.io/_uploads/r1Huu44PA.png =400x)
    根據[Stackoverflow](https://stackoverflow.com/questions/52068746/mitmproxy-client-connection-killed-by-block-global)的說明，我們可以加上set參數
    ```bash
    $ mitmweb --set block_global=false --set view
    ```
    就可以順利攔截到流量了
    ![圖片](https://hackmd.io/_uploads/SkYGtVEwA.png)

# Reference
[^zap-turorial]:[網頁安全性測試：OWASP ZAP使用入門](https://www.tpisoftware.com/tpu/articleDetails/2161)