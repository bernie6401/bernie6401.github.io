---
title: NISRA - Hidden?
tags: [NISRA, CTF, Misc]

category: "Security/Practice/NISRA/Misc"
---

# NISRA - Hidden?

## Background
[advanced-potion-making:two::+1:](/uwox6r5hQ6St_8G-4mv1_g)

## Recon
這一題也是蠻巧妙的，用pngcheck可以看到檔案有問題
```bash!
$ pngcheck haha.png
haha.png  additional data after IEND chunk
ERROR: haha.png
```

## Exploit - Recover + Unzip
1. Recover PNG File
先找文件尾（00 00 00 00 49 45 4E 44 AE 42 60 82）
![](https://hackmd.io/_uploads/SySm_6DO3.png)
發現後續還有其他bytes，用[list signature](https://en.wikipedia.org/wiki/List_of_file_signatures)追查後面是甚麼，![](https://hackmd.io/_uploads/Hy-5OpPOh.png)
發現應該是個zip file，所以獨立出來後解壓縮

2. Unzip
解壓縮後有一些文件，從裡面撈了一下flag就在./word/document.xml中
Flag: `NISRA{Oop5!_yoU_fOuNd_1t}`

![](https://hackmd.io/_uploads/BkLoDTwO3.png)
