---
title: CrewCTF - ez rev
tags: [CTF, CrewCTF, Reverse]

category: "Security/Practice/CrewCTF/Reverse"
---

# CrewCTF - ez rev

## Source Code
:::spoiler IDA Fake Main Function
```cpp
void __fastcall __noreturn main(int a1, char **a2, char **a3)
{
  int i; // [rsp+Ch] [rbp-4h]

  puts("[+] Another flag checker...");
  fgets(byte_4200E0, 256, stdin);
  if ( byte_4200E0[strlen(byte_4200E0) - 1] == 10 )
    byte_4200E0[strlen(byte_4200E0) - 1] = 0;
  for ( i = 0; i <= 73; ++i )
  {
    if ( byte_4200E0[i] != (byte_420060[i] ^ 0x70) )
      sub_401220();
  }
  sub_401202();
}
```
:::

## Recon
首先這一題真的太難了，超出我的守備範圍，所以我先寫一些當作紀錄，之後可以更快銜接繼續解
1. 首先可以執行一下，如果是在Ubuntu 20.04(預設Libc版本是2.31)的版本和其他版本會有不一樣的output
    ```bash
    $ ldd --version
    ldd (Ubuntu GLIBC 2.31-0ubuntu9.9) 2.31
    Copyright (C) 2020 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Written by Roland McGrath and Ulrich Drepper.
    $ ./a.out
    [+] Another flag checker...
    123456
    [-] No :(
    $ ldd --version
    ldd (Ubuntu GLIBC 2.35-0ubuntu3) 2.35
    Copyright (C) 2022 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Written by Roland McGrath and Ulrich Drepper.
    ./a.out
    [+] Another flag checker...
    123456
    [-] Why you still here
    ```
    這是因為他和這隻程式執行的過程有關係
