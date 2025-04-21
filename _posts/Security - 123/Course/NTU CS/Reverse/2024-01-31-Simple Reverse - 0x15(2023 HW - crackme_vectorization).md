---
title: Simple Reverse - 0x15(2023 HW - crackme_vectorization)
tags: [eductf, CTF, Reverse]

category: "Security/Course/NTU CS/Reverse"
---

# Simple Reverse - 0x15(2023 HW - crackme_vectorization)
<!-- more -->

## Source Code
:::spoiler IDA Main Function
```cpp
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

  __isoc99_scanf("%d", &user_input_len);        // 長度為49
  user_input_len_cp = user_input_len;
  sqrt_length = sqrt((double)user_input_len);   // 開根號後是7
  sqrt_length_cp = (int)sqrt_length;
  if ( sqrt_length > (double)(int)sqrt_length )
    ++sqrt_length_cp;
  sqrt_len = _mm_shuffle_epi32(_mm_cvtsi32_si128(sqrt_length_cp), 224).m128i_u64[0];// 原本的shuffle num就是user input length的開根號結果
  space = (struc_1 *)malloc(0x10uLL);
  space->sqrt_len = sqrt_len;
  size = 4 * sqrt_length_cp * (__int64)sqrt_length_cp;// size是196
  shuffle_space = malloc(size);
  space->content_space = (__int64)shuffle_space;
  if ( user_input_len_cp > 0 )
  {
    shuffle_space_cp = shuffle_space;
    len = 0LL;
    do
    {
      __isoc99_scanf("%d", content);
      shuffle_space_cp[len++] = content[0];
    }
    while ( user_input_len > (int)len );        // 要輸入東西49次
  }
  if ( length == sqrt_length_cp
    && (space_1 = (struc_1 *)malloc(0x10uLL),
        space_1->sqrt_len = sqrt_len,
        shuffle_space_1 = malloc(size),
        src = cipher_flag,
        space_1->content_space = (__int64)shuffle_space_1,
        memcpy(shuffle_space_1, src, size),
        result = ugly_matrix_multiplication(
                   (int *)space_1,
                   (__int64)space),             // guess_cipher的大小是196
                                                // 他會把我們輸入的東西和他原本的東西一起送到guess_encrypt的這個function中
        !memcmp((const void *)result[1], verify_key, size)) )
  {
    puts("Correct!");
  }
  else
  {
    puts(":(");
  }
  return 0LL;
}
```
:::
:::spoiler IDA Ugly Function
```cpp
_QWORD *__fastcall guess_encrypt(int *space_1, __int64 space)
{
  // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

  _RAX = malloc(0x10uLL);
  _RDI = *space_1;
  guess_cipher = _RAX;
  length_0x4 = *(int *)(space + 4);
  __asm { vmovd   xmm5, edi }
  length_0x0 = *space_1;
  _RBX = 4 * length_0x4;
  __asm { vpinsrd xmm0, xmm5, r13d, 1 }
  length_0x4_cp = length_0x4;
  __asm { vmovq   qword ptr [rax], xmm0 }
  space_2 = malloc(4 * length_0x4 * _RDI);
  guess_cipher[1] = space_2;
  if ( length_0x0 > 0 )
  {
    length_0x4_cp2 = length_0x4;
    if ( (int)length_0x4 > 0 )
    {
      length_0x0_2 = space_1[1];
      length_0x0_cp = length_0x0;
      guess_cipher_1 = guess_cipher;
      length_16_0x4 = 16 * length_0x4;
      space_2_cp = space_2;
      length_0x0_2_minus_1 = length_0x0_2 - 1;
      space_1_cp = space_1;
      length_0x0_2_x_4 = 16LL * ((unsigned int)length_0x0_2 >> 2);
      v14 = 0;
      while ( 1 )
      {
        v15 = 0LL;
        v16 = length_0x0_2 * v14;
        v87 = 4LL * length_0x0_2 * v14;
        cmd = length_0x4_cp & 7;
        if ( (length_0x4_cp & 7) == 0 )
          goto LABEL_44;
        switch ( cmd )
        {
          case 1LL:
            goto LABEL_42;
          case 2LL:
            goto LABEL_40;
          case 3LL:
            goto LABEL_38;
          case 4LL:
            goto LABEL_36;
          case 5LL:
            goto LABEL_34;
        }
        if ( cmd != 6 )
        {
          if ( length_0x0_2 > 0 )
            goto LABEL_12;
          v15 = 1LL;
          *space_2_cp = 0;
        }
        if ( length_0x0_2 <= 0 )
          break;
LABEL_12:
        v92 = v14;
        v18 = v15;
        v19 = *((_QWORD *)space_1_cp + 1);
        v20 = *(_QWORD *)(space + 8);
        if ( length_0x0_2_minus_1 <= 2 )
          goto LABEL_26;
        while ( 1 )
        {
          _R15 = v20 + 4 * v15;
          __asm { vpxor   xmm0, xmm0, xmm0 }
          v23 = v19 + v87;
          v24 = length_0x0_2_x_4 + v19 + v87;
          v25 = ((unsigned __int8)((unsigned __int64)(length_0x0_2_x_4 - 16) >> 4) + 1) & 3;
          if ( (((unsigned __int8)((unsigned __int64)(length_0x0_2_x_4 - 16) >> 4) + 1) & 3) == 0 )
            goto LABEL_51;
          if ( v25 != 1 )
          {
            if ( v25 != 2 )
            {
              __asm
              {
                vmovd   xmm3, dword ptr [r15+rbx*2]
                vmovd   xmm4, dword ptr [r15]
              }
              v23 += 16LL;
              __asm
              {
                vpinsrd xmm2, xmm3, dword ptr [r15+r8], 1
                vpinsrd xmm1, xmm4, dword ptr [r15+rbx], 1
              }
              _R15 += length_16_0x4;
              __asm
              {
                vpunpcklqdq xmm6, xmm1, xmm2
                vpmulld xmm0, xmm6, xmmword ptr [rdx-10h]
              }
            }
            __asm
            {
              vmovd   xmm7, dword ptr [r15+rbx*2]
              vmovd   xmm9, dword ptr [r15]
            }
            v23 += 16LL;
            __asm
            {
              vpinsrd xmm8, xmm7, dword ptr [r15+r8], 1
              vpinsrd xmm10, xmm9, dword ptr [r15+rbx], 1
            }
            _R15 += length_16_0x4;
            __asm
            {
              vpunpcklqdq xmm11, xmm10, xmm8
              vpmulld xmm12, xmm11, xmmword ptr [rdx-10h]
              vpaddd  xmm0, xmm0, xmm12
            }
          }
          __asm
          {
            vmovd   xmm13, dword ptr [r15+rbx*2]
            vmovd   xmm15, dword ptr [r15]
          }
          v23 += 16LL;
          __asm
          {
            vpinsrd xmm14, xmm13, dword ptr [r15+r8], 1
            vpinsrd xmm5, xmm15, dword ptr [r15+rbx], 1
          }
          _R15 += length_16_0x4;
          __asm
          {
            vpunpcklqdq xmm3, xmm5, xmm14
            vpmulld xmm2, xmm3, xmmword ptr [rdx-10h]
            vpaddd  xmm0, xmm0, xmm2
          }
          if ( v24 != v23 )
          {
LABEL_51:
            do
            {
              __asm
              {
                vmovd   xmm4, dword ptr [r15+rbx*2]
                vmovd   xmm6, dword ptr [r15]
              }
              v23 += 64LL;
              __asm
              {
                vpinsrd xmm1, xmm4, dword ptr [r15+r8], 1
                vpinsrd xmm7, xmm6, dword ptr [r15+rbx], 1
              }
              _R15 = length_16_0x4 + _R15;
              __asm
              {
                vmovd   xmm11, dword ptr [r15+rbx*2]
                vmovd   xmm13, dword ptr [r15]
                vpinsrd xmm12, xmm11, dword ptr [r15+r8], 1
                vpinsrd xmm14, xmm13, dword ptr [r15+rbx], 1
              }
              _R15 = length_16_0x4 + _R15;
              __asm
              {
                vpunpcklqdq xmm8, xmm7, xmm1
                vmovd   xmm3, dword ptr [r15+rbx*2]
                vpmulld xmm9, xmm8, xmmword ptr [rdx-40h]
                vpinsrd xmm4, xmm3, dword ptr [r15+r8], 1
                vpaddd  xmm10, xmm0, xmm9
                vmovd   xmm2, dword ptr [r15]
                vpinsrd xmm1, xmm2, dword ptr [r15+rbx], 1
              }
              _R15 = length_16_0x4 + _R15;
              __asm
              {
                vpunpcklqdq xmm15, xmm14, xmm12
                vmovd   xmm9, dword ptr [r15+rbx*2]
                vmovd   xmm11, dword ptr [r15]
                vpmulld xmm5, xmm15, xmmword ptr [rdx-30h]
                vpinsrd xmm12, xmm11, dword ptr [r15+rbx], 1
                vpaddd  xmm0, xmm10, xmm5
                vpunpcklqdq xmm6, xmm1, xmm4
                vpmulld xmm7, xmm6, xmmword ptr [rdx-20h]
                vpinsrd xmm10, xmm9, dword ptr [r15+r8], 1
                vpaddd  xmm8, xmm0, xmm7
              }
              _R15 = length_16_0x4 + _R15;
              __asm
              {
                vpunpcklqdq xmm13, xmm12, xmm10
                vpmulld xmm14, xmm13, xmmword ptr [rdx-10h]
                vpaddd  xmm0, xmm8, xmm14
              }
            }
            while ( v24 != v23 );
          }
          __asm
          {
            vpsrldq xmm15, xmm0, 8
            vpaddd  xmm5, xmm0, xmm15
            vpsrldq xmm0, xmm5, 4
          }
          v75 = length_0x0_2 & 0xFFFFFFFC;
          __asm
          {
            vpaddd  xmm3, xmm5, xmm0
            vmovd   ecx, xmm3
          }
          if ( length_0x0_2 != (length_0x0_2 & 0xFFFFFFFC) )
            goto LABEL_21;
LABEL_24:
          space_2_cp[v15++] = _ECX;
          if ( length_0x4_cp == v15 )
            break;
          v18 = v15;
          if ( length_0x0_2_minus_1 <= 2 )
          {
LABEL_26:
            v75 = 0;
            _ECX = 0;
LABEL_21:
            v78 = v75 + 1;
            _ECX += *(_DWORD *)(v20 + 4LL * (int)(v75 * length_0x4_cp2 + v18))
                  * *(_DWORD *)(v19 + 4LL * (int)(v16 + v75));
            if ( (int)(v75 + 1) < length_0x0_2 )
            {
              v79 = length_0x4_cp2 + v75 * length_0x4_cp2;
              v80 = v75 + 2;
              _ECX += *(_DWORD *)(v20 + 4LL * (v79 + v18)) * *(_DWORD *)(v19 + 4LL * (int)(v16 + v78));
              if ( length_0x0_2 > v80 )
                _ECX += *(_DWORD *)(v19 + 4LL * (v16 + v80)) * *(_DWORD *)(v20 + 4LL * (v18 + length_0x4_cp2 + v79));
            }
            goto LABEL_24;
          }
        }
        v14 = v92;
LABEL_28:
        space_2_cp = (_DWORD *)((char *)space_2_cp + _RBX);
        if ( length_0x0_cp == ++v14 )
          return guess_cipher_1;
      }
      space_2_cp[v15++] = 0;
LABEL_34:
      if ( length_0x0_2 > 0 )
        goto LABEL_12;
      space_2_cp[v15++] = 0;
LABEL_36:
      if ( length_0x0_2 > 0 )
        goto LABEL_12;
      space_2_cp[v15++] = 0;
LABEL_38:
      if ( length_0x0_2 > 0 )
        goto LABEL_12;
      space_2_cp[v15++] = 0;
LABEL_40:
      if ( length_0x0_2 > 0 )
        goto LABEL_12;
      space_2_cp[v15++] = 0;
LABEL_42:
      if ( length_0x0_2 > 0 )
        goto LABEL_12;
      space_2_cp[v15++] = 0;
      if ( length_0x4_cp == v15 )
        goto LABEL_28;
LABEL_44:
      v82 = v15;
      while ( length_0x0_2 <= 0 )
      {
        space_2_cp[v82] = 0;
        v83 = v82 + 1;
        space_2_cp[v83] = 0;
        space_2_cp[v83 + 1] = 0;
        space_2_cp[v83 + 2] = 0;
        space_2_cp[v83 + 3] = 0;
        space_2_cp[v83 + 4] = 0;
        space_2_cp[v83 + 5] = 0;
        space_2_cp[v83 + 6] = 0;
        v82 = v83 + 7;
        if ( length_0x4_cp == v82 )
          goto LABEL_28;
      }
      v15 = v82;
      goto LABEL_12;
    }
  }
  return guess_cipher;
}
```
:::

