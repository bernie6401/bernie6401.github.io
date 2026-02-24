---
title: NISRA 2023 Enlightened - Jack的flag
tags: [NISRA, CTF, Misc]

category: "Security Practice｜NISRA｜Misc"
date: 2024-01-31
---

# NISRA 2023 Enlightened - Jack的flag
<!-- more -->

## Background
Microsoft Word Forensics

## Recon
這是第一次寫到有關word的隱寫，蠻特別的就紀錄一下，但看得出來應該是考古古古古古古題了ㄅ

## Exploit
有兩種方法
1. 強制解壓縮
直接把副檔名改成.zip，然後用解壓縮軟體解壓縮，接著就可以在`Final-Jack\word\document.xml`中可以找到flag
2. 把隱藏設定打開
直接在word中的`檔案/選項/顯示/隱藏文字`的方塊打勾，就可以直接在下面看到flag了

Flag: `NISRA{Word'$_h1Dden_7eXT_reVEaLed}`