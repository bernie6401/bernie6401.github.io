---
title: PicoCTF - seed-sPRiNG
tags: [PicoCTF, CTF, PWN]

category: "Security Practice｜PicoCTF｜PWN"
date: 2024-01-31
---

# PicoCTF - seed-sPRiNG
<!-- more -->

## Source code
:::spoiler IDA Main Function
```cpp=
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int guess_height; // [esp+0h] [ebp-18h] BYREF
  int ans; // [esp+4h] [ebp-14h]
  unsigned int seed; // [esp+8h] [ebp-10h]
  int i; // [esp+Ch] [ebp-Ch]
  int *p_argc; // [esp+10h] [ebp-8h]

  p_argc = &argc;
  puts(&unk_A50);
  puts(&unk_A50);
  puts("                                                                             ");
  puts("                          #                mmmmm  mmmmm    \"    mm   m   mmm ");
  puts("  mmm    mmm    mmm    mmm#          mmm   #   \"# #   \"# mmm    #\"m  # m\"   \"");
  puts(" #   \"  #\"  #  #\"  #  #\" \"#         #   \"  #mmm#\" #mmmm\"   #    # #m # #   mm");
  puts("  \"\"\"m  #\"\"\"\"  #\"\"\"\"  #   #          \"\"\"m  #      #   \"m   #    #  # # #    #");
  puts(" \"mmm\"  \"#mm\"  \"#mm\"  \"#m##         \"mmm\"  #      #    \" mm#mm  #   ##  \"mmm\"");
  puts("                                                                             ");
  puts(&unk_A50);
  puts(&unk_A50);
  puts("Welcome! The game is easy: you jump on a sPRiNG.");
  puts("How high will you fly?");
  puts(&unk_A50);
  fflush(stdout);
  seed = time(0);
  srand(seed);
  for ( i = 1; i <= 30; ++i )
  {
    printf("LEVEL (%d/30)\n", i);
    puts(&unk_A50);
    LOBYTE(ans) = rand() & 0xF;
    ans = ans;
    printf("Guess the height: ");
    fflush(stdout);
    __isoc99_scanf("%d", &guess_height);
    fflush(stdin);
    if ( ans != guess_height )
    {
      puts("WRONG! Sorry, better luck next time!");
      fflush(stdout);
      exit(-1);
    }
  }
  puts("Congratulation! You've won! Here is your flag:\n");
  fflush(stdout);
  get_flag();
  fflush(stdout);
  return 0;
}
```
:::

## Recon
看了[^seed-sPRiNG]，才發現意外的簡單，就只是implement IDA分析的psuedo code，讓server和exploit的seed達成一致，原本看了老半天都沒發現明顯的洞，蠻有趣的，喜歡

## Exploit
```cpp=
#include <stdio.h> 
#include <time.h>
#include <stdlib.h> 
  
int main () 
{ 
    int i;
      
    srand(time(0)); 
    
    for (i = 0; i < 30; i++)
    {
        printf("%d\n", rand() & 0xf); 
    }
      
    return 0; 
} 
```
```bash
$ gcc exp.c -o exp
$ chmod 777 exp
$ ./exp | nc jupiter.challenges.picoctf.org 34558
```

Flag: `picoCTF{pseudo_random_number_generator_not_so_random_81b0dd7e}`

## Reference
[^seed-sPRiNG]:[seed-sPRiNG](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/seed-sPRiNG.md)