---
layout: post
title: "HackTheBox - Debugme"
date: 2026-03-20
category: "Security Practice｜HackTheBox｜Reverse"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - Debugme
<!-- more -->

* Challenge Scenario
    > A develper is experiementing with different ways to protect their software. They have sent in a windows binary that is suposed to super secureand really hard to debug. Debug and see if you can find the flag.

## Recon
這一題沒有很難，但我完全猜錯作者出題的方向所以想了很久，有時候猜對方向比實力更重要。首先靜態的部分看了很久也沒啥想法，這時候有幾個方向可以猜
1. 在main之前的Entry Point搞不好有其他操作
2. 靜態看到的東西不一定runtime也一樣
3. 有沒有什麼是靜態反編譯不出來的地方
4. Anti-debug的判斷

基於以上的方向眾多，我就先用動態看一下並且直接執行在VM中看看實際跑起來會有什麼變化
```bash
$ debugme.exe
I heard you like bugs so I put bugs in your debugger so you can have bugs while you debug!!!
Seriously though try and find the flag, you will find it in your debugger!!!
```
程式print出了什麼東西看起來應該和malware無關，所以動態跟的時候就可以先想辦法bp在print之前，看他有什麼樣的操作。可以善用靜態的\[Ctrl+E\]的功能找尋Entry Point

一開始會斷在`0x4010F9` → `jmp _mainCRTStartup_0(0x408904)`

到這邊可以在靜態中看到反編譯的操作
```c
char mainCRTStartup_0()
{
  int v0; // eax
  unsigned __int64 v1; // rax
  int v2; // ebx
  unsigned __int64 v3; // rax
  int (__cdecl *v4)(int, const char **, const char **); // eax

  LOBYTE(v0) = NtCurrentPeb()->BeingDebugged;
  if ( !(_BYTE)v0 )
  {
    LOBYTE(v0) = NtCurrentPeb()->NtGlobalFlag;
    if ( !(_BYTE)v0 )
    {
      v1 = __rdtsc();
      v2 = v1;
      v3 = __rdtsc();
      v0 = v3 - v2;
      if ( v0 <= 1000 )
      {
        v4 = main;
        do
        {
          *(_BYTE *)v4 ^= 0x5Cu;
          v4 = (int (__cdecl *)(int, const char **, const char **))((char *)v4 + 1);
        }
        while ( (int)v4 <= (int)sub_401791 );
        mingw_app_type = 0;
        __security_init_cookie();
        LOBYTE(v0) = __tmainCRTStartup();
      }
    }
  }
  return v0;
}
```
如果實際動態跟，會發現在下面的地方不斷在xor某一段program的decode，那就是`0x401620~0x401791`共370 Bytes，這是很常見的落地方是
```
0040896E | B8 20164000              | mov eax,debugme.401620   |
00408973 | 8030 5C                  | xor byte ptr ds:[eax],5C |
00408976 | 40                       | inc eax                  |
00408977 | 3D 91174000              | cmp eax,debugme.401791   |
0040897C | 7E F5                    | jle debugme.408973       |
```
decrypt完之後就會發現靜態的地方已經把這一段看成main function，但完全反編譯不出來
<img src="/assets/posts/HackTheBox/Debugme -1.png" width=300>
之後的分析有兩種方式，那就是把decrypt完的東西，把落地的東西dump下來再丟到靜態看，不然就是直接繼續動態跟，一開始我選擇直接patch然後開靜態跟，但如果仔細看動態的寫法，他是在 `0x4013E5` 的地方直接call `0x401620`，然後跳過去，所以沒有接calling convention，也就是還要手動修過，太麻煩了

### 繼續跟0x401620
在下面標住的地方要特別注意，他應該是一段anti-debug，所以可以手動更改eax的值，反正只要小於0x3E8(1000)就好
```
00401674 | 3D E8030000   | cmp eax,3E8               |
00401679 | 7F 05         | jg debugme.401680         |
0040167B | E9 14000000   | jmp debugme.401694        |
00401680 | 68 00904000   | push debugme.409000       | 409000:"Looks like your doing something naughty. Stop it!!!\n"
00401685 | E8 626F0000   | call <JMP.&printf>        |
0040168A | 81C4 04000000 | add esp,4                 |
00401690 | 89EC          | mov esp,ebp               |
00401692 | 5D            | pop ebp                   |
00401693 | C3            | ret                       |
00401694 | 68 35904000   | push debugme.409035       | 409035:"I heard you like bugs so I put bugs in your debugger so you can have bugs while you debug!!!\n"
00401699 | E8 4E6F0000   | call <JMP.&printf>        |
0040169E | 81C4 04000000 | add esp,4                 |
004016A4 | 68 93904000   | push debugme.409093       | 409093:"Seriously though try and find the flag, you will find it in your debugger!!!\n"
004016A9 | E8 3E6F0000   | call <JMP.&printf>        |
004016AE | 81C4 04000000 | add esp,4                 |
```
另外，看了[^1]的說明才發現其實前面也有一系列的anti-debug，只是我都習慣把x64dbg的scylla hide的各種anti-anti-debugger feature打開，所以就順順過了

接著看後續會經歷一些eax的操作後，push到stack，接著會看到也有一段loop
```
00401788 | AC                       | lodsb                     |
00401789 | 31D8                     | xor eax,ebx               |
0040178B | AA                       | stosb                     |
0040178C | E2 FA                    | loop debugme.401788       |
```
不需要去看他push了什麼，只要知道這也是一段decrypt的過程，而他在decrypt的就是stack上剛剛push上去的那些data，我們只要在data windows上去看就好了
```
0061FE64      00 00 00 00 54 72 30 6C 6C 69 6E 67 5F 41 6E 74  ....Tr0lling_Ant  
0061FE74      31 5F 44 33 62 75 47 47 65 52 5F 74 72 69 63 6B  1_D3buGGeR_trick  
0061FE84      7A 5F 52 5F 66 75 6E 21 EA 13 40 00 01 00 00 00  z_R_fun!ê.@.....  
```
Flag: `HTB{Tr0lling_Ant1_D3buGGeR_trickz_R_fun!}`

## Reference
[^1]:[Debugme - HTB reversing challenge](https://fexsec.net/hackthebox/debugme/)