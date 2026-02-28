---
title: PicoCTF - babygame02
tags: [PicoCTF, CTF, PWN]

category: "Security Practice｜PicoCTF｜PWN"
date: 2024-01-31
---

# PicoCTF - babygame02
<!-- more -->

## Source
:::spoiler IDA Main Function
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int position[2]; // [esp+0h] [ebp-AA0h] BYREF
  char map[2700]; // [esp+Bh] [ebp-A95h] BYREF
  char input; // [esp+A97h] [ebp-9h]
  int *p_argc; // [esp+A98h] [ebp-8h]

  p_argc = &argc;
  init_player(position);
  init_map(map, position);
  print_map(map);
  signal(2, sigint_handler);
  do
  {
    do
    {
      input = getchar();
      move_player(position, input, map);
      print_map(map);
    }
    while ( position[0] != 29 );                // y座標
  }
  while ( position[1] != 89 );                  // x座標
  puts("You win!");
  return 0;
}
```
:::
:::spoiler IDA Win Function
```cpp
int win()
{
  char s[60]; // [esp+0h] [ebp-48h] BYREF
  FILE *stream; // [esp+3Ch] [ebp-Ch]

  stream = fopen("flag.txt", "r");
  if ( !stream )
  {
    puts("flag.txt not found in current directory");
    exit(0);
  }
  fgets(s, 60, stream);
  return printf(s);
}
```
:::

:::spoiler IDA Win Function (Assembly)
```assembly
.text:0804975D ; int win()
.text:0804975D public win
.text:0804975D win proc near
.text:0804975D
.text:0804975D s= byte ptr -48h
.text:0804975D stream= dword ptr -0Ch
.text:0804975D var_4= dword ptr -4
.text:0804975D
.text:0804975D ; __unwind {
.text:0804975D push    ebp
.text:0804975E mov     ebp, esp
.text:08049760 push    ebx
.text:08049761 sub     esp, 44h
.text:08049764 call    __x86_get_pc_thunk_bx
.text:08049764
.text:08049769 add     ebx, (offset _GLOBAL_OFFSET_TABLE_ - $)
.text:0804976F nop
.text:08049770 nop
.text:08049771 nop
.text:08049772 nop
.text:08049773 nop
.text:08049774 nop
.text:08049775 nop
.text:08049776 nop
.text:08049777 nop
.text:08049778 nop
.text:08049779 sub     esp, 8
.text:0804977C lea     eax, (aR - 804C000h)[ebx]       ; "r"
.text:08049782 push    eax                             ; modes
.text:08049783 lea     eax, (aFlagTxt - 804C000h)[ebx] ; "flag.txt"
.text:08049789 push    eax                             ; filename
.text:0804978A call    _fopen
.text:0804978A
.text:0804978F add     esp, 10h
.text:08049792 mov     [ebp+stream], eax
.text:08049795 cmp     [ebp+stream], 0
.text:08049799 jnz     short loc_80497B7
.text:08049799
.text:0804979B sub     esp, 0Ch
.text:0804979E lea     eax, (aFlagTxtNotFoun - 804C000h)[ebx] ; "flag.txt not found in current directory"
.text:080497A4 push    eax                             ; s
.text:080497A5 call    _puts
.text:080497A5
.text:080497AA add     esp, 10h
.text:080497AD sub     esp, 0Ch
.text:080497B0 push    0                               ; status
.text:080497B2 call    _exit
```
:::

## Recon
這一題超難，主要是看了ref[^babygame02_martin_wp][^babygame02_ryan_wp]也不太知道怎麼做的，跟了gdb也分析不出個所以然，大概是和[前一題](https://hackmd.io/@SBK6401/rytbWvp5h)概念很像，從IDA分析的main function可以知道這次我們要想辦法跳到一個叫做win function的地方，但是這個function從來沒有被呼叫過，也沒有明顯的bof，所以要先用一些奇淫技巧改變return address，也就是到零零座標之後要先往上走(但是stack的變化我看不懂，總之y軸的數值變成0xfffffff，但不像上一題一樣會表現出來)，總之再往左邊走39次，並改變原本玩家的表示字元(0x40)成win()對應的最後一個byte，例如0x50, 0x5e, 0x60, 0x61, 0x64, 0x69, 0x6f, 0x70 - 0x78...，此時就會看到stack的return value就會是0x80497xx，他就會跳到win function吐出flag

## Exploit
Payload:
```bash
aaaa
wwwww
l]
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
s
```

## Reference
[^babygame02_martin_wp]:[ picoCTF babygame02 - Martin Carlisle](https://youtu.be/y2E9fGfV6sI)
[^babygame02_ryan_wp]:[babygame02 picoCTF writeup](https://blog.ry4n.org/babygame02-picoctf-writeup-6bf57b54f7b3)