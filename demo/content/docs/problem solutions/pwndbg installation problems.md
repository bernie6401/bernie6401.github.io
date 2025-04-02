---
title: pwndbg installation problems
tags: [problem solution]

---

# pwndbg installation problems
## Normal Installation
```bash
$ git clone https://github.com/pwndbg/pwndbg
$ cd pwndbg
$ ./setup.sh
```

## Problem I
```bash!
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 python3-venv : Depends: python3.8-venv (>= 3.8.2-1~) but it is not going to be installed
                Depends: python3 (= 3.8.2-0ubuntu2) but 3.10.4-0ubuntu2 is to be installed
E: Unable to correct problems, you have held broken packages.
```
1. 如果遇到這種的問題，就直接分析setup.sh是crash在哪邊，照理說應該是跟python的版本有關係，想我的狀況是原本安裝python3的version是3.10，而不是3.8，所以最直接的做法是修改setup.sh file，在第23行的地方修改一下，直接指定安裝的版本，另外
    ```bash=22
    # original
    sudo apt-get install -y git gdb gdbserver python3-dev python3-venv python3-pip python3-setuptools libglib2.0-dev libc6-dbg
    ```
    ```bash=22
    # revised
    sudo apt-get install -y git gdb gdbserver python3-dev=3.8.2-0ubuntu2 python3-venv=3.8.2-0ubuntu2 python3-pip python3-setuptools libglib2.0-dev libc6-dbg
    ```
    * 另外如果gdb吃的python版本不是3.8，就需要直接指定，也就是在第172行的地方新增版本
        ```bash=172
        $ PYVER=$(gdb -batch -q --nx -ex 'pi import platform; print(".".join(platform.python_version_tuple()[:2]))')
        $ PYVER="3.8" # 直接指定，上面那行不要刪掉
        ```
        然後安裝python3.8
        ```bash
        $ sudo apt install python3.8
        ```
    * 如果還是不行就強制把python3的版本改成3.8[^alter_python_version_on_ubuntu]
        ```bash
        $ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
        ```
        此時應該會看到`dpkg -l|grep python`中，python3的結果應該是`3.8.2-0ubuntu2`
    
2. 如果都不行，就全部砍掉[^apt_remove_python]，語法如下，理論上應該就沒剩多少了，如果查看python會發現沒有這個command
    ```bash
    $ sudo apt-get remove --auto-remove python3.10
    $ sudo apt-get remove --auto-remove python3.
    $ dpkg -l|grep python
    ```
3. 此時應該就可以正常安裝了`$ ./setup.sh`.

## Problem II
```bash
$ gdb
GNU gdb (Ubuntu 12.0.90-0ubuntu1) 12.0.90
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Traceback (most recent call last):
  File "/home/sbk6401/pwndbg/gdbinit.py", line 68, in <module>
    import pwndbg  # noqa: F401
  File "/home/sbk6401/pwndbg/pwndbg/__init__.py", line 9, in <module>
    import pwndbg.commands
  File "/home/sbk6401/pwndbg/pwndbg/commands/__init__.py", line 17, in <module>
    from pwndbg.heap.ptmalloc import DebugSymsHeap
  File "/home/sbk6401/pwndbg/pwndbg/heap/ptmalloc.py", line 19, in <module>
    import pwndbg.disasm
  File "/home/sbk6401/pwndbg/pwndbg/disasm/__init__.py", line 13, in <module>
    import capstone
  File "/home/sbk6401/pwndbg/.venv/lib/python3.8/site-packages/capstone/__init__.py", line 326, in <module>
    import distutils.sysconfig
ModuleNotFoundError: No module named 'distutils.sysconfig'
Reading symbols from chal...
(No debugging symbols found in chal)
Python Exception <class 'ModuleNotFoundError'>: No module named 'distutils.sysconfig'
(gdb)
```

碰到這個問題的前提是已經安裝好了(setup的部分完成)，那就直接安裝python3-distutils就好了
```bash
$ sudo apt-get install python3-distutils
```

## Problem III
如果是沒有`Pwngdb`的folder的話就直接拿已經安裝好的電腦，然後複製整個資料夾到`~/`就好了

