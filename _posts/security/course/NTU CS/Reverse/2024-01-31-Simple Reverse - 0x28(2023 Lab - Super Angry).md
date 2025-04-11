---
title: Simple Reverse - 0x28(2023 Lab - Super Angry)
tags: [eductf, CTF, Reverse]

category: "Security/Course/NTU CS/Reverse"
---

# Simple Reverse - 0x28(2023 Lab - Super Angry)
## Source code
:::spoiler main function
```cpp
__int64 __fastcall main(int argc, char **argv, char **a3)
{
  __int64 *user_input; // rcx
  __int64 v5; // rdx
  __int64 v6; // rdx
  char output[128]; // [rsp+10h] [rbp-B0h] BYREF
  __int64 user_input_cp[6]; // [rsp+90h] [rbp-30h] BYREF

  user_input_cp[5] = __readfsqword(0x28u);
  if ( argc == 2 )
  {
    user_input = (__int64 *)argv[1];
    v5 = user_input[1];
    user_input_cp[0] = *user_input;
    user_input_cp[1] = v5;
    v6 = user_input[3];
    user_input_cp[2] = user_input[2];
    user_input_cp[3] = v6;
    scramble_fn((__int64)user_input_cp, output, 0x20uLL);
    if ( !memcmp(output, verify_key, 0x80uLL) )
      puts("Correct!");
    else
      puts("Incorrect!");
    return 0LL;
  }
  else
  {
    printf("Usage: %s <input>\n", *argv);
    return 1LL;
  }
}
```
:::

:::spoiler scramble function
```cpp
unsigned __int64 __fastcall scramble_fn(char *user_input, uint32_t *output, unsigned __int64 const_0x20)
{
  unsigned __int64 result; // rax
  int cmd; // [rsp+24h] [rbp-Ch]
  unsigned __int64 i; // [rsp+28h] [rbp-8h]

  cmd = 1;
  memset(output, 0, 4 * const_0x20);            // 從這邊可以看得出來output的大小應該是int或是uint，因為有4 bytes
  for ( i = 0LL; ; ++i )
  {
    result = i;
    if ( i >= const_0x20 )
      break;
    switch ( cmd )
    {
      case 1:
        output[i] = (user_input[i] << 12) + 5308892;
        cmd = 3;
        break;
      case 2:
        output[i] = 4 * (user_input[i] + 1958409);
        cmd = 4;
        break;
      case 3:
        output[i] = user_input[i] + 192731;
        cmd = 5;
        break;
      case 4:
        output[i] = 4 * user_input[i] + 14474785;
        cmd = 1;
        break;
      case 5:
        output[i] = (user_input[i] << 17) + 176044;
        cmd = 6;
        break;
      case 6:
        output[i] = user_input[i] - 3874948;
        cmd = 2;
        break;
      default:
        continue;
    }
  }
  return result;
}
```
:::
## Recon
可以從IDA解析出來的結果得知，這支程式的主要流程是我們執行的時候command多帶一個參數，而這個參數會直接進到scramble_fn做一些操作，最後會再跟verify_key進行memcmp，大略分析一下scramble_fn後發先他是一個偏簡單但我們懶得看得操作，所以可以試看看用angr解看看

angr基本流程:
1. 建立一個project
2. 建立claripy symbol - 以這個lab的例子來說就是建立我們輸入進去的程式的input string
3. 建立初始的state - 以這個lab來說就是我們一開始輸入的input string
4. 有了proj / symbol / initial state之後就要開始讓他跑起來
## Exploit
```python
import angr
import claripy

# 建立一個project
root = 'Reverse/Lab3/Super Angry/'
proj = angr.Project(root + 'super_angry')

# 建立Claripy Symbol
sym_arg = claripy.BVS('sym_arg', 8 * 32) # 就像z3一樣要建立symbol

# 建立初始的state
state = proj.factory.entry_state(args=[proj.filename, sym_arg])
simgr = proj.factory.simulation_manager(state)

# 有了proj/symbol/initial state之後就要開始讓他跑起來
simgr.explore(find = lambda s: b'Correct!' in  s.posix.dumps(1))

if len(simgr.found) > 0:
    print(simgr.found[0].solver.eval(sym_arg, cast_to=bytes))
else:
    print("NONONONO")
    
# b'FLAG{knowing_how_2_angr!}\x00DBUS_S'
```

Flag: `FLAG{knowing_how_2_angr!}`