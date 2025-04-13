---
title: Programming Related
tags: [名詞解釋]

category: "Terminology"
---

# Programming Related

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

## What is decorator in Python?
參考資料: https://myapollo.com.tw/blog/python-decorator-tutorial/
以下為Chat-GPT提供
在 Python 中，裝飾器（decorator）是一種用於修改函數或方法行為的高級函數。裝飾器本質上是一個函數，它接受一個函數作為參數，並返回一個新的函數。裝飾器通常用於在不修改原函數代碼的情況下，添加額外的功能或行為。

裝飾器的常見用途包括：
- 記錄日誌
- 訪問控製和權限檢查
- 緩存
- 性能計時
- 輸入驗證

以下是一個簡單的裝飾器示例，用於記錄函數的執行時間：

```python
import time
import functools

def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行时间: {end - start:.4f} 秒")
        return result
    return wrapper

@time_it
def my_function():
    time.sleep(2)

my_function()
```

在這個示例中：

1. `time_it` 是一個裝飾器函數，它接受一個函數 `func` 作為參數。
2. 在 `time_it` 函數內部，定義了一個 `wrapper` 函數。`wrapper` 函數在調用 `func` 之前記錄開始時間，在調用 `func` 之後記錄結束時間，並計算執行時間。
3. 使用 `@functools.wraps(func)` 保留原函數的元數據（如函數名和文檔字符串），以便裝飾後的函數看起來像原函數。
4. `time_it` 函數返回 `wrapper` 函數。
5. 使用 `@time_it` 語法將 `my_function` 函數應用裝飾器。這樣，當調用 `my_function` 時，實際上調用的是 `wrapper` 函數。

裝飾器可以堆疊使用，即一個函數可以被多個裝飾器裝飾，裝飾器的應用順序是從內到外。例如：

```python
@decorator1
@decorator2
def my_function():
    pass
```

等价于：

```python
def my_function():
    pass

my_function = decorator1(decorator2(my_function))
```

装饰器是 Python 中非常强大的特性，可以用于简化代码、提高代码的可读性和可维护性。

### 在Flask中，常常看到route也有用@這個東西，意思是一樣的嗎
是的，在 Flask 中，`@route` 裝飾器的作用與 Python 中的其他裝飾器類似。它們都是用於在不修改原始函數代碼的情況下，動態地修改函數或方法的行為。

在 Flask 中，`@app.route` 裝飾器用於將 URL 路徑與視圖函數關聯起來。它的作用是告訴 Flask，當訪問特定 URL 時，應該調用哪個函數來處理請求。

以下是一個簡單的 Flask 應用示例，展示了如何使用 `@app.route` 裝飾器：

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/about')
def about():
    return "About Page"

if __name__ == '__main__':
    app.run(debug=True)
