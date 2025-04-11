---
title: PicoCTF - Investigative Reversing 0
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/General"
---

# PicoCTF - Investigative Reversing 0
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [Investigative Reversing 0](https://play.picoctf.org/practice/challenge/70?category=4&page=3)

## Background
[fputc() - C語言庫函數](http://tw.gitbook.net/c_standard_library/c_function_fputc.html)
[C/C++ fread 用法與範例](https://shengyu7697.github.io/cpp-fread/)
[C中fread()函数的返回值](https://blog.51cto.com/u_6680689/3260951)
[C语言之1ULL/1UL/1L区别](https://blog.csdn.net/u010164190/article/details/124945191)

## Source code - IDA
:::spoiler source code
```cpp=
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+4h] [rbp-4Ch]
  int j; // [rsp+8h] [rbp-48h]
  FILE *stream; // [rsp+10h] [rbp-40h]
  FILE *v8; // [rsp+18h] [rbp-38h]
  char ptr[40]; // [rsp+20h] [rbp-30h] BYREF
  unsigned __int64 v10; // [rsp+48h] [rbp-8h]

  v10 = __readfsqword(40u);
  stream = fopen("flag.txt", "r");
  v8 = fopen("mystery.png", "a");
  if ( !stream )
    puts("No flag found, please make sure this is run on the server");
  if ( !v8 )
    puts("mystery.png is missing, please run this on the server");
  if ( (int)fread(ptr, 26uLL, 1uLL, stream) <= 0 )
    exit(0);
  puts("at insert");
  fputc(ptr[0], v8);
  fputc(ptr[1], v8);
  fputc(ptr[2], v8);
  fputc(ptr[3], v8);
  fputc(ptr[4], v8);
  fputc(ptr[5], v8);
  for ( i = 6; i <= 14; ++i )
    fputc((char)(ptr[i] + 5), v8);
  fputc((char)(ptr[15] - 3), v8);
  for ( j = 16; j <= 25; ++j )
    fputc(ptr[j], v8);
  fclose(v8);
  fclose(stream);
  return __readfsqword(40u) ^ v10;
}
```
:::

## Exploit
1. Analyze source code
First, it open `mystery.png` and `flag.txt` file and read 26 characters in `flag.txt`
Then it append first 6 characters to `mystery.png` and do some disalignment like rot13.

2. In addition...
Observing `mystery.png` by `HxD`
![](https://i.imgur.com/V7qMwSx.png)
Seems we got a flag-like answer.

3. Recover it
The first 6 character can copy paste.
`K€k5zsid6` $\to$ `F{f0und_1` by minusing 5 based on ascii table
`q` $\to$ `t` by adding 3 based on ascii table again
The rest strings still copy paste again
Then we got flag... $\to$
`picoCTF{f0und_1t_3d659f57}`