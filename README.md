# Introduction
此部落格是引用[jekyll-theme-next](https://github.com/Simpleyyt/jekyll-theme-next)，也是從[HackMD](https://hackmd.io/@SBK6401)搬過來的文章，HackMD大機率應該不會更新了
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