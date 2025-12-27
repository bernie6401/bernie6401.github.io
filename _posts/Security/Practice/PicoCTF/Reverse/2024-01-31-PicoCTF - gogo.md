---
title: PicoCTF - gogo
tags: [PicoCTF, CTF, Reverse]

category: "Security｜Practice｜PicoCTF｜Reverse"
---

# PicoCTF - gogo
<!-- more -->

## Source code
:::spoiler IDA Main Function
```cpp=
// main.main
void __cdecl main_main()
{
  _slice_interface_ typ[2]; // [esp+0h] [ebp-58h] BYREF
  string *second_flag; // [esp+20h] [ebp-38h]
  string *flag; // [esp+24h] [ebp-34h]
  _slice_interface_ v3; // [esp+28h] [ebp-30h] BYREF
  string *v4; // [esp+34h] [ebp-24h]
  _DWORD v5[2]; // [esp+38h] [ebp-20h] BYREF
  _DWORD v6[2]; // [esp+40h] [ebp-18h] BYREF
  _slice_interface_ v7; // [esp+48h] [ebp-10h] BYREF
  string *v8; // [esp+54h] [ebp-4h]

  flag = runtime_newobject(&RTYPE_string_0);
  typ[0].array = "Enter Password: ";
  typ[0].len = 16;
  memset(&typ[0].cap, 0, sizeof(_slice_interface_));
  fmt_Printf(*&typ[0].array, *&typ[0].cap);
  v6[0] = &RTYPE__ptr_string;
  v6[1] = flag;
  typ[0].array = "%s\n";
  typ[0].len = 3;
  typ[0].cap = v6;
  *&typ[1].array = 0x100000001LL;
  fmt_Scanf(*&typ[0].array, *&typ[0].cap);
  if ( main_checkPassword(*flag) )
  {
    v5[0] = &RTYPE_string_0;
    v5[1] = &main_statictmp_0;
    typ[0].array = v5;
    *&typ[0].len = 0x100000001LL;
    fmt_Println(typ[0]);
    v3.cap = &RTYPE_string_0;
    v4 = &main_statictmp_1;
    typ[0].array = &v3.cap;
    *&typ[0].len = 0x100000001LL;
    fmt_Println(typ[0]);
    v3.array = &RTYPE_string_0;
    v3.len = &main_statictmp_2;
    typ[0].array = &v3;
    *&typ[0].len = 0x100000001LL;
    fmt_Println(typ[0]);
    second_flag = runtime_newobject(&RTYPE_string_0);
    v7.cap = &RTYPE__ptr_string;
    v8 = second_flag;
    typ[0].array = "%s\n";
    typ[0].len = 3;
    typ[0].cap = &v7.cap;
    *&typ[1].array = 0x100000001LL;
    fmt_Scanf(*&typ[0].array, *&typ[0].cap);
    main_ambush(*second_flag);
    runtime_deferproc(0, &stru_81046A0);
  }
  else
  {
    v7.array = &RTYPE_string_0;
    v7.len = &main_statictmp_3;
    typ[0].array = &v7;
    *&typ[0].len = 0x100000001LL;
    fmt_Println(typ[0]);
  }
  runtime_deferreturn(typ[0].array);
}
```
:::

:::spoiler IDA First Stage Checker
```cpp=
// main.checkPassword
bool __golang main_checkPassword(string flag)
{
  __int32 idx; // eax
  int check_counter; // ebx
  uint8 key[32]; // [esp+4h] [ebp-40h] BYREF
  char enc_flag[32]; // [esp+24h] [ebp-20h]

  if ( flag.len < 32 )
    os_Exit(0);
  (loc_8090B18)();
  qmemcpy(key, "861836f13e3d627dfa375bdb8389214e", sizeof(key));
  (loc_8090FE0)();
  idx = 0;
  check_counter = 0;
  while ( idx < 32 )
  {
    if ( idx >= flag.len || idx >= 0x20 )
      runtime_panicindex();
    if ( (key[idx] ^ flag.str[idx]) == enc_flag[idx] )
      ++check_counter;
    ++idx;
  }
  return check_counter == 32;
}
```
:::

