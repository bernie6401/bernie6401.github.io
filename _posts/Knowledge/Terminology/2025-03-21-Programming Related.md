---
title: Programming Related
tags: [名詞解釋]

category: "Knowledge｜Terminology"
date: 2025-03-21
---

# Programming Related
## 綜合
* [Thread VS Process](https://pjchender.dev/computer-science/cs-process-thread/)
<!-- more -->

## What is namespace in programming?
From ChatGPT
在程式語言中，**namespace**（命名空間）是一種用來**組織和管理代碼**的機制，目的是避免名稱衝突並提升代碼的可讀性和結構化。

---

### **Namespace 的概念與作用**
1. **名稱分隔**  
   命名空間可以將代碼中的名稱（如變數、函數、類別等）組織起來，避免與其他代碼中的名稱發生衝突。  
   - 例如，兩個不同的模組中可能都定義了名稱為 `calculate` 的函數，但由於它們位於不同的命名空間，因此可以共存。

2. **代碼組織**  
   命名空間可以將相關聯的功能分組在一起，使代碼結構更加清晰，便於維護和重用。

3. **避免名稱污染**  
   命名空間可以避免全域命名空間中的名稱被不小心覆蓋或污染，降低了意外錯誤的可能性。

---

### **Namespace 的具體表現**

#### 1. **C++**  
在 C++ 中，命名空間是通過 `namespace` 關鍵字來實現的。
```cpp
#include <iostream>

namespace Math {
    int add(int a, int b) {
        return a + b;
    }
}

namespace Physics {
    int add(int a, int b) {
        return a - b;
    }
}

int main() {
    std::cout << Math::add(3, 4) << std::endl;  // 使用 Math 的 add 函數
    std::cout << Physics::add(3, 4) << std::endl; // 使用 Physics 的 add 函數
    return 0;
}
```

#### 2. **Python**  
在 Python 中，每個模組（module）本身就是一個命名空間，通過 `import` 來使用其他命名空間的內容。
```python
# math.py
def calculate():
    return "Math calculate"

# physics.py
def calculate():
    return "Physics calculate"

# main.py
import math
import physics

print(math.calculate())   # 使用 math 的 calculate
print(physics.calculate())  # 使用 physics 的 calculate
```

#### 3. **Java**  
在 Java 中，命名空間是通過「**包（package）**」來管理的。
```java
package com.example.utils;

public class MathUtils {
    public static int add(int a, int b) {
        return a + b;
    }
}

// main.java
import com.example.utils.MathUtils;

public class Main {
    public static void main(String[] args) {
        int result = MathUtils.add(3, 4);
        System.out.println(result);
    }
}
```

#### 4. **JavaScript**  
在 JavaScript 中，命名空間可以用物件或模組的方式模擬。
```javascript
const MathNamespace = {
    add: function(a, b) {
        return a + b;
    }
};

const PhysicsNamespace = {
    add: function(a, b) {
        return a - b;
    }
};

console.log(MathNamespace.add(3, 4));  // 使用 MathNamespace 的 add
console.log(PhysicsNamespace.add(3, 4));  // 使用 PhysicsNamespace 的 add
```

#### 5. **Rust**  
Rust 使用模組（`mod`）作為命名空間的一種實現。
```rust
mod math {
    pub fn add(a: i32, b: i32) -> i32 {
        a + b
    }
}

mod physics {
    pub fn add(a: i32, b: i32) -> i32 {
        a - b
    }
}

fn main() {
    println!("{}", math::add(3, 4));   // 使用 math 的 add
    println!("{}", physics::add(3, 4)); // 使用 physics 的 add
}
```

---

### **Namespace 的好處**
1. **避免命名衝突**：在大型項目中，不同開發者可能使用相同名稱，命名空間可以讓它們彼此隔離。
2. **提升可讀性**：命名空間為名稱提供了上下文，開發者可以更清楚其來源。
3. **方便管理**：將功能模組化，便於管理和維護代碼。

---

### **總結**
命名空間的核心目的是為了**組織代碼並避免名稱衝突**。它在不同語言中的具體實現可能有所不同，但基本理念是一致的：提供一個結構化的方式來管理代碼名稱和功能。


## .NET平台是什麼
是 Microsoft 推出的跨平台軟體開發平台，用來開發各種類型的應用程式，例如桌面程式、網站、後端 API、行動 App、雲端服務，甚至是遊戲。可以把 .NET 想成是一整套「開發生態系」，而不只是一個語言。<span style="background-color: yellow">**一個讓你用多種語言，寫一次程式，就能在多種作業系統上跑的開發平台**</span>

### 支援的語言
* C#（最主流、最推薦）
* F#
* Visual Basic (VB.NET)

### 開發框架

| 用途       | 技術               |
| -------- | ---------------- |
| 網站 / API | **ASP.NET Core** |
| 桌面應用     | WPF / WinForms   |
| 行動 App   | .NET MAUI        |
| 遊戲       | Unity（使用 C#）     |
| 雲端       | Azure + .NET     |

### .NET 的運作概念
和以下的概念幾乎一樣
* Java（JVM）
* Android（ART / Dalvik）

```
C# 原始碼
   ↓ 編譯
IL（中介語言）
   ↓ Runtime
作業系統執行
```

### 適合與不適合之處
* ✔ 想做後端 API
* ✔ 想寫 Windows 桌面程式
* ✔ 想快速開發工具
* ✔ 想進企業或微軟生態
* ✔ 想要強型別但又不想像 C++ 那麼痛苦
* ❌ 極度底層（驅動程式、核心）
* ❌ 極限效能手寫優化（雖然現在已經很強）

## Java Related
* [JVM](https://www.jyt0532.com/2020/02/14/jvm-introduction/)
* [JDK、JRE 和 JVM](https://ithelp.ithome.com.tw/articles/10264453)

## JavaScript
* [你不可不知的 JavaScript 二三事#Day3：資料型態的夢魘——動態型別加弱型別(2)](https://ithelp.ithome.com.tw/articles/10202260)
* [10. [JS] 一般函式與箭頭函式的差異？ ](https://ithelp.ithome.com.tw/articles/10221214)