```

在這個示例中：

1. `@app.route('/')` 裝飾器將根 URL (`/`) 與 `home` 函數關聯起來。當用戶訪問根 URL 時，Flask 會調用 `home` 函數，並將返回的字符串作為響應發送給客戶端。
2. `@app.route('/about')` 裝飾器將 `/about` URL 與 `about` 函數關聯起來。當用戶訪問 `/about` URL 時，Flask 會調用 `about` 函數，並將返回的字符串作為響應發送給客戶端。

裝飾器的作用是將函數與特定的 URL 路徑關聯起來，而不需要在函數內部處理 URL 路徑的邏輯。這使得代碼更加簡潔和易於維護。

裝飾器在 Flask 中的使用示例展示了它們在 Web 開發中的強大功能。通過使用裝飾器，可以輕松地將 URL 路徑與視圖函數關聯起來，從而實現路由功能。裝飾器的這種特性使得代碼更加模塊化和可讀。

## What is CMake/GCC/G++

### **CMake vs. GCC/G++ 的區別**
CMake 和 GCC/G++ 在 C/C++ 專案的開發中扮演不同的角色：

| **工具** | **功能** |
|----------|----------|
| **GCC/G++** | **編譯器**，將 C/C++ 程式碼編譯成執行檔或函式庫 |
| **CMake** | **建構系統生成工具**，用來產生 `Makefile` 或 `Visual Studio` 等建構文件，然後交給 GCC/G++ 或其他編譯器執行 |

CMake **不直接負責編譯**，它是幫助開發者組織專案並讓編譯器（如 GCC/G++）能夠正確執行的工具。

- **GCC/G++** = 工具（負責編譯程式碼）
- **CMake** = 施工藍圖（負責告訴工具如何組裝專案）

### **1. GCC/G++**
🔹 **GCC（GNU Compiler Collection）** 是一個編譯器集合，支援多種語言，包括 C、C++、Fortran 等。

- **GCC 用於編譯 C 程式**
  ```sh
  gcc main.c -o my_program
  ```
- **G++ 用於編譯 C++ 程式**
  ```sh
  g++ main.cpp -o my_program
  ```

GCC/G++ 只會處理單一或少量檔案的編譯，但對於大型專案（有很多 C++ 檔案和函式庫），管理這些文件的依賴關係會很麻煩，這時候 **CMake** 就能派上用場。

---

### **2. CMake**
🔹 **CMake 是一個建構系統生成工具**，它會根據 `CMakeLists.txt` 檔案產生適合當前環境的建構文件，例如：
- **Linux/macOS** → `Makefile`
- **Windows（Visual Studio）** → `.sln` 工程檔
- **Ninja** → `build.ninja`

然後，你可以使用 `make` 或 `ninja` 來執行實際的編譯。

### **CMake 典型用法**
```sh
mkdir build && cd build
cmake ..       # 產生 Makefile
make -j$(nproc)  # 使用 Make 來編譯
```
CMake 不會直接執行 `gcc` 或 `g++`，但它會根據**專案的需求**自動選擇合適的編譯器。

---

### **CMake 與 GCC/G++ 的關係**
CMake 和 GCC/G++ 其實是**互補關係**，CMake **負責管理建構過程**，然後讓 GCC/G++ **執行編譯**。

在 CMake 的 `CMakeLists.txt` 檔案中，你可以指定使用 GCC：
```cmake
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)
```
然後執行 CMake 時，它就會使用 **GCC/G++ 來編譯程式碼**。

---

### **何時使用 CMake？**
| **場景** | **適合工具** |
|----------|------------|
| 編譯單個 C/C++ 檔案 | `gcc` / `g++` |
| 小型專案（幾個檔案） | `make` |
| **大型專案（多個目錄、函式庫、跨平台）** | `CMake` |

---

### **g++ vs. gcc 的主要區別**
| **比較項目** | **gcc** | **g++** |
|-------------|--------|--------|
| **主要用途** | 編譯 C 程式 | 編譯 C++ 程式 |
| **編譯 C++ 時是否自動連結標準函式庫** | ❌ 否，需要手動加 `-lstdc++` | ✅ 是，會自動連結 `libstdc++` |
| **檔案預設行為** | 預設識別 `.c` 為 C 語言 | 預設識別 `.cpp` 為 C++ 語言 |
| **C++ 語法支援** | 部分支援，但預設不啟用 C++ 標準 | 完整支援 C++ |

---

### **1. `gcc` 編譯 C 程式**
如果你用 `gcc` 編譯 C 程式：
```sh
gcc main.c -o main
```
它會使用 C 語言的編譯規則。

---

### **2. `gcc` 編譯 C++ 程式（需要手動指定標準庫）**
如果你用 `gcc` 編譯 C++ 程式：
```sh
gcc main.cpp -o main
```
這會產生錯誤，因為 `gcc` **不會自動連結 C++ 標準函式庫**。你必須手動加上 `-lstdc++`：
```sh
gcc main.cpp -lstdc++ -o main
```

---

### **3. `g++` 編譯 C++ 程式（推薦方式）**
如果你用 `g++` 編譯 C++ 程式：
```sh
g++ main.cpp -o main
```
它**自動連結 C++ 標準函式庫**，不用額外加 `-lstdc++`，是**推薦的方式**。

---

### **4. `gcc` 和 `g++` 在多檔案專案的行為**

#### **混合 C 和 C++ 的專案**
假設我們有兩個檔案：
- `main.cpp`（C++ 代碼）
- `utils.c`（C 代碼）

用 `gcc` 來編譯（需要手動連結 C++ 標準庫）：
```sh
gcc main.cpp utils.c -lstdc++ -o main
```

用 `g++` 來編譯：
```sh
g++ main.cpp utils.c -o main
```
**`g++` 會自動連結 `libstdc++`，所以更方便。**

---

### **結論：該用哪個？**
| **情境** | **建議工具** |
|----------|-------------|
| **純 C 程式** | `gcc` |
| **純 C++ 程式** | `g++` |
| **C 和 C++ 混合專案** | `g++`（因為它會自動連結 C++ 標準庫） |

如果你的專案主要是 C++，**優先使用 `g++`**，因為它會處理 C++ 標準函式庫連結。如果是 C，則用 `gcc`。