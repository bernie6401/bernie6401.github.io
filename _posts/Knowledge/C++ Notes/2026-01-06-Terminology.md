---
layout: post
title: "Terminology"
date: 2026-01-06
category: "Knowledge｜C++ Notes"
tags: []
draft: false
toc: true
comments: true
---

<!-- more -->

# Terminology
* Class(類別): 類似藍圖的概念
* Object(物件): Class的，也就是Class的Instance
* Data Member: Class 中的 Variable
* Member Function: Class中的Function，和**Method**類似
* Constructor: 開一個Class的Instance時，預設會執行的初始化Function，就類似Python的`__init__`，只要在Class中創一個名稱為`{Class Name}`的function，就可以當作constructor
* Private: 只有該Class可以使用
* Public: 其他Class可以使用
* Protected: 繼承父類別的子類別可以使用，但類別以外的地方，就無法使用

## Keyword
### Storage-class Specifiers
C++提供五個不同的keyword決定lifetime、scope、linkage
* auto: 自動讓編譯器推導data type
    ```c++
    auto double x;
    ```
* extern
* register: c時代的遺物，拜託compiler把變數放在CPU暫存器
* mutable:
* static: static是最重要的
    1. Local Variable的Static: 只初始化一次，值會保留，常用來<span style="background-color: yellow">記住上次的狀態</span>
    2. Global Variable的Static: 限制只能在此file中使用
    3. Class中的Static: 屬於class而不是物件，所有object共用一份
        ```c++
        class A{
            public: 
            static int x;
        };

        int A::x=10;
        ```

|Keyword|主要用途|Lifetime|Scope|
|---|---|---|---|
|auto|(default)Local Variable|Block|Block|
|register|放暫存器|Block|Block|
|extern|使用外部Variable/Function|Global|跨File|
|static|保存狀態/限制可見性|Global|視位置而定|
|mutable|只用於class成員，允許修改const變數|Object的Lifetime|class|

### class相關
* friend
* explicit
* export
* template
* this: 類似Python的`self`，都是用來指向物件本身
* inline: 通常用於inline function，程式較少的副程式，沒有function call、push/pop stack也沒有call/ret，會直接寫死在main program中，會比較快
    ```c++
    inline double cube(const double side)
    {
        return side * side * side;
    }

    int main(){
        double sideValue = 10.5;
        cout << cube(sideValue) << endl;
    }
    ```

### Pure Virtual Function
* virtual: 會用在class中修飾member function，意思是該member function不給出確切實作，而是交由被繼承的子類別個別定義，重點是**等於0**
    ```c++
    virtual return_type function_name(...) = 0;
    ```
* 以下這三個東西都屬於 C++ 的 RTTI（Run-Time Type Information，執行期型別資訊），用來在「多型（polymorphism）」情境下，在執行時判斷物件的真實型別。
    * dynamic_cast: 在繼承關係中，安全地做「向下轉型（downcast）」，成功條件是
        * Base 必須是 polymorphic class（有 virtual）
        * b 實際指向 Derived 物件
        * 轉型方向必須在繼承樹中合法
        ```c++
        Base* b = new Derived();
        Derived* d = dynamic_cast<Derived*>(b);
        ```
    * typeid: 在執行期取得「實際型別資訊」
        ```c++
        Base* b = new Derived();
        cout << typeid(*b).name() << endl;
        ```
    * type_info: 主要用途是typeid 的回傳型別
        ```c++
        if (typeid(*b) == typeid(Derived)) {// 真的是 Derived}
        ```

### 其他
* enum: 把一組⌈有限、固定選項⌋，用有意義的名字表示，本質上還是整數，只是比較好讀
    ```c++
    enum Status {CONTINUE, WON, LOST}; // 定義新的data type Status，定義CONTINUE是0，WON是1，LOST是2
    Status gameStatus;

    if (gameStatus == WON) {cout << "You win" << endl;}
    else if (gameStatus == LOST) {cout << "You lost" << endl;}
    else if (gameStatus == CONTINUE) {cout << "Continue" << endl;}
    ```
* sizeof
* struct
* typedef
* union
* volatile
* compl
* const_cast
* new: 開一個記憶體空間出來給某個物件，比方說class instance, vector等等
* reinterpret_cast
* static_cast: 要`# include <iomanip>`，目的是暫時改變某個variable的data type變成另外一個data type，運算完就消失了
    ```c++
    // total 原本是int，暫時變成double這個type
    average = static_cast<double>(total) / gradeCounter;
    ```
* typename
* using
* wchar_t

## 其他
* EOF(End of File)是`Ctrl+Z`
* Scope Resolution Operator(::): 代表這個東西在某個namespace/class/global中`ing num = 7; int main(){cout << ::num << endl;}`
* subscript/index: 在Array中，代表`[]`的數值，`[0]`含數字的叫做subscript notation

### Data Type

| 型別                    | 常見大小*       | 說明               |
| --------------------- | ----------- | ---------------- |
| `bool`                | 1 byte      | `true` / `false` |
| `char`                | 1 byte      | 字元或小整數           |
| `signed char`         | 1 byte      | 有號字元             |
| `unsigned char`       | 1 byte      | 無號字元             |
| `short` (`short int`) | 2 bytes     | 短整數              |
| `unsigned short`      | 2 bytes     |                  |
| `int`                 | 4 bytes     | 最常用整數            |
| `unsigned int`        | 4 bytes     |                  |
| `long`                | 4 或 8 bytes | 視平台              |
| `unsigned long`       | 4 或 8 bytes |                  |
| `long long`           | 8 bytes     | 長整數              |
| `unsigned long long`  | 8 bytes     |                  |
| `float`       | 4 bytes      | 單精度      |
| `double`      | 8 bytes      | 雙精度（最常用） |
| `long double` | 8 / 16 bytes | 高精度      |

## Standard Library
* `<cstdlib>`: 處理記憶體/系統/轉型的問題(malloc/calloc/realoc/free/atoi/atol/strtol/strtod/rand/srand/exit/abort/getenv/qsort/bsearch)
* `<cctype>`: 字元分類及轉換(isdigit/isalpha/isalnum/isspace/toupper/tolower)
* `<cstring>` / `<string>`: 字串處理(strlen/strcpy/strncpy/strcat/strcmp/strncmp/strchr/strstr/memcpy/memmove/memset/memcmp)，後者的差別是實行自動化管理memory且安全性較高(s.size(), s.length()/s+t+u+.../s.substr())
* `<fstream>`: 處理file的讀取和寫入
* `<cassert>`: debug用，用來檢查理論上一定要成立的條件`int x = 10; assert(x>0);`
* `<climits>` / `<limits>`: 是一種巨集，定義`INT_MAX`, `INT_MIN`, `CHAR_BIT`

## Standard Template Library
`<vector>`, `<list>`, `<deque>`, `<queue>`, `<stack>`, `<map>`, `<set>`, `<bitset>`