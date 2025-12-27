---
title: PicoCTF - not crypto
tags: [PicoCTF, CTF, Reverse]

category: "Security｜Practice｜PicoCTF｜Reverse"
---

# PicoCTF - not crypto
<!-- more -->

## Source code
:::spoiler IDA Pseudo Source COde
```clike!
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  __int128 *v4; // rax
  unsigned __int8 v5; // di
  unsigned __int8 v6; // si
  unsigned __int8 v7; // cl
  unsigned __int8 v8; // dl
  unsigned int v9; // r8d
  unsigned __int8 v10; // r11
  int v16; // eax
  __int64 v17; // rdx
  unsigned int v18; // r12d
  char *v20; // r15
  unsigned __int8 v25; // r8
  int v30; // esi
  unsigned __int8 v32; // r12
  unsigned __int8 v36; // r14
  unsigned __int8 v38; // dl
  unsigned __int8 v40; // cl
  char v42; // r12
  char v43; // r14
  char v44; // al
  __int64 v45; // r13
  unsigned __int8 v46; // r10
  unsigned __int8 v47; // bp
  unsigned __int8 v48; // bl
  unsigned __int8 v49; // r8
  unsigned __int8 v50; // r11
  char v51; // dl
  char v54; // r10
  __int64 v63; // rdx
  char v72; // al
  unsigned __int8 v84; // [rsp+Ah] [rbp-1FEh]
  unsigned __int8 v85; // [rsp+Bh] [rbp-1FDh]
  int v86; // [rsp+Ch] [rbp-1FCh]
  int v87; // [rsp+10h] [rbp-1F8h]
  unsigned __int8 v88; // [rsp+14h] [rbp-1F4h]
  unsigned __int8 v89; // [rsp+15h] [rbp-1F3h]
  unsigned __int8 v90; // [rsp+16h] [rbp-1F2h]
  unsigned __int8 v91; // [rsp+17h] [rbp-1F1h]
  unsigned __int8 v92; // [rsp+18h] [rbp-1F0h]
  unsigned __int8 v93; // [rsp+19h] [rbp-1EFh]
  unsigned __int8 v94; // [rsp+1Ah] [rbp-1EEh]
  unsigned __int8 v95; // [rsp+1Bh] [rbp-1EDh]
  unsigned __int8 v96; // [rsp+1Ch] [rbp-1ECh]
  char v97; // [rsp+1Dh] [rbp-1EBh]
  char *v98; // [rsp+20h] [rbp-1E8h]
  unsigned __int8 v99; // [rsp+2Ah] [rbp-1DEh]
  char v100; // [rsp+50h] [rbp-1B8h]
  char v101; // [rsp+52h] [rbp-1B6h]
  char v102; // [rsp+54h] [rbp-1B4h]
  char v103; // [rsp+56h] [rbp-1B2h]
  char v104; // [rsp+58h] [rbp-1B0h]
  char v105; // [rsp+5Ah] [rbp-1AEh]
  char v106; // [rsp+5Ch] [rbp-1ACh]
  char v107; // [rsp+5Eh] [rbp-1AAh]
  __int128 v108; // [rsp+60h] [rbp-1A8h]
  char ptr[64]; // [rsp+70h] [rbp-198h] BYREF
  __int128 v110; // [rsp+B0h] [rbp-158h] BYREF
  char v111; // [rsp+C0h] [rbp-148h] BYREF
  char v112[15]; // [rsp+150h] [rbp-B8h] BYREF
  __int128 v113; // [rsp+160h] [rbp-A8h]
  __int128 v115[4]; // [rsp+180h] [rbp-88h] BYREF
  char v116; // [rsp+1C0h] [rbp-48h] BYREF
  unsigned __int64 v117; // [rsp+1C8h] [rbp-40h]

  v117 = __readfsqword(0x28u);
  puts("I heard you wanted to bargain for a flag... whatcha got?");
  __asm { vmovdqa xmm0, cs:xmmword_21A0 }
  v4 = &v110;
  v5 = -104;
  v6 = 50;
  v7 = 108;
  v8 = 28;
  __asm { vmovdqa [rsp+208h+var_158], xmm0 }
  v9 = 4;
  do
  {
    if ( (v9 & 3) == 0 )
    {
      v10 = byte_20A0[v6];
      v6 = byte_20A0[v7];
      v7 = byte_20A0[v8];
      v8 = byte_20A0[v5];
      v5 = byte_2080[v9 >> 2] ^ v10;
    }
    v5 ^= *v4;
    ++v9;
    v4 = (v4 + 4);
    v6 ^= *(v4 - 3);
    v7 ^= *(v4 - 2);
    v8 ^= *(v4 - 1);
    *(v4 + 12) = v5;
    *(v4 + 13) = v6;
    *(v4 + 14) = v7;
    *(v4 + 15) = v8;
  }
  while ( v9 != 44 );
  __asm
  {
    vmovdqa xmm0, cs:xmmword_21B0
    vmovdqa [rsp+208h+var_A8], xmm0
  }
  fread(ptr, 1uLL, 0x40uLL, stdin);
  __asm
  {
    vmovdqa xmm0, cs:xmmword_21C0
    vmovdqa [rsp+208h+var_88], xmm0
    vmovdqa xmm0, cs:xmmword_21D0
  }
  v108 = v110;
  __asm
  {
    vmovdqa [rsp+208h+var_78], xmm0
    vmovdqa xmm0, cs:xmmword_21E0
    vmovdqa [rsp+208h+var_68], xmm0
    vmovdqa xmm0, cs:xmmword_21F0
    vmovdqa [rsp+208h+var_58], xmm0
  }
  v100 = v112[0];
  v101 = v112[2];
  v102 = v112[4];
  v103 = v112[6];
  v104 = v112[8];
  v105 = v112[10];
  v106 = v112[12];
  v107 = v112[14];
  v98 = v115;
  v16 = 16;
  do
  {
    if ( v16 == 16 )
    {
      v20 = &v111;
      __asm { vmovdqa xmm4, [rsp+208h+var_A8] }
      LOBYTE(v87) = byte_20A0[(v113 ^ v108)];
      __asm { vpextrb rax, xmm4, 4 }
      LOBYTE(v86) = byte_20A0[(BYTE4(v108) ^ _RAX)];
      v94 = byte_20A0[BYTE8(v113) ^ BYTE8(v108)];
      __asm { vpextrb rax, xmm4, 0Ch }
      v93 = byte_20A0[(BYTE12(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 1 }
      v25 = byte_20A0[(BYTE1(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 5 }
      v85 = byte_20A0[(BYTE5(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 9 }
      v84 = byte_20A0[(BYTE9(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 0Dh }
      v92 = byte_20A0[(BYTE13(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 2 }
      LOBYTE(v30) = byte_20A0[(BYTE2(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 6 }
      v32 = byte_20A0[(BYTE6(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 0Ah }
      v91 = byte_20A0[(BYTE10(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 0Eh }
      v96 = v32;
      v88 = v25;
      v90 = byte_20A0[(BYTE14(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 3 }
      v36 = byte_20A0[(BYTE3(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 7 }
      v95 = v36;
      v38 = byte_20A0[(BYTE7(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 0Bh }
      v40 = byte_20A0[(BYTE11(v108) ^ _RAX)];
      __asm { vpextrb rax, xmm4, 0Fh }
      v89 = byte_20A0[(HIBYTE(v108) ^ _RAX)];
      do
      {
        v42 = v91 ^ v89 ^ v87 ^ v85;
        v99 = v87 ^ v89;
        v43 = v90 ^ v95 ^ v86 ^ v84;
        v97 = v30 ^ v38 ^ v94 ^ v92;
        v44 = v40 ^ v96 ^ v93 ^ v88;
        v45 = ((2 * (v86 ^ v95)) ^ (27 * ((v86 ^ v95) >> 7)) ^ v95 ^ v43 ^ v20[7]);
        v46 = v20[10] ^ v97 ^ v30 ^ (27 * ((v30 ^ v38) >> 7)) ^ (2 * (v30 ^ v38));
        v47 = v20[11] ^ v97 ^ v38 ^ (2 * (v38 ^ v94)) ^ (27 * ((v38 ^ v94) >> 7));
        v48 = v88 ^ v44 ^ v20[13] ^ (2 * (v88 ^ v96)) ^ (27 * ((v88 ^ v96) >> 7));
        v49 = v96 ^ v44 ^ v20[14] ^ (27 * ((v40 ^ v96) >> 7)) ^ (2 * (v40 ^ v96));
        v50 = v44 ^ v20[15] ^ v40 ^ (2 * (v40 ^ v93)) ^ (27 * ((v40 ^ v93) >> 7));
        LOBYTE(v87) = byte_20A0[((2 * (v87 ^ v85)) ^ (27 * ((v87 ^ v85) >> 7)) ^ v42 ^ *v20 ^ v87)];
        LOBYTE(v86) = byte_20A0[((2 * (v86 ^ v84)) ^ (27 * ((v86 ^ v84) >> 7)) ^ v86 ^ v43 ^ v20[4])];
        v94 = byte_20A0[((2 * (v94 ^ v92)) ^ (27 * ((v94 ^ v92) >> 7)) ^ v94 ^ v97 ^ v20[8])];
        v93 = byte_20A0[((27 * ((v93 ^ v88) >> 7)) ^ (2 * (v93 ^ v88)) ^ v93 ^ v20[12] ^ v44)];
        v88 = byte_20A0[((2 * (v85 ^ v91)) ^ (27 * ((v85 ^ v91) >> 7)) ^ v85 ^ v42 ^ v20[1])];
        v85 = byte_20A0[((27 * ((v84 ^ v90) >> 7)) ^ (2 * (v84 ^ v90)) ^ v84 ^ v43 ^ v20[5])];
        v84 = byte_20A0[((27 * ((v30 ^ v92) >> 7)) ^ (2 * (v30 ^ v92)) ^ v20[9] ^ v97 ^ v92)];
        v92 = byte_20A0[v48];
        v51 = v91 ^ v42 ^ v20[2];
        v20 += 16;
        v30 = byte_20A0[((2 * (v91 ^ v89)) ^ (27 * ((v91 ^ v89) >> 7)) ^ v51)];
        v96 = byte_20A0[((27 * ((v90 ^ v95) >> 7)) ^ (2 * (v90 ^ v95)) ^ v43 ^ *(v20 - 10) ^ v90)];
        v91 = byte_20A0[v46];
        v90 = byte_20A0[v49];
        v40 = byte_20A0[v47];
        v38 = byte_20A0[v45];
        v95 = byte_20A0[((27 * (v99 >> 7)) ^ (2 * v99) ^ v89 ^ v42 ^ *(v20 - 13))];
        v89 = byte_20A0[v50];
      }
      while ( v112 != v20 );
      LOBYTE(v30) = v105 ^ v30;
      LOBYTE(v87) = v100 ^ v87;
      _R15D = v30;
      __asm { vmovd   xmm5, r15d }
      v54 = v86;
      LOBYTE(v86) = v103 ^ v90;
      _R9D = (v101 ^ v91);
      _R10D = (v102 ^ v54);
      _EDX = (v107 ^ v96);
      _R13D = (v104 ^ v94);
      __asm
      {
        vmovd   xmm4, edx
        vmovd   xmm7, r9d
        vpinsrb xmm5, xmm5, ebx, 1
        vmovd   xmm3, r10d
      }
      v63 = 15LL;
      _ESI = (v106 ^ v93);
      __asm
      {
        vmovd   xmm1, r13d
        vmovd   xmm0, [rsp+208h+var_1F8]
        vmovd   xmm6, [rsp+208h+var_1FC]
        vpinsrb xmm7, xmm7, [rsp+208h+var_1FD], 1
        vpinsrb xmm0, xmm0, eax, 1
        vpinsrb xmm1, xmm1, r11d, 1
        vpunpcklwd xmm0, xmm0, xmm7
      }
      v72 = HIBYTE(v113);
      __asm
      {
        vpinsrb xmm3, xmm3, [rsp+208h+var_1FE], 1
        vpinsrb xmm6, xmm6, [rsp+208h+var_1F4], 1
        vpunpcklwd xmm1, xmm1, xmm5
        vpunpcklwd xmm3, xmm3, xmm6
        vmovd   xmm2, esi
        vpunpckldq xmm0, xmm0, xmm3
        vpinsrb xmm2, xmm2, r8d, 1
        vpinsrb xmm4, xmm4, ecx, 1
        vpunpcklwd xmm2, xmm2, xmm4
        vpunpckldq xmm1, xmm1, xmm2
        vpunpcklqdq xmm0, xmm0, xmm1
        vmovdqa [rsp+208h+var_98], xmm0
      }
      if ( HIBYTE(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE14(v113);
      HIBYTE(v113) = 0;
      v63 = 14LL;
      if ( BYTE14(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE13(v113);
      BYTE14(v113) = 0;
      v63 = 13LL;
      if ( BYTE13(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE12(v113);
      BYTE13(v113) = 0;
      v63 = 12LL;
      if ( BYTE12(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE11(v113);
      BYTE12(v113) = 0;
      v63 = 11LL;
      if ( BYTE11(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE10(v113);
      BYTE11(v113) = 0;
      v63 = 10LL;
      if ( BYTE10(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE9(v113);
      BYTE10(v113) = 0;
      v63 = 9LL;
      if ( BYTE9(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE8(v113);
      BYTE9(v113) = 0;
      v63 = 8LL;
      if ( BYTE8(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE7(v113);
      BYTE8(v113) = 0;
      v63 = 7LL;
      if ( BYTE7(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE6(v113);
      BYTE7(v113) = 0;
      v63 = 6LL;
      if ( BYTE6(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE5(v113);
      BYTE6(v113) = 0;
      v63 = 5LL;
      if ( BYTE5(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE4(v113);
      BYTE5(v113) = 0;
      v63 = 4LL;
      if ( BYTE4(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE3(v113);
      BYTE4(v113) = 0;
      v63 = 3LL;
      if ( BYTE3(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE2(v113);
      BYTE3(v113) = 0;
      v63 = 2LL;
      if ( BYTE2(v113) != 0xFF )
        goto LABEL_14;
      v72 = BYTE1(v113);
      BYTE2(v113) = 0;
      v63 = 1LL;
      if ( BYTE1(v113) == 0xFF && (v72 = v113, BYTE1(v113) = 0, v63 = 0LL, v113 == 0xFF) )
      {
        LOBYTE(v113) = 0;
        v16 = 0;
      }
      else
      {
LABEL_14:
        *(&v113 + v63) = v72 + 1;
        v16 = 0;
      }
    }
    v17 = v16++;
    *v98++ ^= *(&v115[-1] + v17);
  }
  while ( &v116 != v98 );
  v18 = memcmp(v115, ptr, 0x40uLL);
  if ( v18 )
  {
    v18 = 1;
    puts("Nope, come back later");
  }
  else
  {
    puts("Yep, that's it!");
  }
  return v18;
}
```
:::

## Recon
這一題一開始要我們輸入些東西，應該是flag，不用管中間的一些操作，可以先考慮最後怎麼判斷是不是回答正確就好，可以看到他最後call了一個memcmp的system function，應該就是用來判斷，所以我們只要continue到那裡，應該就會知道原本的flag是多少了

## Exploit
```bash!
$ gdb not-crypto
gef➤  starti
gef➤  vmmap # 確認目前code sction的base address是多少
gef➤  b *(0x0000555555555000+0x3b9)
gef➤  c
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa # fake flag for temp
gef➤  x/s 0x00007fffffffd730
0x7fffffffd730: "picoCTF{c0mp1l3r_0pt1m1z4t10n_15_pur3_w1z4rdry_but_n0_pr0bl3m?}\n\226\327\377\377\377\177"
```
![](https://hackmd.io/_uploads/r1p1fwk6h.png)

Flag: `picoCTF{c0mp1l3r_0pt1m1z4t10n_15_pur3_w1z4rdry_but_n0_pr0bl3m?}`

## Reference
[pico reverse - not crypto wp - ](https://www.ctfwriteup.com/picoctf/picomini-by-redpwn/reverse-engineering#not-crypto)