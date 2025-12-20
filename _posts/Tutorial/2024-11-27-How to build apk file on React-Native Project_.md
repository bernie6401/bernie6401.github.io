---
title: "How to build apk file on React-Native Project"
tags: [Tutorial]

category: "Tutorial"
---

# How to build apk file on React-Native Project
<!-- more -->

## **1. 確保已完成的環境設置**
### 必備工具：
1. 安裝 [Node.js](https://nodejs.org/).
2. 安裝 [Java JDK](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) (推薦 11 或更高版本)。
3. 安裝 [Android Studio](https://developer.android.com/studio) 並設置環境變量：
   - 配置 `ANDROID_HOME` 環境變量，指向你的 Android SDK 安裝路徑。
   - 將以下路徑添加到 `PATH`：
     ```
     $ANDROID_HOME/tools
     $ANDROID_HOME/tools/bin
     $ANDROID_HOME/platform-tools
     ```
4. 使用以下命令確認 Android SDK 設置正確：
   ```bash
   adb --version
   ```

---

## **2. 檢查 React Native 項目配置**
在項目中，確保以下內容已經配置：

### **文件 `android/app/build.gradle`**
確認 `minSdkVersion` 和 `targetSdkVersion` 值符合要求，例如：
```gradle
android {
    defaultConfig {
        applicationId "com.example.myapp" // 替換為你的包名
        minSdkVersion 21
        targetSdkVersion 33
    }
}
```

### **文件 `android/gradle.properties`**
啟用 ProGuard 和 Hermes 以優化 APK：
```properties
android.useAndroidX=true
android.enableJetifier=true
```

### **文件 `android/app/src/main/AndroidManifest.xml`**
確保 AndroidManifest 配置正確。

---

## **3. 生成簽名密鑰（僅限生產構建）**
如果你要構建發布版本的 APK，需要生成簽名密鑰。

1. 使用 `keytool` 生成密鑰：
   ```bash
   keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias
   ```
   - 按照提示設置密鑰密碼。
   - 這將生成一個 `my-release-key.jks` 文件。

2. 將密鑰文件移動到 `android/app` 目錄。

3. 在 `android/gradle.properties` 文件中添加簽名信息：
   ```properties
   MYAPP_RELEASE_STORE_FILE=my-release-key.jks
   MYAPP_RELEASE_KEY_ALIAS=my-key-alias
   MYAPP_RELEASE_STORE_PASSWORD=your-store-password
   MYAPP_RELEASE_KEY_PASSWORD=your-key-password
   ```

4. 修改 `android/app/build.gradle`，添加簽名配置：
   ```gradle
   android {
       signingConfigs {
           release {
               storeFile file(MYAPP_RELEASE_STORE_FILE)
               storePassword MYAPP_RELEASE_STORE_PASSWORD
               keyAlias MYAPP_RELEASE_KEY_ALIAS
               keyPassword MYAPP_RELEASE_KEY_PASSWORD
           }
       }
       buildTypes {
           release {
               signingConfig signingConfigs.release
               minifyEnabled false
               shrinkResources false
           }
       }
   }
   ```

---

## **4. 構建 APK 文件**
使用 React Native 提供的 Gradle 構建工具生成 APK。

1. 進入項目目錄：
   ```bash
   cd android
   ```

2. 構建 Debug APK：
   ```bash
   ./gradlew assembleDebug
   ```

3. 構建 Release APK：
   ```bash
   ./gradlew assembleRelease
   ```

---

## **5. 獲取生成的 APK 文件**
構建完成後，APK 文件會保存在以下路徑：

- Debug APK：
  ```
  android/app/build/outputs/apk/debug/app-debug.apk
  ```

- Release APK：
  ```
  android/app/build/outputs/apk/release/app-release.apk
  ```

---

## **6. 在設備上安裝 APK**
使用以下命令將 APK 安裝到設備：
```bash
adb install app-debug.apk
```

---

## **7. 常見問題**
- **Java 內存不足**：在 `android/gradle.properties` 文件中添加：
  ```properties
  org.gradle.jvmargs=-Xmx2048m
  ```
- **簽名錯誤**：確保密鑰信息正確，並且 `build.gradle` 配置無誤。