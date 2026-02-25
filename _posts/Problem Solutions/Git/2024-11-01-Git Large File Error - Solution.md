---
title: "Git Large File Error - Solution"
tags: [problem solution]

category: "Problem Solutions｜Git"
date: 2024-11-01
---

<!-- more -->
# Git Large File Error - Solution
## Scenario 1
如果在commit之前就已經知道有large file，並且一定要上傳到github，建議用Github提供的LFS(Large File Storage)，這個方法的原理是Github提供一個類似Google Drive的雲端儲存空間，免費用戶的空間是每月1 GB，大檔案本體會放在這個LFS中，而repo中的儲存的是一個pointer
```bash
# 安裝 Git LFS（只要做一次）
$ git lfs install

# 追蹤大檔案類型，例如 mp4 和 pdf
$ git lfs track "*.mp4"
$ git lfs track "*.pdf"

# 確認 .gitattributes 已經更新
$ git add .gitattributes

# 重新 add 那些大檔案
$ git add "./path/to/mp4_file"
$ git add "./path/to/pdf_files"

$ git commit -m "Add large files with Git LFS"
$ git push origin master
```

## Scenario 2
如果是在加入後不慎注意，就直接commit並且push才發現的，要用以下則一解法
1. 用比較新的filter-repo把大檔案移除，包含commit的history
    ```bash
    $ pip install git-filter-repo # 第一次使用要先安裝
    $ git filter-repo --path "./path/to/large_file" --invert-paths --force
    $ git push
    ```

2. (obsolete)以下部分是舊版的filter-branch，缺點是慢也容易出錯
    ```bash!
    ...
    $ git push    # Now it has large file problem
    # Assume the path of large file is : PicoCTF/2023/Reverse/Reverse/ida-20230316-000006-17384.dmp
    $ git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch PicoCTF/2023/Reverse/Reverse/ida-20230316-000006-17384.dmp'
    $ git push #Then it works
    ```
    如果在變更過程中出現`Cannot rewrite branches: You have unstaged changes.`，代表以一些檔案沒有被add以及commit，需要先把其他檔案都做完整的commit後才可以執行上述操作

## Scenario 3
如果是加入後commit但在push之前就發現檔案太大並且自行刪除後再push，要用以下解法
```bash
$ git rm --cached . -r -f
$ git add .
$ git commit -m "update all files"
$ git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch {file path}'
$ git push
```

:::info
基本上第二種和第三種方法都會在git filter-branch...之後看到`==Ref 'refs/heads/master' was rewritten==`的字樣
:::

## Reference
* [解决git不小心提交大文件导致无法提交问题 ](https://blog.51cto.com/frytea/4143701)
* [git filter-branch remove folder failed](https://stackoverflow.com/questions/30316723/git-filter-branch-remove-folder-failed)
* [[Git筆記] exceeds GitHub file size 解決](https://andy6804tw.github.io/2018/12/09/git-exceeds-size/)