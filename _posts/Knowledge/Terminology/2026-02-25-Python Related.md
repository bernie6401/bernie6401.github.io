---
layout: post
title: "Python Related"
date: 2026-02-25
category: "Knowledge｜Terminology"
tags: []
draft: false
toc: true
comments: true
---

# Python Related
<!-- more -->
## 其他基本知識
* [[Series - 8] Python時間轉換介紹](https://ithelp.ithome.com.tw/articles/10235251)
* [[第06天] 資料結構（3）Data Frame](https://ithelp.ithome.com.tw/articles/10185182)
* [【Day 9】Python打包程式](https://ithelp.ithome.com.tw/articles/10261688)
* [[Python]關鍵字yield和return究竟有什麼不同?](https://ithelp.ithome.com.tw/articles/10258195)
* [How to use multiprocess in python & map VS pool VS apply_async](https://www.wongwonggoods.com/all-posts/python/python_parellel/python-multiprocessing-pool)
* [Python asyncio 從不會到上路](https://myapollo.com.tw/blog/begin-to-asyncio/)


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

等價于：

```python
def my_function():
    pass

my_function = decorator1(decorator2(my_function))
```

裝飾器是 Python 中非常强大的特性，可以用于簡化code、提高code的readability和可維護性。

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