## Recon
一陣基本操作處理完比較好看的狀態後，首先發現一開始先輸入字串的長度(應該是49)，然後我們要輸入一些東西(就是按照前面輸入，總共也是49次)，接著就會進到很醜沒辦法解析的function(我暫時不理他)，一開始我在猜應該是做encryption之類的事情，接著就比對mem，一樣就噴correct這樣，我認為超級醜的function應該不是這次出題的重點，因為要全部逆完真的很有難度，對於學習也沒必要，此時我開始用動態+通靈的方式猜他在幹嘛，依照題目的標題和後面對比字串長度必須要等於`7`這兩個東西判斷，他應該是在做矩陣之類的操作，而那個醜不拉基的function應該是類似乘法或是加法之類的功能，有了想法就可以實驗他的操作
如果輸入長度49
1. 內容都是零，毫不意外經過醜不拉基function後都會是零
    :::spoiler Result
    ```
    0x000055aa2b46b4b0│+0x0000: 0x0000000000000000   ← $rdi
    0x000055aa2b46b4b8│+0x0008: 0x0000000000000000
    0x000055aa2b46b4c0│+0x0010: 0x0000000000000000
    0x000055aa2b46b4c8│+0x0018: 0x0000000000000000
    0x000055aa2b46b4d0│+0x0020: 0x0000000000000000
    0x000055aa2b46b4d8│+0x0028: 0x0000000000000000
    0x000055aa2b46b4e0│+0x0030: 0x0000000000000000
    0x000055aa2b46b4e8│+0x0038: 0x0000000000000000
    0x000055aa2b46b4f0│+0x0040: 0x0000000000000000
    0x000055aa2b46b4f8│+0x0048: 0x0000000000000000
    0x000055aa2b46b500│+0x0050: 0x0000000000000000
    0x000055aa2b46b508│+0x0058: 0x0000000000000000
    0x000055aa2b46b510│+0x0060: 0x0000000000000000
    0x000055aa2b46b518│+0x0068: 0x0000000000000000
    0x000055aa2b46b520│+0x0070: 0x0000000000000000
    0x000055aa2b46b528│+0x0078: 0x0000000000000000
    0x000055aa2b46b530│+0x0080: 0x0000000000000000
    0x000055aa2b46b538│+0x0088: 0x0000000000000000
    0x000055aa2b46b540│+0x0090: 0x0000000000000000
    0x000055aa2b46b548│+0x0098: 0x0000000000000000
    0x000055aa2b46b550│+0x00a0: 0x0000000000000000
    0x000055aa2b46b558│+0x00a8: 0x0000000000000000
    0x000055aa2b46b560│+0x00b0: 0x0000000000000000
    0x000055aa2b46b568│+0x00b8: 0x0000000000000000
    0x000055aa2b46b570│+0x00c0: 0x0000000000000000
    ```
    :::
