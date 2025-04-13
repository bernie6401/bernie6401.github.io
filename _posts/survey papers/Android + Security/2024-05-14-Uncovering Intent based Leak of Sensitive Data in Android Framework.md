---
title: Uncovering Intent based Leak of Sensitive Data in Android Framework
tags: [Meeting Paper, NTU]

category: "Survey Papers/Android + Security"
---

# Uncovering Intent based Leak of Sensitive Data in Android Framework
###### tags: `Meeting Paper` `NTU`
:::info
Zhou, H., Luo, X., Wang, H., & Cai, H. (2022, November). Uncovering Intent based Leak of Sensitive Data in Android Framework. In Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security (pp. 3239-3252).
:::

## Background
:::spoiler [[Android] Activity基本介紹](https://ironglion.com/archives/334)
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
:::

:::spoiler [Android基本(2)-Intent基本觀念與使用釐清](https://ithelp.ithome.com.tw/articles/10231988)
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
> 
>    ```kotlin!
>    Intent intent = new Intent(FirstActivity.this, SecondActivity.class);
>    startActivity(intent);
>    ```
>    這邊我的例子是在兩個 activity 間的互動，service相關使用可以參考 google doc 中的範例。
> * 隱含意圖範例
>    ```kotlin!
>    Intent intent = new Intent();
>    intent.setAction(Intent.ACTION_VIEW);
>    intent.setData(Uri.parse("https://google.com"));
>    startActivity(intent);
>    ```
>    這邊這個例子是開啟網頁的使用，另外在 google doc 中的例子是發送電子郵件，也可以進行參考。
:::

:::spoiler What is entity in android?
> fields and classes defined in Android framework
:::

:::spoiler What is field in Android?

#### [Documentation](https://developer.android.com/reference/java/lang/reflect/Field)
> A Field provides information about, and dynamic access to, a single field of a class or an interface. The reflected field may be a class (static) field or an instance field.
>
>A Field permits widening conversions to occur during a get or set access operation, but throws an IllegalArgumentException if a narrowing conversion would occur.
---

#### [012-定義類別與建立物件](https://sites.google.com/site/dychen1127/developer-android/classnewobject)
> 在類別中, 需使用成員變數 (Member Variable) 來描述類別的屬性, 在 Java語言中又稱其為類別的欄位 (Field)。
成員變數的宣告方式, 和前面所用的一般變數差不多, 例如我們的汽車類別要有記錄載油量、耗油率, 可寫成：
>    ```java!
>    class Car{
>      double gas; //載油量
>      double eff; //耗油率
>    }
>    ```
:::

:::spoiler [what is a dex file?](https://www.reviversoft.com/file-extensions/dex?ncr=1&lang=en)
> Dalvik executable files are developer files affixed with the .dex extension, and these DEX files are used to initialize and execute applications developed for the Android mobile OS. The data stored in these DEX files includes compiled code that locates and initializes other program files of the associated application required to run the program.
:::

### Android Framework
:::spoiler What is TTY
Reference: 
[What is TTY](https://swf.com.tw/?p=622&cpage=1)
[Day 12深入Docker Container內部(上)](https://ithelp.ithome.com.tw/articles/10299117?sc=iThelpR)
> TTY的原意是"teletypewriter"（電傳打字機，早期用來操作並和大型電腦連線的終端機）

---
> 在上古時代，一台電腦是要透過多用戶進行操作的，畢竟當時的電腦很貴，要操作的事情也很繁瑣，而多個用戶自然就需要多台打字機對著電腦進行輸入。
>
>而 tty 正是英文 Teletypewriter的縮寫，但其實在現代，終端機和打字機的界線已經模糊不清，可以想像，終端機就是 tty，反之亦然
:::

:::spoiler [com.android.server.telecom.TelecomServiceImpl](https://android.googlesource.com/platform/packages/services/Telecomm/+/2750faaa1ec819eed9acffea7bd3daf867fda444/src/com/android/server/telecom/TelecomServiceImpl.java#725)
```java=725
...
/**
 * @see android.telecom.TelecomManager#getCurrentTtyMode
 */
@Override
public int getCurrentTtyMode(String callingPackage) {
    if (!canReadPhoneState(callingPackage, "getCurrentTtyMode")) {
        return TelecomManager.TTY_MODE_OFF;
    }
    synchronized (mLock) {
        return mCallsManager.getCurrentTtyMode();
    }
}
...
```
:::

:::spoiler [com.android.server.telecom.CallsManager](https://android.googlesource.com/platform/packages/services/Telecomm/+/2750faaa1ec819eed9acffea7bd3daf867fda444/src/com/android/server/telecom/CallsManager.java#467)
```java=467
...
int getCurrentTtyMode() {
    return mTtyManager.getCurrentTtyMode();
}
```
:::

:::spoiler [com.android.server.telecom.TtyManager](https://android.googlesource.com/platform/packages/services/Telecomm/+/2750faaa1ec819eed9acffea7bd3daf867fda444/src/com/android/server/telecom/TtyManager.java#61)
```java=61
...
int getCurrentTtyMode() {
    return mCurrentTtyMode;
}
...
```
:::

---
:::spoiler [Android adb基本用法教學](https://shengyu7697.github.io/android-adb/)
> adb(Android Debug Bridge)指令是開發 Android 時常用到的工具，使用 adb 指令可對 android 裝置進行除錯、測試、檔案處理、安裝/移除 apk 等的操作
:::


:::spoiler [com.android.server.adb.AdbService](https://android.googlesource.com/platform/frameworks/base/+/master/services/core/java/com/android/server/adb/AdbService.java#367)
```java=367
@Override
public FingerprintAndPairDevice[] getPairedDevices() {
    mContext.enforceCallingOrSelfPermission(android.Manifest.permission.MANAGE_DEBUGGING, null);
    if (mDebuggingManager == null) {
        return null;
    }
    Map<String, PairDevice> map = mDebuggingManager.getPairedDevices();
    FingerprintAndPairDevice[] ret = new FingerprintAndPairDevice[map.size()];
    int i = 0;
    for (Map.Entry<String, PairDevice> entry : map.entrySet()) {
        ret[i] = new FingerprintAndPairDevice();
        ret[i].keyFingerprint = entry.getKey();
        ret[i].device = entry.getValue();
        i++;
    }
    return ret;
}
```
:::

:::spoiler [com.android.server.adb.AdbDebuggingManager](https://android.googlesource.com/platform/frameworks/base/+/master/services/core/java/com/android/server/adb/AdbDebuggingManager.java#1697)
```java=1697
/**
 * Returns the list of paired devices.
 */
public Map<String, PairDevice> getPairedDevices() {
    AdbKeyStore keystore = new AdbKeyStore();
    return keystore.getPairedDevices();
}
```
:::

:::spoiler [com.android.server.adb.AdbDebuggingManager.AdbKeyStore](https://android.googlesource.com/platform/frameworks/base/+/master/services/core/java/com/android/server/adb/AdbDebuggingManager.java#1854)
```java
class AdbKeyStore {
    ...
    public Map<String, PairDevice> getPairedDevices() {
        Map<String, PairDevice> pairedDevices = new HashMap<String, PairDevice>();
        for (Map.Entry<String, Long> keyEntry : mKeyMap.entrySet()) {
            String fingerprints = getFingerprints(keyEntry.getKey());
            String hostname = "nouser@nohostname";
            String[] args = keyEntry.getKey().split("\\s+");
            if (args.length > 1) {
                hostname = args[1];
            }
            PairDevice pairDevice = new PairDevice();
            pairDevice.name = hostname;
            pairDevice.guid = fingerprints;
            pairDevice.connected = mWifiConnectedKeys.contains(keyEntry.getKey());
            pairedDevices.put(keyEntry.getKey(), pairDevice);
        }
        return pairedDevices;
    }
}
```
:::

:::spoiler [What is a stock ROM?](https://www.quora.com/What-is-a-stock-ROM)
stock rom其實就有點像是廠商為特定商品出的ROM而且廠商不會對其有其他更改
> Stock ROM: A Stock ROM/Firmware is an official software that is designed by the manufacturer for a particular device. A Truly Stock ROM is one type that does not undergo any cosmetic/functional changes in the code by hardware manufacturer. The "stock ROM" comes installed on the phone or tablet at the time of buying which is given by the device manufacturer. Stock Rom is one that doesn’t undergo any kind of modifications that is done in a custom Rom.

> Custom ROM: A “Custom Rom” is a software(OS) that is modified by user either to add, delete or Modify features or behavior which improves look and feel, design, themes, performance of OS for a particular device. Users including me love to install custom rom because they have extra features, better UI or performance compared to “Stock ROM”.
:::