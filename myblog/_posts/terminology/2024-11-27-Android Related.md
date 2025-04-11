---
title: Android Related
tags: [名詞解釋]

---

# Android Related
## Android App本身
* [[Android] Activity基本介紹](https://ironglion.com/archives/334)
    :::spoiler
    > * 什麼是Activity?
    Activity是App中，提供畫面的一個元件，
    例如：使用Google地圖App時，顯示地圖的那個畫面。
    >
    >* 只有Activity可以顯示畫面嗎？
    不是，除了Activity以外還有其他元件可以顯示畫面，
    例如：Dialog，但每一個App至少要有一個Activity，但這有個例外，如果這個App不提供介面的話也是可以不用有Activity的。
    ---
    > Activity其他注意事項
    > * 兩個Activity傳遞資訊是透過Intent
    >    ```kotlin!
    >    Intent intent = new Intent(this, TwoActivity.class);
    >    startActivity(intent);
    >    ```
    > * Intent 能傳遞的資訊大小要小於512k
    > * 每一個Activity都要在AndroidManifest中聲明
    >    ```kotlin!
    >    <manifest ... >
    >      <application ... >
    >          <activity android:name=".MainActivity" />
    >          ...
    >      </application ... >
    >      ...
    >    </manifest >
    >    ```
* [Android基本(2)-Intent基本觀念與使用釐清](https://ithelp.ithome.com.tw/articles/10231988)
    :::spoiler
    > 我們該如何從一個 activity 去啟動另外一個 activity，又或者我們要怎麼進行兩個 activity 間的資料通等等的問題，這時候最常見的方式就是使用我們今天的主角 Intent 
    > ### 種類
    >下方名稱網路上對他們的名稱有些需的差異，在這邊以 android doc 上名稱為主。
    > 1. 明確意圖(Explicit intents)：官方的說明有點冗長，講白一點就是在指定啟動元件的時候，我們直接使用名稱(完整的類別名稱)進行指定。
        例如：
        `Intent intent = new Intent(FirstActivity.this, SecondActivity.class);`
    >2. 隱含意圖(Implicit intents)：在宣告的時候不指定給特定的元件，而是針對功能、動作進行宣告，來讓定一個應用程式的元件進行處理。
        例如：在APP中開啟網頁，系統發現手機上有chrome以及預設瀏覽器提供網頁瀏覽的功能，這時候便會跳出選單讓使用者選擇。
    >
    > ### 範例
    > * 明確意圖範例
    >    `Intent intent = new Intent(FirstActivity.this, SecondActivity.class);`
    >    `startActivity(intent);`
    >    
    >    這邊我的例子是在兩個 activity 間的互動，service相關使用可以參考 google doc 中的範例。
    > * 隱含意圖範例
    >    `Intent intent = new Intent();`
    >    `intent.setAction(Intent.ACTION_VIEW);`
    >    `intent.setData(Uri.parse("https://google.com"));`
    >    `startActivity(intent);`
    >    這邊這個例子是開啟網頁的使用，另外在 google doc 中的例子是發送電子郵件，也可以進行參考。
* What is entity in android?
    > fields and classes defined in Android framework
* What is field in Android?
    :::spoiler
    [Documentation](https://developer.android.com/reference/java/lang/reflect/Field)
    > A Field provides information about, and dynamic access to, a single field of a class or an interface. The reflected field may be a class (static) field or an instance field.
    >
    >A Field permits widening conversions to occur during a get or set access operation, but throws an IllegalArgumentException if a narrowing conversion would occur.
    ---
    [012-定義類別與建立物件](https://sites.google.com/site/dychen1127/developer-android/classnewobject)
    > 在類別中, 需使用成員變數 (Member Variable) 來描述類別的屬性, 在 Java語言中又稱其為類別的欄位 (Field)。
    成員變數的宣告方式, 和前面所用的一般變數差不多, 例如我們的汽車類別要有記錄載油量、耗油率, 可寫成：
    >    ```java!
    >    class Car{
    >      double gas; //載油量
    >      double eff; //耗油率
    >    }
    >    ```
* [what is a dex file?](https://www.reviversoft.com/file-extensions/dex?ncr=1&lang=en)
    其實就是我們拿到的APK當中的執行檔
    > Dalvik executable files are developer files affixed with the .dex extension, and these DEX files are used to initialize and execute applications developed for the Android mobile OS. The data stored in these DEX files includes compiled code that locates and initializes other program files of the associated application required to run the program.
* [Android adb基本用法教學](https://shengyu7697.github.io/android-adb/)
    > adb(Android Debug Bridge)指令是開發 Android 時常用到的工具，使用 adb 指令可對 android 裝置進行除錯、測試、檔案處理、安裝/移除 apk 等的操作
* Android的簽章
    :::spoiler
    在Android系統安全中有3個主要的技術: Permission Management, Signature Authentication, 以及Sandbox Mechanism，現在主要探討的問題就是在簽章的技術底下。Android的數位簽章總共會包含三個東西: MANIFEST.MF, CERT.SF, CERT.RSA
    * MANIFEST.MF
        是一個Digest File也就是存所有更新的打包檔案的Hash Value
    * CERT.SF
        是一個Signature File，他會用SHA1計算MANIFEST.MF中的所有東西再用Base64進行Encode
    * CERT.RSA
        存放Public Key+加密演算法是哪一個+用自己的Private Key加密CERT.SF中的所有東西的結果
* 什麼是 Hybrid？
    資料來源: [React Native vs Cordova 簡介](https://medium.com/@leonsnoopy/react-native-vs-cordova-%E7%B0%A1%E4%BB%8B-3301362bc3)
    > 首先要先知道 Hybrid 的由來，簡單來說，因為現在的 APP 生命週期太短，要知道市場需要什麼樣類型的 APP，所以就需要可以快速開發 APP 出來，而使用 Hybrid 是最快且最省成本的方式，Hybrid 架構簡單來說，就是讓開發者可以透過撰寫一次程式碼，就可以建置成各種平台的應用程式，例如 iOS, Android, 或 Windows Phone。
    > 而目前 Hybrid 的架構有很多種，例如：React Native, Cordova, Capacitor, Ionic, Flutter, Xamarin, Onsen UI, Framework7，每種開發方式及優缺點都不太一樣

    資料來源:
    :::info
    Liu, Y., Zuo, C., Zhang, Z., Guo, S., & Xu, X. (2018). An automatically vetting mechanism for SSL error-handling vulnerability in android hybrid Web apps. World Wide Web, 21, 127-150.
    :::
    > Hybrid mobile Web apps的優點如下：
    > 構建速度更快、成本更低
    > 可以利用特定於裝置的功能，例如作為電話聯繫人訪問
    > 對於不同的平臺和不同的設備，開發者只需要重寫一部分的本機代碼
    > 易於維護。因為Hybrid mobile Web apps在 Web 伺服器上完成大部分工作易於維護

* 什麼是Gradle?
    資料來源: [ 認識 Gradle 專案建置自動化工具 ](https://ithelp.ithome.com.tw/articles/10129873)
    > Gradle 簡單說就是 Java 世界的 Makefile，它可以幫忙打理那些在專案開發過程中的瑣事，舉凡編譯、測試、檢查程式碼、產生文件、清理或壓縮檔案、上傳、發佈、重新啟動伺服器到送出電子郵件，都可以利用 Gradle 撰寫的 Script 來自動完成作業。

* Android Broadcast Receiver
    資料來源: [Android Broadcast Receiver 教學](https://waynestalk.com/android-broadcast-receiver/)
    > Android Broadcast Receiver 元件讓 app 可以從 Android 系統或其他 apps 接收訊息，也可以傳送訊息給 app 自己的其他元件，或是其他 apps。它類似於 publish-subscribe 設計模式。本文章將介紹如何使用 Broadcast Receiver。
    > 
    > 當有系統事件發生時，Android 系統自動地廣播事件給所有監聽該事件的 apps。例如，當使用者開啟或關係飛航模式時，系統會廣播 ACTION_AIRPLANE_MODE_CHANGED 事件。
    > App 也可以廣播事件給所有監聽該事件的 apps。當然 App 自己也可以監聽自己廣播的事件。
    > 
    > Manifest-declared receivers 指的是在 AndroidManifest.xml 中註冊的 receivers。在 <receiver/> 中設定監聽事件的 class，並且在 <intent-filter/> 中指定要監聽的事件。如果事件來源是系統或是其他的 apps，還要設定 android:exported="true"。

* What is ABI(Application Binary Interface)?
    資料來源: [Android中的ABI以及對應CPU的版本說明](https://blog.csdn.net/Dreamhai/article/details/109891208)
    > * ABI是Application Binary Interface的縮寫。
    > * ABI常表示兩個Process Module之間的接口，且其中一個module常為機器碼級別的library或操作系統。
    > * ABI定義了函數庫的調用、應用的二進制文件（尤其是.so）如何運行在相應的系統平台上等細節。
    > * Android目前支持以下七種ABI：`armeabi`, `armeabi-v7a`, `arm64-v8a`, `x86, x86_64`, `mips`, `mips64`。
    > ###  Android中的ABI與CPU
    > 每種CPU架構都有其自己支持的ABIs。可通過Build.SUPPORTED_ABIS得到根據偏好排序的設備支持的ABI列表。
    > ![圖片](https://hackmd.io/_uploads/H1fGDz_SC.png)

* ARM64 VS aarch64
    資料來源: [arm64和aarch64之間的區別](https://blog.csdn.net/qq_33121481/article/details/122602974)
    > 直接給出結論：arm64已經與aarch64合並，因為aarch64和arm64指的是同一件事。

* What is Deeplink?
    資料來源: [Deep Link教學 - 點擊網址開啟APP](https://codus.me/blog/app-musashi-deeplink.html)
    > 點擊網址開啟APP，就是 deep link，只要在APP上設定 url scheme即可。
    > ![image-editor-GXBI2mtT2G157959888112324](https://hackmd.io/_uploads/BkMpvK7w0.jpg =200x)

    更準確的說，deeplink在做的事情是實現跨App之間的跳轉，資料來源: [Android App Links 設定心得筆記](https://louis383.medium.com/android-app-links-設定心得筆記-6bd8ab212297)

## Android Framework
### React-Native 檔案結構與說明
```
$ tree -L 3 ./android
.
├── app
│   ├── build
│   │   ├── generated
│   │   ├── intermediates
│   │   ├── kotlin
│   │   ├── kotlinToolingMetadata
│   │   ├── outputs
│   │   └── tmp
│   ├── build.gradle
│   ├── debug.keystore
│   ├── my-release-key.jks
│   ├── proguard-rules.pro
│   └── src
│       ├── debug
│       ├── main
│       └── release
├── build
│   └── kotlin
│       └── sessions
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradle.properties
├── gradlew
├── gradlew.bat
└── settings.gradle
```
#### **頂層目錄的文件和Folder**
##### **`build.gradle`**
- 項目級的 Gradle 配置文件。
- 包含全局的配置，如：
  - 所用的 Gradle 插件版本。
  - Maven 倉庫位置。
  - 應用模塊的路徑。
- 它調用 `settings.gradle` 來定義哪些Module需要被構建。
##### **`gradlew` & `gradlew.bat`**
- 用於在項目中運行 Gradle 的腳本。
- **`gradlew`** 是用於 Linux/macOS 的可執行腳本。
- **`gradlew.bat`** 是用於 Windows 的批處理腳本。
##### **`gradle.properties`**
- 全局的 Gradle 屬性配置文件。
- 可以設置項目的 JVM 參數和其他優化選項，比如 `org.gradle.daemon=true` 或 `android.useAndroidX=true`。
##### **`settings.gradle`**
- 定義項目中包含的模塊（如 `app`）。
- 通常看起來像：
  ```groovy
  rootProject.name = "YourProjectName"
  include ':app'
  ```
#### **`gradle/wrapper/` Folder**
- 包含 Gradle Wrapper 的配置和二進制文件（`gradle-wrapper.jar`）。
- **`gradle-wrapper.properties`**：
    - 定義使用的 Gradle 版本。
    - 包含 Gradle 下載的路徑配置。
#### **`app/` Folder**
##### **1. `build/`**
- 自動生成的Folder，包含構建過程中的中間文件。
- **主要子Folder：**
  - **`generated/`**：自動生成的代碼文件，例如資源綁定文件。
  - **`intermediates/`**：構建的中間文件，如優化的資源和處理後的字節碼。
  - **`outputs/`**：生成的 APK 文件或其他構建產物。
  - **`tmp/`**：臨時文件。
##### **2. `build.gradle`**
- 應用級的 Gradle 配置文件。
- 定義特定模塊的依賴項和構建配置，如 SDK 版本、簽名配置等。
##### **3. `debug.keystore`**
- 默認的簽名密鑰文件，用於對 **Debug APK** 進行簽名。
- 開發階段使用，不建議在生產環境使用。
##### **4. `my-release-key.jks`**
- 自定義的密鑰庫，用於對 **Release APK** 進行簽名。
- 必須安全存儲，不然應用的簽名會失效。
##### **5. `proguard-rules.pro`**
- 用於配置 ProGuard 混淆規則。
- ProGuard 會壓縮、優化、混淆代碼以減少應用大小並提高安全性。
##### **6. `src/`**
- 包含應用的源代碼和資源。
  - **`debug/`**：特定於 Debug 構建的配置或資源。
  - **`main/`**：主要的應用代碼和資源，包括：
    - **`java/`**：Java 或 Kotlin 源代碼。
    - **`res/`**：應用的資源文件（XML、圖像等）。
    - **`AndroidManifest.xml`**：定義應用的權限、活動和服務等。
  - **`release/`**：特定於 Release 構建的配置或資源。
#### **`build/` Folder**
##### **1. `kotlin/sessions/`**
- 用於存儲 Kotlin 編譯會話信息。
- 輔助增量編譯，加快編譯速度。
#### **總結**
- 項目級文件（如 `build.gradle` 和 `settings.gradle`）配置全局的項目環境。
- 應用模塊（`app` Folder）包含具體的代碼和資源。
- 構建Folder（`build/`）保存中間文件和最終的產物。
- 密鑰文件和混淆規則等則保證應用安全和優化。