2. 內容都是一，經過醜不拉基function後都會每七個都是同一個數字
    :::spoiler Result
    ```
    0x000055d2f80754b0│+0x0000: 0x000003d4000003d4   ← $rdi
    0x000055d2f80754b8│+0x0008: 0x000003d4000003d4
    0x000055d2f80754c0│+0x0010: 0x000003d4000003d4
    0x000055d2f80754c8│+0x0018: 0x000002d8000003d4
    0x000055d2f80754d0│+0x0020: 0x000002d8000002d8
    0x000055d2f80754d8│+0x0028: 0x000002d8000002d8
    0x000055d2f80754e0│+0x0030: 0x000002d8000002d8
    0x000055d2f80754e8│+0x0038: 0x0000030f0000030f
    0x000055d2f80754f0│+0x0040: 0x0000030f0000030f
    0x000055d2f80754f8│+0x0048: 0x0000030f0000030f
    0x000055d2f8075500│+0x0050: 0x000003000000030f
    0x000055d2f8075508│+0x0058: 0x0000030000000300
    0x000055d2f8075510│+0x0060: 0x0000030000000300
    0x000055d2f8075518│+0x0068: 0x0000030000000300
    0x000055d2f8075520│+0x0070: 0x000003b0000003b0
    0x000055d2f8075528│+0x0078: 0x000003b0000003b0
    0x000055d2f8075530│+0x0080: 0x000003b0000003b0
    0x000055d2f8075538│+0x0088: 0x000003c6000003b0
    0x000055d2f8075540│+0x0090: 0x000003c6000003c6
    0x000055d2f8075548│+0x0098: 0x000003c6000003c6
    0x000055d2f8075550│+0x00a0: 0x000003c6000003c6
    0x000055d2f8075558│+0x00a8: 0x0000031e0000031e
    0x000055d2f8075560│+0x00b0: 0x0000031e0000031e
    0x000055d2f8075568│+0x00b8: 0x0000031e0000031e
    0x000055d2f8075570│+0x00c0: 0x000000000000031e
    ```
    :::
