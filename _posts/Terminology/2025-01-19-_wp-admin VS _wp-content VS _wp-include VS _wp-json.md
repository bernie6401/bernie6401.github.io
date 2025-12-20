---
title: /wp-admin VS /wp-content VS /wp-include VS /wp-json
tags: [problem solution]

category: "Terminology"
---

# /wp-admin VS /wp-content VS /wp-include VS /wp-json
<!-- more -->
From Chat-GPT:

### 1. **`wp-admin`**
   - **用途**: WordPress 的後台管理系統。
   - **位置**: `/wp-admin/`
   - **內容**:
     - 包含所有與管理後台相關的 PHP 文件（如控制面板、用戶管理、文章管理等）。
     - 提供網站管理者的操作界面。
   - **訪問權限**: 需要用戶登錄並具備管理員或其他授權身份才能訪問。

   **範例**:
   - `http://example.com/wp-admin/`：進入 WordPress 後台儀表板。
   - `http://example.com/wp-admin/post-new.php`：進入新增文章頁面。

---

### 2. **`wp-content`**
   - **用途**: 儲存用戶生成的內容和可定制項目。
   - **位置**: `/wp-content/`
   - **內容**:
     - 主題 (`themes`)：網站外觀的所有文件。
     - 外掛 (`plugins`)：網站功能擴展的所有文件。
     - 上傳 (`uploads`)：用戶上傳的媒體文件（圖片、影片等）。
   - **訪問權限**: 通常開放訪問，因為靜態文件（如圖片或 CSS 文件）需要公開存取。

   **範例**:
   - `http://example.com/wp-content/uploads/2025/01/image.jpg`：上傳的圖片文件。
   - `http://example.com/wp-content/themes/my-theme/style.css`：主題樣式文件。

---

### 3. **`wp-includes`**
   - **用途**: 儲存 WordPress 核心功能的代碼。
   - **位置**: `/wp-includes/`
   - **內容**:
     - 包含 WordPress 核心的 PHP 函數庫和類。
     - 負責處理網站的內部邏輯，包括模板標籤、格式化工具和 API 的核心部分。
   - **訪問權限**: 通常禁止直接訪問這些文件，因為它們是內部功能實現的核心部分。

   **範例**:
   - `http://example.com/wp-includes/js/jquery/jquery.min.js`：加載 WordPress 內置的 jQuery 文件。
   - `wp-includes/functions.php`：包含核心函數。

---

### 4. **`wp-json`**
   - **用途**: 提供 REST API 端點，用於數據交互。
   - **位置**: `/wp-json/`
   - **內容**:
     - WordPress REST API 的入口點。
     - 用於開發者通過 API 操作網站數據（如獲取文章、創建用戶等）。
   - **訪問權限**: 根據 API 功能，部分公開（如獲取文章），部分需要授權（如創建、修改內容）。

   **範例**:
   - `http://example.com/wp-json/wp/v2/posts`：獲取網站的文章列表。
   - `http://example.com/wp-json/wp/v2/users`：獲取用戶數據（需授權）。

---

### 總結對比

| **名稱**         | **功能**                           | **是否可公開訪問**       | **主要存放內容**                              |
|------------------|----------------------------------|------------------------|--------------------------------------------|
| **`wp-admin`**   | 後台管理工具                       | 需要授權                | 儀表板、管理頁面相關的 PHP 文件                |
| **`wp-content`** | 儲存用戶生成的內容和可定制項目       | 通常公開訪問            | 主題、外掛、上傳的媒體文件                   |
| **`wp-includes`**| 核心功能的內部代碼                  | 禁止直接訪問            | 核心函數、類、JavaScript 庫等                |
| **`wp-json`**    | 提供 REST API 接口                 | 根據 API 設定           | 互動 API 端點，用於訪問或操作網站數據         |