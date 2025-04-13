---
title: 如何使用Hugo+Github架設網站
tags: [problem solution]

category: "Problem Solutions"
---

# 如何使用Hugo+Github架設網站
<!-- more -->
參考資料: [為了 SEO！我離開了 Medium，改在 GitHub 上自架個人網站](https://kucw.io/blog/2021/1/from-medium-to-github/)

## 註冊Github Account & Create Github Page
參考資料: [使用 GitHub Pages 架設個人網站](https://hackmd.io/@flagmaker/BkvQphP65)

## (Optional)
參考資料: [Github Pages 自訂網域教學](https://medium.com/zrealm-ios-dev/github-pages-%E8%87%AA%E8%A8%82%E7%B6%B2%E5%9F%9F%E6%95%99%E5%AD%B8-483af5d93297)

## Hugo Step

參考資料: [使用 Hugo 在 github 部署個人網站](https://sean22492249.medium.com/%E4%BD%BF%E7%94%A8-hugo-%E5%9C%A8-github-%E9%83%A8%E7%BD%B2%E5%80%8B%E4%BA%BA%E7%B6%B2%E7%AB%99-5b2ff19f8b6)

### 安裝Hugo(latest version)
1. 在[Github Release](https://github.com/gohugoio/hugo/releases)可以找到符合自己需求的版本，目前我是選`0.145.0_windows_amd64`
2. 解壓縮到`C:\hugo\bin`
3. 設定環境變數，設定完後測試
    ```bash
    $ hugo version
    hugo v0.145.0-666444f0a52132f9fec9f71cf25b441cc6a4f355 windows/amd64 BuildDate=2025-02-26T15:41:25Z VendorInfo=gohugoio
    ```

### Deploy Website on Local
1. Create New Site
    ```bash
    $ hugo new site demo
    Congratulations! Your new Hugo site was created in D:\Life\Website\demo.
    
    Just a few more steps...
    
    1. Change the current directory to D:\Life\Website\demo.
    2. Create or install a theme:
       - Create a new theme with the command "hugo new theme <THEMENAME>"
       - Or, install a theme from https://themes.gohugo.io/
    3. Edit hugo.toml, setting the "theme" property to the theme name.
    4. Create new content with the command "hugo new content <SECTIONNAME>\<FILENAME>.<FORMAT>".
    5. Start the embedded web server with the command "hugo server --buildDrafts".
    
    See documentation at https://gohugo.io/.
    ```
2. 選擇Hugo Theme並且更新toml File
    到Hugo的[Official Demo Theme](https://themes.gohugo.io/)看哪一個theme適合自己，假設我選擇relearn這個theme，就點選Download
    ```bash
    $ cd ./demo
    $ git submodule add https://github.com/McShelby/hugo-theme-relearn.git themes/relearn # 因為我是用relearn這個theme所以URL和folder name是customize
    # 也可以直接下載zip file，不過下面在設定toml file有一個地方要修改
    $ echo theme = 'relearn'>> hugo.toml # For CMD
    $ echo "theme = 'relearn'" >> hugo.toml # For linux
    ```
    這個toml檔案就是一個config file，所以描述網站的最基本資訊
3. 新增一個測試的檔案
    ```bash
    $ hugo new posts/hello.md
    $ cat ./content/posts/hello.md
    +++
    date = '2025-04-02T19:15:29+08:00'
    draft = true
    title = 'Hello'
    +++
    ```
    hugo會在`./demo/content/posts`的地方新增一個hello.md這個檔案，並且把draft property改成false，最後deploy之後才會顯示
4. Deploy Local Server
    ```bash
    $ hugo server
    Watching for changes in D:\Life\Website\demo\{archetypes,assets,content,data,i18n,layouts,static,themes}
    Watching for config changes in D:\Life\Website\demo\hugo.toml, D:\Life\Website\demo\themes\relearn\hugo.toml
    Start building sites …
    hugo v0.145.0-666444f0a52132f9fec9f71cf25b441cc6a4f355 windows/amd64 BuildDate=2025-02-26T15:41:25Z VendorInfo=gohugoio


                       | EN
    -------------------+-----
      Pages            | 11
      Paginator pages  |  0
      Non-page files   |  0
      Static files     |  0
      Processed images |  0
      Aliases          |  0
      Cleaned          |  0
    
    Built in 163 ms
    Environment: "development"
    Serving pages from disk
    Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
    Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
    Press Ctrl+C to stop
    ```
    ![圖片](https://hackmd.io/_uploads/SkoITccp1e.png)
    現在Local的deployment已經完成，剩下的就是deploy到Github Page

## 利用Github Action Deploy Hugo
1. 如果沒有碰過github action的人可能要先熟悉一下，這東西就是github的自動化流程，網路上有很多種action script，應該大同小異，我是用[peaceiris/actions-gh-pages](https://github.com/peaceiris/actions-gh-pages#getting-started)
    ```bash
    $ mkdir .github/workflows && touch .github/workflows/gh-pages.yml
    ```
    ```yaml=
    name: GitHub Pages
    
    on:
      push:
        branches:
          - main  # Set a branch name to trigger deployment
      pull_request:
    
    jobs:
      deploy:
        runs-on: ubuntu-22.04
        permissions:
          contents: write
        concurrency:
          group: ${{ github.workflow }}-${{ github.ref }}
        steps:
          - uses: actions/checkout@v3
            with:
              submodules: true  # Fetch Hugo themes (true OR recursive)
              fetch-depth: 0    # Fetch all history for .GitInfo and .Lastmod
    
          - name: Setup Hugo
            uses: peaceiris/actions-hugo@v2
            with:
              hugo-version: '0.145.0'
    
          - name: Build
            run: hugo --minify
            working-directory: ./demo
    
          - name: Deploy
            uses: peaceiris/actions-gh-pages@v3
            # If you're changing the branch from main,
            # also change the `main` in `refs/heads/main`
            # below accordingly.
            if: github.ref == 'refs/heads/main'
            with:
              github_token: ${{ secrets.GITHUB_TOKEN }}
              publish_dir: ./demo/public
    ```
    * on的意思是當main這個branches出現push的操作時，就要觸發這個workflow，也就是設定觸發條件的意思
    * jobs就是說明要做的事情，具體要看jobs.deploy.steps的內容
        * 因為有使用到別人的themes，並且如果是使用submodule的方式加入到git的話，submodules這個property就要設定true，但如果是直接下載的話就要設定成false
        * 因為我是使用`peaceiris`的workflow script所以uses就不用改，但hugo version就要改成latest的版本，不然會不過，像我的就是0.145.0
        * Build minify的意思是透過hugo把指定資源進行最小化處理
        * Deploy就是使用`peaceiris/actions-gh-pages@v3`這個版本的script，進行deploy，不用管具體在幹麻，需要注意的是，publish_dir是在`./demo/public`，因為hugo會把我寫的所有文章rendering之後放到./demo/public這個folder，所以我設定一個條件，如果main這個branch有變化，就把./demo/public這個folder中的所有內容，透過script更新到gh-pages
2. 設定Github的一些東西
    到自己設定的website repo首頁`https://github.com/<username>/<username>.github.io`，會看到上面有Actions和Setting兩個subpage
    ![圖片](https://hackmd.io/_uploads/SJjgXj5pyx.png)
    先到Setting > Pages
    ![圖片](https://hackmd.io/_uploads/HJZ4Xicpkg.png)
    選擇Build and deployment中的選項為==GitHub Actions==，這個的意思是，因為Github在deploy類似Hugo這樣的靜態網頁框架時，如果選擇`Deploy from a branch`，那預設就會deploy Jekyll這個框架而不是Hugo導致deployment會失敗
    如果在VScode的`GitHub Actions` Extension發現有另外一個workflow叫做`pages build deployment`那大機率就是這個地方沒有設定好，可以參考[禁用Github pages build deployment](https://blog.361way.com/2023/10/pages-build-deployment.html)
3. Push to repo
    ```bash
    $ git add .
    $ git commit -m "Init Website"
    $ git push
    ```
    丟上去到repo的時候可以透過vscode的`GitHub Actions`這個Extension查看有沒有deploy成功
    ![圖片](https://hackmd.io/_uploads/rJNFHs5a1x.png)
    有時候會出現像這樣deploy失敗的狀況，可以利用旁邊的View step logs查看具體哪邊出問題
4. (最重要的地方)更改Source變成Deploy from a branch，並且把Branch改成如下圖
    ![圖片](https://hackmd.io/_uploads/BywW0hcaJe.png)
    這邊的邏輯是: 
    1. 從 master (或 main) 分支的 Hugo 原始碼建置 (`hugo --minify`)
    2. 將建置結果 (./demo/public/) 部署到 `gh-pages` 分支
    3. GitHub Pages再從`gh-pages` branch提供網站

    之後Source就不需要再改回`GitHub Actions`了
5. 如果之後要跟新文章，就直接像一般的git push那樣固定的add->commit->push這樣的流程就可以了，GitHub Actions會自己把東西deploy到public pages