3. 內容都是二，和上面對比全部都會是兩倍
    :::spoiler Result
    ```
    0x0000563c09e664b0│+0x0000: 0x000007a8000007a8   ← $rdi
    0x0000563c09e664b8│+0x0008: 0x000007a8000007a8
    0x0000563c09e664c0│+0x0010: 0x000007a8000007a8
    0x0000563c09e664c8│+0x0018: 0x000005b0000007a8
    0x0000563c09e664d0│+0x0020: 0x000005b0000005b0
    0x0000563c09e664d8│+0x0028: 0x000005b0000005b0
    0x0000563c09e664e0│+0x0030: 0x000005b0000005b0
    0x0000563c09e664e8│+0x0038: 0x0000061e0000061e
    0x0000563c09e664f0│+0x0040: 0x0000061e0000061e
    0x0000563c09e664f8│+0x0048: 0x0000061e0000061e
    0x0000563c09e66500│+0x0050: 0x000006000000061e
    0x0000563c09e66508│+0x0058: 0x0000060000000600
    0x0000563c09e66510│+0x0060: 0x0000060000000600
    0x0000563c09e66518│+0x0068: 0x0000060000000600
    0x0000563c09e66520│+0x0070: 0x0000076000000760
    0x0000563c09e66528│+0x0078: 0x0000076000000760
    0x0000563c09e66530│+0x0080: 0x0000076000000760
    0x0000563c09e66538│+0x0088: 0x0000078c00000760
    0x0000563c09e66540│+0x0090: 0x0000078c0000078c
    0x0000563c09e66548│+0x0098: 0x0000078c0000078c
    0x0000563c09e66550│+0x00a0: 0x0000078c0000078c
    0x0000563c09e66558│+0x00a8: 0x0000063c0000063c
    0x0000563c09e66560│+0x00b0: 0x0000063c0000063c
    0x0000563c09e66568│+0x00b8: 0x0000063c0000063c
    0x0000563c09e66570│+0x00c0: 0x000000000000063c
    ```
    :::