:::spoiler IDA Second Stage Checker
```cpp=
// main.ambush
void __golang main_ambush(string second_flag)
{
  int j; // eax
  _slice_uint8 v2; // [esp+0h] [ebp-94h]
  _slice_uint8 s; // [esp+4h] [ebp-90h]
  _slice_uint8 dataa; // [esp+Ch] [ebp-88h]
  string data; // [esp+Ch] [ebp-88h]
  string data_4; // [esp+10h] [ebp-84h]
  uint8 v7; // [esp+1Fh] [ebp-75h]
  unsigned __int32 i; // [esp+20h] [ebp-74h]
  uint8 hashed[16]; // [esp+24h] [ebp-70h] BYREF
  uint8 key[32]; // [esp+34h] [ebp-60h] BYREF
  uint8 buf[32]; // [esp+54h] [ebp-40h] BYREF
  uint8 v12[32]; // [esp+74h] [ebp-20h] BYREF

  dataa = runtime_stringtoslicebyte(buf, second_flag);
  crypto_md5_Sum(dataa);
  (loc_8091008)();
  (loc_8090B18)();
  qmemcpy(key, "861836f13e3d627dfa375bdb8389214e", sizeof(key));
  for ( j = 0; j < 16; j = i + 1 )
  {
    i = j;
    v2.array = hashed;
    *&v2.len = 0x1000000010LL;
    data = encoding_hex_EncodeToString(v2);
    if ( i >= data.len
      || (v7 = data.str[i],
          s.array = key,
          *&s.len = 0x2000000020LL,
          data_4 = runtime_slicebytetostring(v12, s),
          i >= data_4.len) )
    {
      runtime_panicindex();
    }
    if ( v7 != data_4.str[i] )
      os_Exit(0);
  }
}
```
:::

## Recon
終於有一點像樣的題目出現了，這一題有兩個關卡需要克服
```bash
$ file enter_password
enter_password: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, Go BuildID=3-hVI6nMz0HbfIUMSEzq/TkiA8oRk8FHsCuRXIle2/C1my_KvOIt2KUk44LyQs/-XrwOx7UDhcGGdtF5xpG, with debug_info, not stripped
```
用IDA和gdb跟一下整體的流程
1. 首先他先把我們輸入的flag，丟到main_checkPassword function檢查，而跟了一下gdb發現他是先跟`861836f13e3d627dfa375bdb8389214e`的每一個數值進行xor然後跟enc_flag的字元做比較，而enc_flag是run time的時候需要從memory撈的資料，這就需要慢慢跟然後慢慢看，大概就像下面撈的那樣，反著作就可以得到第一階段的flag
2. 過了第一階段後他還會叫你要再輸入一次另外一個flag，然後會丟到main_ambush function做檢查，他會先把我們輸入的second flag進行md5的hash，然後和`861836f13e3d627dfa375bdb8389214e`進行比對，所以我們要做的事情是推測甚麼樣的字串，他的md5 hash是`861836f13e3d627dfa375bdb8389214e`，這個可以用online tool做到這件事情

## Exploit
1. Script For 1st Stage
    ```python
    enc_flag = [74, 83, 71, 93, 65, 69, 3, 84, 93, 2, 90, 10, 83, 87, 69, 13, 5, 0, 93, 85, 84, 16, 1, 14, 65, 85, 87, 75, 69, 80, 70, 1]
    key = [0x38, 0x36, 0x31, 0x38, 0x33, 0x36, 0x66, 0x31, 0x33, 0x65, 0x33, 0x64, 0x36, 0x32, 0x37, 0x64, 0x66, 0x61, 0x33, 0x37, 0x35, 0x62, 0x64, 0x62, 0x38, 0x33, 0x38, 0x39, 0x32, 0x31, 0x34, 0x65]

    FLAG = []
    for a, b in zip(enc_flag, key):
        FLAG.append(bytes.fromhex(hex(a ^ b)[2:]).decode('utf-8'))

    print("".join(FLAG))
    ```
2. Use [online tool](https://md5.gromweb.com/) to unhash
![](https://hackmd.io/_uploads/HkEBMjztn.png)

3. Conclusion
    ```bash
    $ nc mercury.picoctf.net 4052
    Enter Password: reverseengineericanbarelyforward
    =========================================
    This challenge is interrupted by psociety
    What is the unhashed key?
    goldfish
    Flag is:  picoCTF{p1kap1ka_p1c09a4dd7f3}
    ```