2. 用IDA看一下發現有翻譯出main function，但這個main function其實是假的，這個可以從上面的進度條看出來，橘色的部分感覺很可疑，而假的main function卻是在整個進度的後半段，代表可以往前分析一下，但由於整體的流程太長，所以搞事的部分沒辦法分析出來，這要用動態去看會比較清楚(真正的main function是在==sub_40123E()==)
![](https://hackmd.io/_uploads/rkqsdVzc3.png)
另外也可以用strings xref的方式知道他call strings的地方有兩個，其中一個就是真的main function
![](https://hackmd.io/_uploads/rJnTY4z92.png)

3. 分析real main function過程大概是
    1. 用ptrace看有沒有使用debugger，所以這邊要先patch
    2. 接著輸入flag，放在`0x4200e0`
    3. 接著就是進入`loc_4012FE()`，這邊應該就是做一些檢查，也要patch，會做三次，如果都正確才會真正進入到搞事的function(`loc_4013AA`)，否則會進到`loc_401394`說掰掰，這一段其實就是在檢查libc是不是在正確的版本以利後面的搞事節奏
    4. 搞事的function做的事情很簡單，就是不斷用*($rbp-0x100e0)(也就是0x00007ffff7da52fd)做一些offset的加減，然後把對應到的address放到$rbp對應的位置
    例如：
        ```bash
        0x7ffffffed8c0:	0x00000000000008c0	0x0000000000000a40
        0x7ffffffed8d0:	0x00007ffff7dc4000	0x0000000000000014
        0x7ffffffed8e0:	0x00007ffff7de684d	0x00007ffff7de7b6a
        0x7ffffffed8f0:	0x00007ffff7dfa174	0x00007ffff7de66c0
        0x7ffffffed900:	0x00007ffff7dea01f	0x00007ffff7f06c92
        0x7ffffffed910:	0x00007ffff7ec657e	0x00000000004011fc
        0x7ffffffed920:	0x00007ffff7ed055f	0x00007ffff7ea9190
        0x7ffffffed930:	0x00007ffff7e58eab	0x00007ffff7e70186
        0x7ffffffed940:	0x00007ffff7df9a22	0x00007ffff7dea6e3
        0x7ffffffed950:	0x00007ffff7e72df5	0x00007ffff7e6ff48
        0x7ffffffed960:	0x00007ffff7e6e38c	0x00007ffff7e3561e
        0x7ffffffed970:	0x00007ffff7f0873b	0x00007ffff7eb5b65
        0x7ffffffed980:	0x00007ffff7e701dc	0x00007ffff7df7da1
        0x7ffffffed990:	0x00007ffff7ee37d7	0x00000000004011ee
        0x7ffffffed9a0:	0x00000000004011f3	0x00000000004011f8


        0x7ffffffed9b0:	0x00007ffff7dea01f(pop rsi; ret)	0x00000000000000ff
        0x7ffffffed9c0:	0x00007ffff7de66c0(pop rbp; ret)	0x0000000000420328
        0x7ffffffed9d0:	0x00007ffff7f06c92(pop rdx; ret)	0x0000000000000000
        0x7ffffffed9e0:	0x00007ffff7e58eab(cmp DWORD PTR [rbp+rdx*1+0x0], esi; ret)	0x00007ffff7dfa174(pop rax; ret)
        0x7ffffffed9f0:	0x0000000000000000	0x00007ffff7ed055f(setl al; ret)
        0x7ffffffeda00:	0x00000000004011ee	0x00007ffff7dea01f
        0x7ffffffeda10:	0x000000000000001a	0x00000000004011f3
        0x7ffffffeda20:	0x00007ffff7ec657e	0x0000000000000000
        0x7ffffffeda30:	0x0000000038188124	0x00007ffff7e72df5
        0x7ffffffeda40:	0x00007ffff7dfa174	0x000000000042029d
        ```
    5. 放完之後就call `memcpy(src=0x00007ffffffed9b0, dest=0x00007ffffffed8b0, n=0x6e50)`，然後執行ROP，沒錯就是ROP，所以他要先在前面檢查libc的版本，讓他可以取得正確的gadget
    6. 現在的問題是因為他存放的ROP太多也很複雜，導致我不知道哪邊其實是確切在執行check flag的環節，我有想說要找system call之類的gadget，但還找不到，所以分析了老半天還是沒結果

## Exploit
Discord上別人的腳本
:::spoiler Script
```python
from z3 import *
s = Solver()

flag = [BitVec(f"flag[{i}]",8) for i in range(0x100)]
tmp = []
t = 0x69
for i in range(len(flag)):
    t = (flag[i]+i)^t
    tmp.append(t)
t = 0x96
for i in range(1,len(flag)):
    tmp[i] = ((tmp[i-1] - tmp[i]) ^ t)&0xff
    t = tmp[i]
enc = bytes.fromhex("0a07ee64058ef6943d85178411691c8902751f8c01830b85169a0e8c0084038517b30f9f3ce417b7609537f9d5af46a243b15aa07c62f96b06ad1dc93ef3e49332c31ea10ac31cd330d33cd03ece8bdf32c209cf81cd89c9f33295c480ba99e910e009dd3039743e655f3a2010c42c0812c824dc58736b5454736f2cf033d374bc33b73ca8d3fb34a4d3ff2ca0d3e354cc53c75cf8334b54f4334f6cd073b3349cf397fc88d39bf484d39fec80d383d4ec53e75c98f3abd494f3")

for i in range(len(enc)):
    s.add(enc[i] == tmp[i])
print(s.check())
m = s.model()
for d in m.decls():
    print("%s = %s"%(d.name(),m[d]))
flag = [0]*0x100
flag[5] = 116
flag[42] = 110
flag[175] = 0
flag[137] = 0
flag[34] = 98
flag[118] = 0
flag[65] = 114
flag[54] = 99
flag[23] = 111
flag[31] = 97
flag[38] = 111
flag[177] = 0
flag[55] = 105
flag[0] = 99
flag[120] = 0
flag[128] = 0
flag[62] = 111
flag[13] = 105
flag[180] = 0
flag[44] = 120
flag[25] = 95
flag[28] = 112
flag[50] = 101
flag[57] = 108
flag[27] = 111
flag[71] = 98
flag[33] = 95
flag[133] = 0
flag[158] = 0
flag[169] = 0
flag[115] = 125
flag[184] = 0
flag[140] = 0
flag[91] = 116
flag[24] = 119
flag[106] = 103
flag[59] = 121
flag[74] = 95
flag[170] = 0
flag[160] = 0
flag[49] = 95
flag[147] = 0
flag[69] = 114
flag[80] = 117
flag[93] = 105
flag[68] = 101
flag[97] = 111
flag[30] = 99
flag[101] = 114
flag[32] = 110
flag[4] = 99
flag[58] = 108
flag[10] = 108
flag[63] = 114
flag[159] = 0
flag[26] = 114
flag[168] = 0
flag[45] = 105
flag[29] = 95
flag[72] = 117
flag[64] = 95
flag[179] = 0
flag[99] = 95
flag[47] = 117
flag[108] = 100
flag[129] = 0
flag[119] = 0
flag[2] = 101
flag[39] = 95
flag[139] = 0
flag[11] = 108
flag[8] = 119
flag[149] = 0
flag[35] = 101
flag[3] = 119
flag[142] = 0
flag[131] = 0
flag[60] = 95
flag[178] = 0
flag[19] = 116
flag[22] = 110
flag[40] = 111
flag[113] = 101
flag[95] = 95
flag[121] = 0
flag[96] = 121
flag[134] = 0
flag[136] = 0
flag[141] = 0
flag[67] = 118
flag[145] = 0
flag[150] = 0
flag[73] = 116
flag[83] = 97
flag[151] = 0
flag[155] = 0
flag[172] = 0
flag[174] = 0
flag[14] = 95
flag[103] = 95
flag[132] = 0
flag[138] = 0
flag[163] = 0
flag[36] = 95
flag[78] = 121
flag[37] = 115
flag[109] = 95
flag[153] = 0
flag[107] = 111
flag[76] = 102
flag[125] = 0
flag[53] = 101
flag[85] = 95
flag[51] = 115
flag[173] = 0
flag[176] = 0
flag[181] = 0
flag[182] = 0
flag[18] = 110
flag[16] = 105
flag[104] = 97
flag[123] = 0
flag[61] = 102
flag[43] = 111
flag[126] = 0
flag[185] = 0
flag[6] = 102
flag[90] = 95
flag[148] = 0
flag[165] = 0
flag[48] = 115
flag[117] = 0
flag[164] = 0
flag[114] = 114
flag[98] = 117
flag[77] = 95
flag[79] = 111
flag[84] = 110
flag[88] = 110
flag[105] = 95
flag[122] = 0
flag[127] = 0
flag[111] = 101
flag[156] = 0
flag[81] = 95
flag[166] = 0
flag[21] = 107
flag[161] = 0
flag[183] = 0
flag[86] = 102
flag[171] = 0
flag[20] = 95
flag[87] = 105
flag[92] = 104
flag[46] = 111
flag[146] = 0
flag[12] = 95
flag[167] = 0
flag[157] = 0
flag[52] = 112
flag[56] = 97
flag[102] = 101
flag[130] = 0
flag[152] = 0
flag[89] = 100
flag[41] = 98
flag[162] = 0
flag[110] = 114
flag[144] = 0
flag[7] = 123
flag[17] = 100
flag[66] = 101
flag[82] = 99
flag[100] = 97
flag[1] = 114
flag[75] = 105
flag[116] = 0
flag[94] = 115
flag[124] = 0
flag[135] = 0
flag[143] = 0
flag[112] = 118
flag[9] = 101
flag[15] = 100
flag[70] = 95
flag[154] = 0

print(bytes(flag))
```
:::

Flag: `crewctf{well_i_didnt_know_rop_can_be_so_obnoxious_especially_for_rever_but_if_you_can_find_this_you_are_a_god_rever}`