4. 只有第一個element是1，其他都是零，由結果可知只有七個一數的第一個element會有值，且該值是已經從儲存在原本的執行檔中，比對之後發現一模一樣
    :::spoiler Result
    ```
    0x0000563dd53444b0│+0x0000: 0x000000000000003c ("<"?)    ← $rdi
    0x0000563dd53444b8│+0x0008: 0x0000000000000000
    0x0000563dd53444c0│+0x0010: 0x0000000000000000
    0x0000563dd53444c8│+0x0018: 0x0000007300000000
    0x0000563dd53444d0│+0x0020: 0x0000000000000000
    0x0000563dd53444d8│+0x0028: 0x0000000000000000
    0x0000563dd53444e0│+0x0030: 0x0000000000000000
    0x0000563dd53444e8│+0x0038: 0x000000000000007a ("z"?)
    0x0000563dd53444f0│+0x0040: 0x0000000000000000
    0x0000563dd53444f8│+0x0048: 0x0000000000000000
    0x0000563dd5344500│+0x0050: 0x0000004100000000
    0x0000563dd5344508│+0x0058: 0x0000000000000000
    0x0000563dd5344510│+0x0060: 0x0000000000000000
    0x0000563dd5344518│+0x0068: 0x0000000000000000
    0x0000563dd5344520│+0x0070: 0x0000000000000067 ("g"?)
    0x0000563dd5344528│+0x0078: 0x0000000000000000
    0x0000563dd5344530│+0x0080: 0x0000000000000000
    0x0000563dd5344538│+0x0088: 0x0000007900000000
    0x0000563dd5344540│+0x0090: 0x0000000000000000
    0x0000563dd5344548│+0x0098: 0x0000000000000000
    0x0000563dd5344550│+0x00a0: 0x0000000000000000
    0x0000563dd5344558│+0x00a8: 0x00000000000000fa
    0x0000563dd5344560│+0x00b0: 0x0000000000000000
    0x0000563dd5344568│+0x00b8: 0x0000000000000000
    0x0000563dd5344570│+0x00c0: 0x0000000000000000
    ```
    :::
    
