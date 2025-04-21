---
title: PicoCTF - Easy as GDB
tags: [PicoCTF, CTF, Reverse]

category: "Security/Practice/PicoCTF/Reverse"
---

# PicoCTF - Easy as GDB
<!-- more -->

## Source code
:::spoiler IDA Main Function
```cpp=
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char *str_len; // eax
  int v5; // [esp-8h] [ebp-20h]
  int v6; // [esp-4h] [ebp-1Ch]
  char *input_flag; // [esp+4h] [ebp-14h]
  size_t str_len_1; // [esp+8h] [ebp-10h]
  char *src; // [esp+Ch] [ebp-Ch]

  input_flag = calloc(0x200u, 1u);
  printf("input the flag: ");
  fgets(input_flag, 512, stdin);
  str_len = strnlen(aZNh, 512, v5, v6);
  src = enc_input(str_len, str_len);
  sub_7C2(src, 1, 1);
  if ( check_flag(src, str_len_1) == 1 )
    puts("Correct!");
  else
    puts("Incorrect.");
  return 0;
}
```
:::

:::spoiler IDA Main Encryption Part
```cpp=
char *__cdecl sub_82B(char *src, size_t enc_flag_len)
{
  unsigned int i; // [esp+0h] [ebp-18h]
  char *dest; // [esp+Ch] [ebp-Ch]
  size_t enc_flag_len_and; // [esp+24h] [ebp+Ch]

  enc_flag_len_and = (enc_flag_len & 0xFFFFFFFC) + 4;
  dest = malloc(enc_flag_len_and + 1);
  strncpy(dest, src, enc_flag_len_and);
  for ( i = 0xABCF00D; i < 0xDEADBEEF; i += 0x1FAB4D )
    main_enc_part(dest, enc_flag_len_and, i);
  return dest;
}
```
:::
:::spoiler IDA Main Encryption Part 2
```cpp=
unsigned int __cdecl sub_6BD(int dest, unsigned int enc_flag_len_and, int idx)
{
  unsigned int result; // eax
  unsigned int i; // [esp+14h] [ebp-14h]
  char v5[4]; // [esp+18h] [ebp-10h]
  unsigned int v6; // [esp+1Ch] [ebp-Ch]

  v6 = __readgsdword(0x14u);
  v5[0] = HIBYTE(idx);                          // 0x0a
  v5[1] = BYTE2(idx);                           // 0xbc
  v5[2] = BYTE1(idx);                           // 0xf0
  v5[3] = idx;                                  // 0x0d
  for ( i = 0; i < enc_flag_len_and; ++i )
    *(dest + i) ^= v5[i & 3];
  result = __readgsdword(0x14u) ^ v6;
  if ( result )
    sub_B20();
  return result;
}
```
:::

## Recon
這一題算簡單，但搞了好久，一方面是ida有些東西翻的很醜，一方面gdb看不出來main, encryption等等function symbol，所以一些動態的address的提示都沒有，會有點妨礙，但整體來說他做的事情就是他先把index的每一個bytes，都獨立出來，以0x0abcf00d來說，
    v5[0]=0x0a
    v5[1]=0xbc
    v5[2]=0xf0
    v5[3]=0x0d
然後跟我們的input的每一個bytes都進行XOR，當第一round結束後new index = 0x0abcf00d + 0x1FAB4D，然後重複前面執行的部分，所以我們要做的事情就只是重複剛剛所有的過程，就可以拿到flag了。
至於要比較的ciphertext可以直接從gdb的動態看出來

## Exploit
```python=
cipher = bytes.fromhex("2E6E40681D53657C175816436D5862366F436230016347333F6314636d7a00")

flag = []
for i in range(len(cipher)):
    flag.append(hex(cipher[i])[2:])


for i in range(0xABCF00D, 0xdea62e4b, 0x1FAB4D):
    tmp_idx = hex(i)[2:].encode()
    if len(tmp_idx) < 8:
        tmp_idx = b'0' + tmp_idx
    key = [int(tmp_idx[-8:-6], 16), int(tmp_idx[-6:-4], 16), int(tmp_idx[-4:-2], 16), int(tmp_idx[-2:], 16)]

    for j in range(len(cipher)):
        tmp = hex(int(flag[j], 16) ^ key[j % 4])[2:]
        flag[j] = tmp
        # cipher[j] = bytes.fromhex(hex(cipher[j] ^ key[j % 4])[2:])
print(bytes.fromhex("".join(flag)).decode('cp437'))
```