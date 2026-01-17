---
title: Simple Reverse - 0x29(2023 Lab - Unpackme)
tags: [eductf, CTF, Reverse]

category: "Security｜Course｜NTU CS｜Reverse"
date: 2024-01-31
---

# Simple Reverse - 0x29(2023 Lab - Unpackme)
<!-- more -->

## Source code
```cpp
...
LOAD:0000000000005AE8 mov     rdi, [rsp+18h+start]            ; start
LOAD:0000000000005AED push    5
LOAD:0000000000005AEF pop     rdx                             ; prot
LOAD:0000000000005AF0 push    0Ah
LOAD:0000000000005AF2 pop     rax
LOAD:0000000000005AF3 syscall                                 ; LINUX - sys_mprotect
LOAD:0000000000005AF5 jmp     r13
LOAD:0000000000005AF5
LOAD:0000000000005AF5 sub_5A7C endp
LOAD:0000000000005AF5
LOAD:0000000000005AF8 ; ---------------------------------------------------------------------------
LOAD:0000000000005AF8
LOAD:0000000000005AF8 loc_5AF8:                               ; CODE XREF: start+2↑p
LOAD:0000000000005AF8 pop     rbp
LOAD:0000000000005AF9 call    sub_5A7C
LOAD:0000000000005AF9
LOAD:0000000000005AF9 ; ---------------------------------------------------------------------------
LOAD:0000000000005AFE aProcSelfExe db '/proc/self/exe',0
LOAD:0000000000005B0D align 2
LOAD:0000000000005B0E dw 1
LOAD:0000000000005B10 dq 81B00000C1100h, 0FFFFFF0000000200h, 7549F983004AE8E5h, 0FD374C8D48575344h, 0CE39482FEB5B565Eh, 0FFFFFBFF5E563273h
LOAD:0000000000005B10 dq 778F3C0A72803CACh, 2C06740FFE7E8006h, 56161BE477013CE8h, 0FFBFFFFF75D028ADh, 0D801F829C80F5FDFh, 0C35BDFEBAC0312ABh
LOAD:0000000000005B10 dq 8948505741564158h, 0DBFFEDFEEC8148E6h, 590A6A5F54591000h, 5003E8348A548F3h, 0B6AB48FE8949F875h, 0F60C0AFC0CCBB374h
LOAD:0000000000005B10 dq 4DF5FF6EDFFE02FFh, 5E57370FFFBAFC29h, 50F58596AED7B8Ch, 0DFFF6FDB0579C085h, 8D49FD91580F6A0Eh, 0E741AAA00B0FF7Dh
...
```
:::spoiler Real File main Function
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  unsigned __int64 i; // [rsp+8h] [rbp-58h]
  char user_input[32]; // [rsp+10h] [rbp-50h] BYREF
  char v6[40]; // [rsp+30h] [rbp-30h]
  unsigned __int64 v7; // [rsp+58h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  printf("Enter input: ");
  scanf("%s", user_input);
  if ( sub_10C0(user_input, qword_4018, 10LL) )
  {
    printf_0("Incorrect!");
    result = 1;
  }
  else
  {
    for ( i = 0LL; i <= 0x26; ++i )
      v6[i] = user_input[i % 0xA] ^ *(qword_4010 + i);
    printf("%s");
    result = 0;
  }
  if ( v7 != __readfsqword(0x28u) )
    return sub_10A0();
  return result;
}
```
:::

## Recon
這一題一開始就知道是UPX加殼，但是直接試了upx幫忙decompress，卻遇到error，代表可能有一些問題(在Unix環境底下?)，所以我嘗試使用手動脫殼，去分析其中的內容

1. 首先可以先靜態看一下脫完殼之前是在哪邊跳轉，經過實測和判斷，應該是:
    ```cpp
    LOAD:0000000000005AF5 jmp     r13
    ```
    :::info
    如何在動態取得這一行的位置呢?手動算出rebase address
    1. 首先先用靜態分析看starti的時候的offset
    2. 開始動態執行程式
    3. 把目前指到的address拿去和靜態分析拿到的offset相減
    4. (optional)可以用vmmap確認一下
    5. 再把我們想要得知的那一行的offset加回來
    
    ---
    ![圖片.png](https://hackmd.io/_uploads/Hk8-l9XXa.png)
    一開始的offset是0x5888
    ```bash
    gef➤  starti
    gef➤  x/x 0x7ffff7ffd888-0x5888
    0x7ffff7ff8000: 0x7f
    gef➤  vmmap
    [ Legend:  Code | Heap | Stack ]
    Start              End                Offset             Perm Path
    0x00007ffff7ff2000 0x00007ffff7ff6000 0x0000000000000000 r-- [vvar]
    0x00007ffff7ff6000 0x00007ffff7ff8000 0x0000000000000000 r-x [vdso]
    0x00007ffff7ff8000 0x00007ffff7ff9000 0x0000000000000000 rw- /mnt/d/NTU/Second Year/Computer Security/Reverse/Lab3/Unpackme/unpackme
    0x00007ffff7ff9000 0x00007ffff7ffd000 0x0000000000000000 rw-
    0x00007ffff7ffd000 0x00007ffff7fff000 0x0000000000000000 r-x /mnt/d/NTU/Second Year/Computer Security/Reverse/Lab3/Unpackme/unpackme
    0x00007ffffffdd000 0x00007ffffffff000 0x0000000000000000 rw- [stack]
    gef➤  x/10i 0x7ffff7ff8000+0x5AF5
       0x7ffff7ffdaf5:      jmp    r13
       0x7ffff7ffdaf8:      pop    rbp
       0x7ffff7ffdaf9:      call   0x7ffff7ffda7c
       0x7ffff7ffdafe:      (bad)
       0x7ffff7ffdaff:      jo     0x7ffff7ffdb73
       0x7ffff7ffdb01:      outs   dx,DWORD PTR ds:[rsi]
       0x7ffff7ffdb02:      movsxd ebp,DWORD PTR [rdi]
       0x7ffff7ffdb04:      jae    0x7ffff7ffdb6b
       0x7ffff7ffdb06:      ins    BYTE PTR es:[rdi],dx
       0x7ffff7ffdb07:      data16 (bad)
    ```
    :::
2. 利用動態看r13的address會跳去哪邊$\to$0x00007ffff7ff1000
3. 接下來我找不太到分析的地方，所以就直接c(continue)到user input的地方停下來，再看vmmap
    :::spoiler vmmap
    ```bash
    [ Legend:  Code | Heap | Stack ]
    Start              End                Offset             Perm Path
    0x00007ffff7d84000 0x00007ffff7d87000 0x0000000000000000 rw-
    0x00007ffff7d87000 0x00007ffff7daf000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/libc.so.6
    0x00007ffff7daf000 0x00007ffff7f44000 0x0000000000028000 r-x /usr/lib/x86_64-linux-gnu/libc.so.6
    0x00007ffff7f44000 0x00007ffff7f9c000 0x00000000001bd000 r-- /usr/lib/x86_64-linux-gnu/libc.so.6
    0x00007ffff7f9c000 0x00007ffff7fa0000 0x0000000000214000 r-- /usr/lib/x86_64-linux-gnu/libc.so.6
    0x00007ffff7fa0000 0x00007ffff7fa2000 0x0000000000218000 rw- /usr/lib/x86_64-linux-gnu/libc.so.6
    0x00007ffff7fa2000 0x00007ffff7faf000 0x0000000000000000 rw-
    0x00007ffff7fb3000 0x00007ffff7fb5000 0x0000000000000000 rw-
    0x00007ffff7fb5000 0x00007ffff7fb7000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x00007ffff7fb7000 0x00007ffff7fe1000 0x0000000000002000 r-x /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x00007ffff7fe1000 0x00007ffff7fec000 0x000000000002c000 r-- /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x00007ffff7fec000 0x00007ffff7fed000 0x0000000000000000 ---
    0x00007ffff7fed000 0x00007ffff7fef000 0x0000000000037000 r-- /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x00007ffff7fef000 0x00007ffff7ff1000 0x0000000000039000 rw- /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x00007ffff7ff2000 0x00007ffff7ff6000 0x0000000000000000 r-- [vvar]
    0x00007ffff7ff6000 0x00007ffff7ff8000 0x0000000000000000 r-x [vdso]
    0x00007ffff7ff8000 0x00007ffff7ff9000 0x0000000000000000 r--
    0x00007ffff7ff9000 0x00007ffff7ffa000 0x0000000000000000 r-x
    0x00007ffff7ffa000 0x00007ffff7ffc000 0x0000000000000000 r--
    0x00007ffff7ffc000 0x00007ffff7ffd000 0x0000000000000000 rw-
    0x00007ffff7ffe000 0x00007ffff7fff000 0x0000000000000000 r-- /mnt/d/NTU/Second Year/Computer Security/Reverse/Lab3/Unpackme/unpackme
    0x00007ffff7fff000 0x00007ffff8020000 0x0000000000000000 rw- [heap]
    0x00007ffffffdd000 0x00007ffffffff000 0x0000000000000000 rw- [stack]
    ```
    :::
    可以看到`0x00007ffff7ff8000`開始會有ELF的字樣，代表應該是他脫殼完的結果，我的作法是直接把`0x00007ffff7ff8000`~`0x00007ffff7ffd000`全部dump下來進行分析
    ```bash
    gef➤  x/s 0x00007ffff7ff8000
    0x7ffff7ff8000: "\177ELF\002\001\001"
    gef➤  dump memory real_file 0x00007ffff7ff8000 0x00007ffff7ffd000
    ```
4. 開始分析real_file，先用靜態看一下(如source code所示)
    ![圖片.png](https://hackmd.io/_uploads/BylZUq7X6.png)
5. 找到我們要停的地方的offset$\to$`0x1213`
    ```bash
    gef➤  x/10i 0x00007ffff7ff8000+0x1213
       0x7ffff7ff9213:      mov    rcx,QWORD PTR [rip+0x2dfe]        # 0x7ffff7ffc018
       0x7ffff7ff921a:      lea    rax,[rbp-0x50]
       0x7ffff7ff921e:      mov    edx,0xa
       0x7ffff7ff9223:      mov    rsi,rcx
       0x7ffff7ff9226:      mov    rdi,rax
    => 0x7ffff7ff9229:      call   0x7ffff7ff90c0
       0x7ffff7ff922e:      test   eax,eax
       0x7ffff7ff9230:      je     0x7ffff7ff924b
       0x7ffff7ff9232:      lea    rax,[rip+0xe13]        # 0x7ffff7ffa04c
       0x7ffff7ff9239:      mov    rdi,rax
    ```
    可以看到解析出來的assembly和IDA的差不多，代表我們找對地方
6. 設定breakpoint後continue就可以在stack中看到key
    ```
    gef➤  b *(0x00007ffff7ff9000+0x229)
    Breakpoint 1 at 0x7ffff7ff9229
    gef➤  c
    Continuing.
    adjfl

    Breakpoint 1, 0x00007ffff7ff9229 in ?? ()
    
    ```
    ```────────────────────────────────────────────────────────────────────────────────────────── arguments (guessed) ────
    0x7ffff7ff90c0 (
       $rdi = 0x00007fffffffd6c0 → 0x0000006c666a6461 ("adjfl"?),
       $rsi = 0x00007ffff7ffa030 → "just_a_key",
       $rdx = 0x000000000000000a,
       $rcx = 0x00007ffff7ffa030 → "just_a_key"
    )
    ```

## Exploit
key: `just_a_key`
```bash
$ ./unpackme
Enter input: just_a_key
FLAG{just_4_simple_unpackme_challenge!}
```

Flag: `FLAG{just_4_simple_unpackme_challenge!}`