---
title: PicoCTF - babygame01
tags: [PicoCTF, CTF, PWN]

category: "Security/Practice/PicoCTF/PWN"
---

# PicoCTF - babygame01
<!-- more -->

## Background
Bof

## Description & Hint
> Get the flag and reach the exit. Welcome to BabyGame! Navigate around the map and see what you can find! The game is available to download here. There is no source available, so you'll have to figure your way around the map. You can connect with it using nc saturn.picoctf.net 50227.
> Hint 1: Use 'w','a','s','d' to move around.
> Hint 2: There may be secret commands to make your life easy.

## Source Code
:::spoiler IDA Main Function
```cpp=
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char input; // [esp+1h] [ebp-AA5h]
  int position[2]; // [esp+2h] [ebp-AA4h] BYREF
  char win_var; // [esp+Ah] [ebp-A9Ch]
  char map[2700]; // [esp+Eh] [ebp-A98h] BYREF
  unsigned int v8; // [esp+A9Ah] [ebp-Ch]
  int *p_argc; // [esp+A9Eh] [ebp-8h]

  p_argc = &argc;
  v8 = __readgsdword(0x14u);
  init_player(position);
  init_map(map, position);
  print_map(map, position);
  signal(2, sigint_handler);
  do
  {
    do
    {
      input = getchar();
      move_player(position, input, map);
      print_map(map, position);
    }
    while ( position[0] != 29 );
  }
  while ( position[1] != 89 );
  puts("You win!");
  if ( win_var )
  {
    puts("flage");
    win();
    fflush(stdout);
  }
  return 0;
}
```
:::

## Recon
這一題蠻有趣的，一樣是觸發類似Bof的概念，可以先用靜態的方式看，如果要用動態的方式看得話，需要讓glibc可以解析x32的檔案，另外glibc的版本也需要2.34，所以可以從[^gdb_problem][^x32_glibc_problem]這兩個ref解決gdb版本的問題

## Exploit
1. Hint當中有提到金手指的操作，觀察source code當中的move_player function中可以按p可以直接跑到終點，這樣就可以不用這麼麻煩

2. 可以看到main function中要使`win_var`達到非零才能夠進入win function，印出flag，所以看了別人的WP[^babygame01_WP]，可以讓player的位置覆蓋掉原本win_var的value，可以看一下在進入第一個getchar()之前stack的狀態
    ![](https://hackmd.io/_uploads/SkeT2IAq3.png)

3. 往左邊走之後，user input就會放在\$esp+3的地方，而\$esp+4放y軸的座標，\$esp+8放x軸的座標，所以可想而知，win_var應該是放在\$esp+12的地方
    ![](https://hackmd.io/_uploads/BkluaLCq2.png)

4. 在座標零零的地方又往左邊走之後x座標會變成0xffffffff，而雖然\$esp+12還是0，但是可以看到$esp+15變成0x40也就是(`@`)這個字元的ascii，所以我們可以在往左邊走點
    ![](https://hackmd.io/_uploads/H1GYCL0qh.png)
5. 現在win_var已經變成0x40了，所以player就有64個flag，此時就可以直接按p到達終點，拿到flag
    ![](https://hackmd.io/_uploads/BkqVfwR9n.png)
    ![](https://hackmd.io/_uploads/ryxwGP0ch.png)
    ![](https://hackmd.io/_uploads/Hy0qMD0q3.png)



Flag: `picoCTF{gamer_m0d3_enabled_054c1d5a}`

## Reference
[^babygame01_WP]:[picoCTF 2023 babygame01](https://youtu.be/I9BL3fZOj1M)
[^gdb_problem]:[version `GLIBC_2.34‘ not found简单有效解决方法](https://blog.csdn.net/huazhang_001/article/details/128828999)
[^x32_glibc_problem]:[解決gdb運行文件報錯During startup program exited with code 127.](https://www.zendei.com/article/55341.html)