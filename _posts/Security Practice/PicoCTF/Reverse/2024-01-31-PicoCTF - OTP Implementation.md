---
title: PicoCTF - OTP Implementation
tags: [PicoCTF, CTF, Reverse]

category: "Security Practice｜PicoCTF｜Reverse"
date: 2024-01-31
---

# PicoCTF - OTP Implementation
<!-- more -->

## Source code
:::spoiler IDA Main Function
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4; // al
  char v5; // dl
  unsigned int v6; // eax
  int i; // [rsp+18h] [rbp-E8h]
  int j; // [rsp+1Ch] [rbp-E4h]
  char input_key[112]; // [rsp+20h] [rbp-E0h] BYREF
  char tmp_key[104]; // [rsp+90h] [rbp-70h] BYREF
  unsigned __int64 v11; // [rsp+F8h] [rbp-8h]

  v11 = __readfsqword(0x28u);
  if ( argc > 1 )
  {
    strncpy(input_key, argv[1], 0x64uLL);
    input_key[100] = 0;
    for ( i = 0; valid_char(input_key[i]); ++i )// 確認字元是否在[0-9|a-f]之間
    {
      if ( i )
      {
        v4 = jumble(input_key[i]);
        v5 = tmp_key[i - 1] + v4;
        v6 = ((tmp_key[i - 1] + v4) >> 31) >> 28;
        tmp_key[i] = ((v6 + v5) & 0xF) - v6;
      }
      else
      {
        tmp_key[0] = jumble(input_key[0]) % 16;
      }
    }
    for ( j = 0; j < i; ++j )
      tmp_key[j] += 0x61;
    if ( i == 100
      && !strncmp(
            tmp_key,
            "bajbgfapbcclgoejgpakmdilalpomfdlkngkhaljlcpkjgndlgmpdgmnmepfikanepopbapfkdgleilhkfgilgabldofbcaedgfe",
            100uLL) )
    {
      puts("You got the key, congrats! Now xor it with the flag!");
      return 0;
    }
    else
    {
      puts("Invalid key!");
      return 1;
    }
  }
  else
  {
    printf("USAGE: %s [KEY]\n", *argv);
    return 1;
  }
}
```
:::

:::spoiler IDA Jumble Function
```cpp
__int64 __fastcall jumble(char input_key_char)
{
  char v2; // [rsp+0h] [rbp-4h]
  char v3; // [rsp+0h] [rbp-4h]

  v2 = input_key_char;
  if ( input_key_char > 0x60 )
    v2 = input_key_char + 9;
  v3 = 2 * (v2 % 16);
  if ( v3 > 15 )
    ++v3;
  return v3;
}
```
:::
:::spoiler IDA Valid Function
```cpp
_BOOL8 __fastcall valid_char(char a1)
{
  if ( a1 > 0x2F && a1 <= 0x39 )
    return 1LL;
  return a1 > 0x60 && a1 <= 0x66;
}
```
:::

## Recon
這一題頗難，我寫的script也沒有很好，readability頗低，但我就爛，懶得優化了
1. 這一題簡單來說就是把我們輸入的key做一些操作，然後把它和`bajbgfa...`做比較，如果對了我們就可以直接和他提供的flag進行xor，然後轉換成ASCII
2. 有幾個重點，首先透過valid_char function可以知道我們輸入的key一定介於[0-9a-f]之間(這是個伏筆，因為他最後會直接和他提供的ciphertext進行xor，所以其實就是hex字元)
3. 接著可以從後面推回來，第一個flag做了一些操作，之後就直接加上0x61，再和`bajbgfa...`做比較，所以我們先減回去
    :::spoiler tmp_key
    `[1, 0, 9, 1, 6, 5, 0, 15, 1, 2, 2, 11, 6, 14, 4, 9, 6, 15, 0, 10, 12, 3, 8, 11, 0, 11, 15, 14, 12, 5, 3, 11, 10, 13, 6, 10, 7, 0, 11, 9, 11, 2, 15, 10, 9, 6, 13, 3, 11, 6, 12, 15, 3, 6, 12, 13, 12, 4, 15, 5, 8, 10, 0, 13, 4, 15, 14, 15, 1, 0, 15, 5, 10, 3, 6, 11, 4, 8, 11, 7, 10, 5, 6, 8, 11, 6, 0, 1, 11, 3, 14, 5, 1, 2, 0, 4, 3, 6, 5, 4]`
    :::
4. 接著我們分析jumble function在幹嘛，簡單來說，如果傳入的是
    * '0'-'9'$\to$return 0 2 4 6 8 10 12 14 17 19
    * 'a'-'f'$\to$return 21 23 25 27 29 31
5. 跟著if statement走`tmp_key[0] = jumble(input_key[0]) % 16;`
我們知道`tmp_key[0]=0x1`(因為key的第一個字元是`b`$\to$`0x62`，減掉`0x61=0x1`)，所以仔細推敲jumble(input_key[0])的return value是`0 2 4 6 8 10 12 14 1 3 5 7 9 11 13 15`(對應到的是[0-9a-f])，所以代表0x1在經過mod運算是0x11(要+16)，而正確的key就是對應到的8
6. 接著換下一個字元，先破哏，if statement裡面的v6基本上是零，畢竟右移那麼多次，也不知道作者設計這個有甚麼用，可能是混淆逆向的?!但反正
    ```
    v4 -> jumble(tmp_key[i-1])([0 2 4 6 8 10 12 14 , .... , 31])
    v5 -> [0-15]+v4
    v6 -> v5 >> 59 (基本上是0)
    tmp_key[i] = v5 & 0xf
    ```
    可以看到tmp_key[i]是v5和0xf做and operation，意思是他只會保留一個byte的後四個bits，跟一下gdb會發現前四bits，有可能存在，所以我們可以透過v5-v4是正還是負判斷前四bits有沒有數值，舉個例子，tmp_key[1]是0，而要判斷v5是0x0還是0x10可以透過減掉tmp_key[0]=1來決定，當結果是負的，就要加0x10，所以v5是0x10，v4是0xf，此時會發現沒有相對應的數值可以轉換，因為jumble function的return value並不包含0xf，所以我們要再加上0x10=0x1f，因為其實v5真正的數值是0x20才對，有了v4=31，就可以知道key[1]='f'
    
6. 就這樣不斷做下去，就能拿到key了，開寫script

## Exploit
```python
enc_key = "bajbgfapbcclgoejgpakmdilalpomfdlkngkhaljlcpkjgndlgmpdgmnmepfikanepopbapfkdgleilhkfgilgabldofbcaedgfe"
enc_key_1 = []
jumble_table = {
    0:{'0':'0'},
    2:{'2':'1'},
    4:{'4':'2'},
    6:{'6':'3'},
    8:{'8':'4'},
    10:{'10':'5'},
    12:{'12':'6'},
    14:{'14':'7'},
    1:{'17':'8'},
    3:{'19':'9'},
    5:{'21':'a'},
    7:{'23':'b'},
    9:{'25':'c'},
    11:{'27':'d'},
    13:{'29':'e'},
    15:{'31':'f'},
}

FLAG= ""
def get_flag(str_1):
    if str_1 % 2 == 0:
        return jumble_table[str_1][str(str_1)]
    else:
        return jumble_table[str_1][str(str_1 + 16)]


for i, single_chr in enumerate(enc_key):
    enc_key_1.append(ord(single_chr) - 0x61)
    if i == 0:
        FLAG += get_flag(enc_key_1[-1])

    else:
        tmp = enc_key_1[-1] - enc_key_1[-2]
        if tmp < 0:
            tmp += 16
        FLAG += get_flag(tmp)

cipher_text = open("./flag.txt", "r").read()
xor_tmp = int(cipher_text, 16) ^ int(FLAG, 16)
print(bytes.fromhex('{:x}'.format(xor_tmp)).decode('utf-8'))
```


Flag: `picoCTF{cust0m_jumbl3s_4r3nt_4_g0Od_1d3A_42dad069}`