## Problem IV
如果下gdb發現沒有使用任何plugin就要檢查.gdbinit的檔案怎麼寫，例如我的文件有gef和pwndbg，如果要使用其中一種，另外一個就要全部註解，才不會出錯
```bash
# source ~/.gdbinit-gef.py

#### gef
# gef setting
# gef config dereference.max_recursion 2
# gef config context.layout "regs code args source memory stack trace"
# gef config context.nb_lines_backtrace 3
# gef config context.redirect /dev/pts/1

#### pwndbg
source /home/sbk6401/pwndbg/gdbinit.py
source /home/sbk6401/Pwngdb/pwngdb.py
source /home/sbk6401/Pwngdb/angelheap/gdbinit.py

define hook-run
python
import angelheap
angelheap.init_angelheap()
end
end
```
---
到最後安裝的結果就會如下
:::spoiler Complete Result
```bash
$ dpkg -l|grep python
ii  libpython3-dev:amd64                   3.10.4-0ubuntu2                         amd64        header files and a static library for Python (default)
ii  libpython3-stdlib:amd64                3.10.4-0ubuntu2                         amd64        interactive high-level object-oriented language (default python3 version)
ii  libpython3.10:amd64                    3.10.4-3                                amd64        Shared Python runtime library (version 3.10)
ii  libpython3.10-dev:amd64                3.10.4-3                                amd64        Header files and a static library for Python (v3.10)
ii  libpython3.10-minimal:amd64            3.10.4-3                                amd64        Minimal subset of the Python language (version 3.10)
ii  libpython3.10-stdlib:amd64             3.10.4-3                                amd64        Interactive high-level object-oriented language (standard library, version 3.10)
ii  libpython3.8:amd64                     3.8.17-1+jammy1                         amd64        Shared Python runtime library (version 3.8)
ii  libpython3.8-dev:amd64                 3.8.17-1+jammy1                         amd64        Header files and a static library for Python (v3.8)
ii  libpython3.8-minimal:amd64             3.8.17-1+jammy1                         amd64        Minimal subset of the Python language (version 3.8)
ii  libpython3.8-stdlib:amd64              3.8.17-1+jammy1                         amd64        Interactive high-level object-oriented language (standard library, version 3.8)
ii  python-apt-common                      2.3.0ubuntu2                            all          Python interface to libapt-pkg (locales)
rc  python-matplotlib-data                 3.1.2-1ubuntu4                          all          Python based plotting system (data package)
ii  python-pip-whl                         20.0.2-5ubuntu1.9                       all          Python package installer
ii  python3                                3.10.4-0ubuntu2                         amd64        interactive high-level object-oriented language (default python3 version)
ii  python3-apt                            2.3.0ubuntu2                            amd64        Python 3 interface to libapt-pkg
ii  python3-dev                            3.10.4-0ubuntu2                         amd64        header files and a static library for Python (default)
ii  python3-distutils                      3.10.4-0ubuntu1                         all          distutils package for Python 3.x
ii  python3-lib2to3                        3.10.4-0ubuntu1                         all          Interactive high-level object-oriented language (lib2to3)
ii  python3-minimal                        3.10.4-0ubuntu2                         amd64        minimal subset of the Python language (default python3 version)
ii  python3-pip                            20.0.2-5ubuntu1.9                       all          Python package installer
ii  python3-pkg-resources                  59.6.0-1.2                              all          Package Discovery and Resource Access using pkg_resources
ii  python3-setuptools                     59.6.0-1.2                              all          Python3 Distutils Enhancements
ii  python3-wheel                          0.34.2-1ubuntu0.1                       all          built-package format for Python
ii  python3.10                             3.10.4-3                                amd64        Interactive high-level object-oriented language (version 3.10)
ii  python3.10-dev                         3.10.4-3                                amd64        Header files and a static library for Python (v3.10)
ii  python3.10-minimal                     3.10.4-3                                amd64        Minimal subset of the Python language (version 3.10)
ii  python3.8                              3.8.17-1+jammy1                         amd64        Interactive high-level object-oriented language (version 3.8)
ii  python3.8-dev                          3.8.17-1+jammy1                         amd64        Header files and a static library for Python (v3.8)
ii  python3.8-minimal                      3.8.17-1+jammy1                         amd64        Minimal subset of the Python language (version 3.8)
rc  python3.8-venv                         3.8.17-1+jammy1                         amd64        Interactive high-level object-oriented language (pyvenv binary, version 3.8)

$ gdb
GNU gdb (Ubuntu 12.0.90-0ubuntu1) 12.0.90
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
pwndbg: loaded 146 pwndbg commands and 47 shell commands. Type pwndbg [--shell | --all] [filter] for a list.
pwndbg: created $rebase, $ida GDB functions (can be used with print/break)
Reading symbols from chal...
(No debugging symbols found in chal)
------- tip of the day (disable with set show-tips off) -------
Pwndbg context displays where the program branches to thanks to emulating few instructions into the future. You can disable this with set emulate off which may also speed up debugging
pwndbg>
```
:::

## Reference
[^apt_remove_python]:[uninstall_python3](https://gist.github.com/zhensongren/811dcf2471f663ed3148a272f1faa957)
[^alter_python_version_on_ubuntu]:[Installing multiple alternative versions of Python on Ubuntu 20.04](https://towardsdatascience.com/installing-multiple-alternative-versions-of-python-on-ubuntu-20-04-237be5177474)