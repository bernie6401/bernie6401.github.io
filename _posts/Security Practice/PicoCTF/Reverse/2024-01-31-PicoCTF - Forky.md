---
title: PicoCTF - Forky
tags: [PicoCTF, CTF, Reverse]

category: "Security Practice｜PicoCTF｜Reverse"
date: 2024-01-31
---

# PicoCTF - Forky
<!-- more -->

## Background
[ fork用法與範例 ](https://burweisnote.blogspot.com/2017/09/fork.html)

## Source code
Main Function From IDA
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  _DWORD *v4; // [esp+8h] [ebp-Ch]

  v4 = mmap(0, 4u, 3, 33, -1, 0);
  *v4 = 1000000000;
  fork();
  fork();
  fork();
  fork();
  *v4 += 1234567890;
  doNothing(*v4);
  return 0;
}
```

## Recon
這一題很有趣，有了background之後其實對這一題的想法差不多就和[^Forky-wp]差不多，也就是parent process fork出child process後會繼續往下fork出grandchild process，直到parent process執行完成
>  ```
>  +                                                                     
>  |                                                                     
>  +-----------------------------------+                                 
>  |                                   |                                 
>  +-----------------+                 +-----------------+               
>  |                 |                 |                 |               
>  +--------+        +--------+        +--------+        +--------+      
>  |        |        |        |        |        |        |        |      
>  +---+    +---+    +---+    +---+    +---+    +---+    +---+    +---+  
>  |   |    |   |    |   |    |   |    |   |    |   |    |   |    |   |  
>  O   O    O   O    O   O    O   O    O   O    O   O    O   O    O   O  
>  ```
而且他們所操作的外部記憶體對象都會是一樣的，代表\*v4最終會被加16次，只是我沒有考慮到負號的問題，因為該題是32bits，代表加到一定程度會overflow，所以都沒解出來

## Exploit
```bash
>>> base = np.array(1000000000).astype(np.int32)
>>> step = np.array(1234567890).astype(np.int32)
>>> str(np.array(20753086240).astype(np.int32))
'-721750240'
```

Flag: `picoCTF{-721750240}`

## Reference
[^Forky-wp]:[Forky - WP](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/Forky.md)