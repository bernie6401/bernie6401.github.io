---
title: "Git Large File Error - Solution"
tags: [problem solution]

category: "Problem Solutions"
---

# Git Large File Error - Solution
## Scenario 1
如果是在加入後不慎注意，就直接commit並且push才發現的，要用以下解法
```bash!
...
$ git push    # Now it has large file problem
# Assume the path of large file is : PicoCTF/2023/Reverse/Reverse/ida-20230316-000006-17384.dmp
$ git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch PicoCTF/2023/Reverse/Reverse/ida-20230316-000006-17384.dmp'
$ git push #Then it works
```
<!-- more -->
:::info
如果在變更過程中出現`Cannot rewrite branches: You have unstaged changes.`，代表以一些檔案沒有被add以及commit，需要先把其他檔案都做完整的commit後才可以執行上述操作
:::

## Scenario 2
如果是加入後commit但在push之前就發現檔案太大並且自行刪除後再push，要用以下解法
```bash
$ git rm --cached . -r -f
$ git add .
$ git commit -m "update all files"
$ git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch {file path}'
$ git push
```

:::info
基本上不管是哪一種方法都會在git filter-branch...之後看到==Ref 'refs/heads/master' was rewritten==的字樣
:::

## Reference
[解决git不小心提交大文件导致无法提交问题 ](https://blog.51cto.com/frytea/4143701)
[git filter-branch remove folder failed](https://stackoverflow.com/questions/30316723/git-filter-branch-remove-folder-failed)
[[Git筆記] exceeds GitHub file size 解決](https://andy6804tw.github.io/2018/12/09/git-exceeds-size/)