由以上實驗可以大致確認醜不拉基function做的事情就是矩陣乘法，而我們知道他比較的乘法結果，也知道和我們輸入的矩陣相乘的乘數，換言之可以反推回我們應該輸入的東西為何

## Exploit
```python
from pwn import *
from sage.all import *

r = process('./simple-crackme_f5e33c76600e')

flag_len = 49
verify_matrix = Matrix([[0x00010ee0, 0x00010814, 0x00014d06, 0x00015a7c, 0x00012de1, 0x00014a5a, 0x0000f883], 
                       [0x0000df33, 0x0000a7a5, 0x0000e66b, 0x0000e0c8, 0x0000b727, 0x0000eb70, 0x00008d9e], 
                       [0x0000fe08, 0x0000d725, 0x00010163, 0x000101a0, 0x0000c427, 0x00010365, 0x0000afca], 
                       [0x0000db6f, 0x0000dbdf, 0x00010dc3, 0x0000fb36, 0x0000d5c3, 0x00011ae8, 0x0000ddc2], 
                       [0x00011589, 0x0000fbc8, 0x00014000, 0x00011f7f, 0x0001019d, 0x0001567c, 0x0000f435], 
                       [0x00012c8d, 0x0000ff0b, 0x00012caf, 0x00014592, 0x000112ff, 0x00015e64, 0x00010322], 
                       [0x000109f9, 0x0000f002, 0x000115ee, 0x0000fe74, 0x0000d58e, 0x00011306, 0x0000c506]])

ct = Matrix([[0x3C, 0xAD, 0xB9, 0xF5, 0x84, 0x25, 0x94], 
            [0x73, 0xC8, 0x4E, 0x01, 0xAF, 0x04, 0x9B], 
            [0x7A, 0xC8, 0x33, 0x6D, 0x0A, 0x7F, 0xA4], 
            [0x41, 0x8E, 0x12, 0xE1, 0x94, 0x73, 0x37], 
            [0x67, 0x82, 0x60, 0x7F, 0xE9, 0x91, 0x6E], 
            [0x79, 0xBA, 0xEE, 0x09, 0xC1, 0xD0, 0x0B], 
            [0xFA, 0xAD, 0x46, 0x64, 0x10, 0x59, 0x64]])

# flag = [102, 103, 112, 53, 70, 100, 72, 88, 47, 55, 122, 50, 69, 49, 66, 67, 74, 120, 118, 80, 68, 53, 99, 114, 102, 101, 100, 105, 57, 49, 89, 52, 68, 107, 71, 97, 83, 79, 68, 48, 113, 85, 79, 48, 86, 53, 48, 61, 0]

flag = (verify_matrix.transpose() / ct.transpose()).transpose().coefficients()
print(flag)
r.sendline(str(flag_len).encode())
for i in range(len(flag)):
    r.sendline(str(flag[i]).encode())
r.sendline(b'0')
assert r.recvline().strip().decode() == "Correct!"
r.close()

print("Password = " + "".join([chr(i) for i in flag]))
```
```bash
$ python exp.py
[+] Starting local process './simple-crackme_f5e33c76600e': pid 12091
[102, 103, 112, 53, 70, 100, 72, 88, 47, 55, 122, 50, 69, 49, 66, 67, 74, 120, 118, 80, 68, 53, 99, 114, 102, 101, 100, 105, 57, 49, 89, 52, 68, 107, 71, 97, 83, 79, 68, 48, 113, 85, 79, 48, 86, 53, 48, 61]
[*] Stopped process './simple-crackme_f5e33c76600e' (pid 12091)
Password = fgp5FdHX/7z2E1BCJxvPD5crfedi91Y4DkGaSOD0qUO0V50=
```
最後只要把解出來的東西丟回去revguard就可以拿到真正的flag了
![圖片.png](https://hackmd.io/_uploads/Sy6cmC1Xa.png)

Flag: `FLAG{yOu_kn0w_hOw_to_r3v3r53_4_m47riX!}`