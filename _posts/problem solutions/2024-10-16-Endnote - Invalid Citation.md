---
title: Endnote - Invalid Citation
tags: [problem solution]

category: "Problem Solutions"
---

# Endnote - Invalid Citation
目前遇到的怪問題，先紀錄起來，之後再解決
## Problem
使用Endnote寫論文，因不明原因導致關閉Word之後，出現某一些references不見了，而且經過一些測試，不見的論文都是同樣幾篇，
## 已嘗試的方法
1. 重新remove該reference後，再cite一次，但只要關閉word，重開後就還是回復原樣
2. 刪除endnote的data file，並且建立新的library，再從雲端拉資料下來，再重複方法1，還是無果
3. 複製一份新的paper template(原本的這一篇也是用這個template改的)，再重新把資料從舊的word，一段一段搬運過去，並且同步cite各個reference，但還是一樣，重新開啟Word後，在同樣的幾篇論文出現Invalid Citation
4. 在Endnote中去除有問題的幾篇論文，再重新下載Google Scholar的Endnote Files，然後再用一樣的方法cite，結果還是一樣
5. 如果用一篇完全空白的word，並且用Endnote cite那幾篇有問題的論文，會發現沒有出現任何問題

## 確定的事情
1. 雲端的資料應該沒有問題
2. 出現問題的應該是Word，但不確定是哪邊

目前可能的解決方式是直接開一個新的Word，然後一段一段搬運過去，就不要用Template改

## 更新
我大概知道原因了，基本上應該是Endnote無法處理"範圍"，也就是類似\[10-13\]這樣的關係，雖然不知道為什麼，但其實只要把範圍拆開獨立顯示->\[10\]\[11\]\[12\]\[13\]就沒問題了，不過之後還是要查一下為什麼會這樣