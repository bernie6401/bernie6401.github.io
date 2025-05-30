# Introduction
此部落格是引用[jekyll-theme-next](https://github.com/Simpleyyt/jekyll-theme-next)，也是從[HackMD](https://hackmd.io/@SBK6401)搬過來的文章，HackMD大機率應該不會更新了

## Post 分類
* Books Notes
    讀書的心得或是學習筆記
* Data Structure
    看了交大資工系 彭文志老師在YT上的開放式課程所寫的筆記
* Job
    和工作有關的文章
* Knowledge
    學到一些廢廢的common knowledge，有些是直接問Chatgpt，並且把回答直接濃縮，都有在文章開頭註明
* LeetCode
    寫LeetCode的思考過程
* Problem Solutions
    大部分是IT遇到的問題，透過看別人的文章時解決的過程
* Security
    和資安相關的文章，有比賽、課程也有自己線下練習的文章
* Side Project
    有大學的專題也有高中的專題，或是其他心血來潮的小專案
* Survey Papers
    在碩班看到的論文
* Terminology
    簡單的解釋各種類似但對我來說容易搞混的名詞，有不同的類型
* Tools
    方便我自己查找的tools，大部分是CTF會用到的
* 原始文章
    目前主題的原始文章
* Tutorial
    和Problems Solutions不同的是這些文章都是一個完整使用某tools或framework之類的實際體驗教學

## Script
* `add_date_2_filename`
	如果是從HackMD搬過來的文章，目前(2025/04)還沒有把建立文章的時間寫在yaml front matter，只有Title和Tags，但是如果是Hugo/Hexo/Jekyll系列的framework，通常都要加入date才能符合themes的一些設定(有些是optional，但Jekyll是強制要把date放在filename, e.g., <date>-<title>.md)，我直接把從HackMD下載下來的檔案的修改時間當作檔案的建立時間，但非常不準確，就是一個下下策
	```python
	$ python add_date_2_filename.py
	```
* `add_category_2_file`
	我的寫法是把文章的file path直接當作category，例如`a/b/c/d.md`，則`categories: "a/b/c"`
	```python
	$ python add_category_2_file.py
	```
* `new_file`
	因為Jekyll不像Hugo可以直接new一個post instance，所以直接寫一個script，包含最基本的front matter和標題以及excerpt
	```python
	$ python new_file.py --file_path="a/b/c/d.md"
	```
	```template
	---
    layout: post
    title: "{name}"
    date: {date_full}
    categories: "{category_str}"
    tags: []
    draft: false
    toc: true
    comments: true
    ---
	
    # {name}
    <!--more-->
    
	```
* `add_new_line_before_header`
	由於HackMD的特性是，blockquote後面如果是接header(##,###,####...)，會主動render出header對應的layer，但在Jekyll中，他會承接blockquote的效果，所以我在每一個header前面判斷，如果header前一行不是`\n`，就直接加一行
	```
	# jjj
    lll
    ## aaa
    xxx
    ### bbb
    zzz
    #### ccc
    ```
    會變成
    ```
    # jjj
    lll
    
    ## aaa
    xxx
    
    ### bbb
    zzz
    
    #### ccc
    ```