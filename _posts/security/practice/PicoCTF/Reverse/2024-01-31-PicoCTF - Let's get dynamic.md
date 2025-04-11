---
title: PicoCTF - Let's get dynamic
tags: [PicoCTF, CTF, Reverse]

category: "Security/Practice/PicoCTF/Reverse"
---

# PicoCTF - Let's get dynamic
## Source code
:::spoiler IDA Main Function
```cpp=
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+1Ch] [rbp-114h]
  char s2[64]; // [rsp+20h] [rbp-110h] BYREF
  char s[64]; // [rsp+60h] [rbp-D0h] BYREF
  char v7[8]; // [rsp+A0h] [rbp-90h] BYREF
  __int64 v8; // [rsp+A8h] [rbp-88h]
  __int64 v9; // [rsp+B0h] [rbp-80h]
  __int64 v10; // [rsp+B8h] [rbp-78h]
  __int64 v11; // [rsp+C0h] [rbp-70h]
  __int64 v12; // [rsp+C8h] [rbp-68h]
  __int16 v13; // [rsp+D0h] [rbp-60h]
  __int64 v14[6]; // [rsp+E0h] [rbp-50h]
  __int16 v15; // [rsp+110h] [rbp-20h]
  unsigned __int64 v16; // [rsp+118h] [rbp-18h]

  v16 = __readfsqword(0x28u);
  *v7 = 0xFD872AC7CA737102LL;
  v8 = 0x4915F12BF9F82DCBLL;
  v9 = 0xA7EF0D4C54003C10LL;
  v10 = 0x9399CCF74D02A843LL;
  v11 = 0x2AC6F818989688D7LL;
  v12 = 0x9F51EBCA33584C85LL;
  v13 = 231;
  v14[0] = 0x92D46893B5010A61LL;
  v14[1] = 0xA6BDE59D58F4EB4LL;
  v14[2] = 0xFC993A3238355027LL;
  v14[3] = 0xEDA7B28D7054D179LL;
  v14[4] = 0x419FBB499BD4CFBBLL;
  v14[5] = 0x935AE3903F554688LL;
  v15 = 185;
  fgets(s, 49, _bss_start);
  for ( i = 0; i < strlen(v7); ++i )
    s2[i] = *(v14 + i) ^ v7[i] ^ i ^ 0x13;
  if ( !memcmp(s, s2, 49uLL) )
  {
    puts("No, that's not right.");
    return 1;
  }
  else
  {
    puts("Correct! You entered the flag.");
    return 0;
  }
}
```
:::
## Recon
這一題也沒有很難，就要用dbg細心的跟一下，然後不太確定這一題設計的用意，但無論如何還是蠻直觀的
可以看到IDA解析的source code中間有一段是在進行encryption，然後只要反著做就可以拿到flag，但重點是他實際跑起來會和肉眼觀察到的有一點不一樣，一開始讀取的時候會從v7的後端以及v14[0]的後端開始xor，所以如果像我要從兩者最後一個byte開始解密的話，index的i就要特別注意，不過我也是建議要從第一個byte開始解密，因為這樣會對應到flag的第一個字元，所以如果不知道這支程式怎麼加密的話，可以直接跑下面的script，用debugger追一下就知道了

## Exploit
```python=
enc_flag = [[0x92, 0xD4, 0x68, 0x93, 0xB5, 0x01, 0x0A, 0x61, ],
            [0x0A, 0x6B, 0xDE, 0x59, 0xD5, 0x8F, 0x4E, 0xB4, ],
            [0xFC, 0x99, 0x3A, 0x32, 0x38, 0x35, 0x50, 0x27, ],
            [0xED, 0xA7, 0xB2, 0x8D, 0x70, 0x54, 0xD1, 0x79, ],
            [0x41, 0x9F, 0xBB, 0x49, 0x9B, 0xD4, 0xCF, 0xBB, ],
            [0x93, 0x5A, 0xE3, 0x90, 0x3F, 0x55, 0x46, 0x88]]# 0x7fffffffd660
key = [[0xFD, 0x87, 0x2A, 0xC7, 0xCA, 0x73, 0x71, 0x02, ],
       [0x49, 0x15, 0xF1, 0x2B, 0xF9, 0xF8, 0x2D, 0xCB, ],
       [0xA7, 0xEF, 0x0D, 0x4C, 0x54, 0x00, 0x3C, 0x10, ],
       [0x93, 0x99, 0xCC, 0xF7, 0x4D, 0x02, 0xA8, 0x43, ],
       [0x2A, 0xC6, 0xF8, 0x18, 0x98, 0x96, 0x88, 0xD7, ],
       [0x9F, 0x51, 0xEB, 0xCA, 0x33, 0x58, 0x4C, 0x85]]# 0x7fffffffd620


FLAG = []
for i in range(len(enc_flag)):
    for j in range(len(enc_flag[0])):
        FLAG.append(bytes.fromhex(hex(enc_flag[i][7-j] ^ key[i][7-j] ^ 0x13 ^ (j + 8 * i))[2:]).decode('utf-8'))

print("".join(FLAG) + "}")
```

Flag: `picoCTF{dyn4m1c_4n4ly1s_1s_5up3r_us3ful_6044e660}`