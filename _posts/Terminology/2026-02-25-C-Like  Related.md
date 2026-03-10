---
layout: post
title: "C-Like  Related"
date: 2026-02-25
category: "Terminology"
tags: []
draft: false
toc: true
comments: true
---

# C-Like  Related
* [C#編譯到執行與Java的相似之處](https://ithelp.ithome.com.tw/articles/10217608)
* [C語言雜談01---如何理解條件編譯](https://ithelp.ithome.com.tw/articles/10283174)
<!-- more -->


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


## MSVC VS. MinGW
都是編譯C++的編譯器

### 編譯器來源

| 編譯器                             | 來源 / 背景                    |
| ------------------------------- | -------------------------- |
| **MSVC (Microsoft Visual C++)** | 微軟官方，Visual Studio 內建編譯器   |
| **MinGW / MinGW-w64**           | GCC 在 Windows 的移植版本，開源社群維護 |

### Standard Library & ABI

| 特性      | MSVC                       | MinGW                      |
| ------- | -------------------------- | -------------------------- |
| C++ 標準庫 | MSVC STL (`std::vector` 等) | GCC STL (`libstdc++`)      |
| C++ ABI | Microsoft C++ ABI          | GCC C++ ABI                |
| 互通性     | **不與 GCC 編譯的二進制互通**        | 與 Linux/Unix 上 GCC 二進制互通性高 |

> ⚠️ 因此，MSVC 編譯的 .lib / .dll 不能直接和 MinGW 的 .a / .dll 混用（除非用 C 介面）

### 編譯器選項與鏈結方式

| 特性      | MSVC                       | MinGW                          |
| ------- | -------------------------- | ------------------------------ |
| 命令行     | `cl main.cpp /Fe:main.exe` | `g++ main.cpp -o main.exe`     |
| 靜態連結標準庫 | `/MT`                      | `-static`                      |
| 動態連結標準庫 | `/MD`                      | 預設（依賴 DLL，如 `libstdc++-6.dll`） |

### 適合場合
#### MSVC
* 開發 Windows 原生程式 / GUI / .NET 互通
* 發布 DLL 或 exe 給 Windows 使用者
* 使用 Visual Studio 生態系（Debugger、Profiler、IntelliSense）
#### MinGW
* 跨平台開發（程式在 Linux / Windows / macOS 可用 GCC 編譯）
* 想用 GCC / Makefile / Autotools 工具鏈
* 開源專案，或不依賴 Visual Studio