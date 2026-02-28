---
title: PicoCTF - File types
tags: [PicoCTF, CTF, Misc]

category: "Security Practice｜PicoCTF｜Misc｜General"
date: 2023-02-20
---

# PicoCTF - File types
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [File types]()

## Background

### For Shell Script
[Linux MD5](https://blog.gtwang.org/linux/generate-verify-check-files-md5-sha1-checksum-linux/)
[Linux egrep命令](https://www.runoob.com/linux/linux-comm-egrep.html)
[Shell test 命令](https://www.runoob.com/linux/linux-shell-test.html)
> -f 文件名: 如果文件存在且为普通文件则为真

[How to modify $PATH](https://phoenixnap.com/kb/linux-add-to-path)
[touch - time stamp](https://blog.gtwang.org/linux/linux-touch-command-tutorial-examples/)
[What is $$ in bash?](https://unix.stackexchange.com/questions/291570/what-is-in-bash)

### For Compress Command
[Linux 備份檔案操作 cpio 指令教學與範例](https://officeguide.cc/linux-copy-files-to-and-from-archives-cpio-command-tutorial-examples/)
[bzip2 command in Linux](https://www.geeksforgeeks.org/bzip2-command-in-linux-with-examples/)
[Gzip Command in Linux](https://linuxize.com/post/gzip-command-in-linux/)
[Lzip Manual](https://www.nongnu.org/lzip/manual/lzip_manual.html)
[lz4 manual](https://manpages.ubuntu.com/manpages/xenial/man1/lz4.1.html)
[lzma manual](https://manpages.ubuntu.com/manpages/xenial/man1/lzmp.1.html)
[lzop(1) - Linux man page](https://linux.die.net/man/1/lzop)

## Source code
:::spoiler Flag.pdf
```bash=
#!/bin/sh
# This is a shell archive (produced by GNU sharutils 4.15.2).
# To extract the files from this archive, save it to some FILE, remove
# everything before the '#!/bin/sh' line above, then type 'sh FILE'.
#
lock_dir=_sh00046
# Made on 2022-03-15 06:50 UTC by <root@e8647f66bc56>.
# Source directory was '/app'.
#
# Existing files will *not* be overwritten, unless '-c' is specified.
#
# This shar contains:
# length mode       name
# ------ ---------- ------------------------------------------
#   1092 -rw-r--r-- flag
#
MD5SUM=${MD5SUM-md5sum}
f=`${MD5SUM} --version | egrep '^md5sum .*(core|text)utils'`
test -n "${f}" && md5check=true || md5check=false
${md5check} || \
  echo 'Note: not verifying md5sums.  Consider installing GNU coreutils.'
if test "X$1" = "X-c"
then keep_file=''
else keep_file=true
fi
echo=echo
save_IFS="${IFS}"
IFS="${IFS}:"
gettext_dir=
locale_dir=
set_echo=false

for dir in $PATH
do
  if test -f $dir/gettext \
     && ($dir/gettext --version >/dev/null 2>&1)
  then
    case `$dir/gettext --version 2>&1 | sed 1q` in
      *GNU*) gettext_dir=$dir
      set_echo=true
      break ;;
    esac
  fi
done

if ${set_echo}
then
  set_echo=false
  for dir in $PATH
  do
    if test -f $dir/shar \
       && ($dir/shar --print-text-domain-dir >/dev/null 2>&1)
    then
      locale_dir=`$dir/shar --print-text-domain-dir`
      set_echo=true
      break
    fi
  done

  if ${set_echo}
  then
    TEXTDOMAINDIR=$locale_dir
    export TEXTDOMAINDIR
    TEXTDOMAIN=sharutils
    export TEXTDOMAIN
    echo="$gettext_dir/gettext -s"
  fi
fi
IFS="$save_IFS"
if (echo "testing\c"; echo 1,2,3) | grep c >/dev/null
then if (echo -n test; echo 1,2,3) | grep n >/dev/null
     then shar_n= shar_c='
'
     else shar_n=-n shar_c= ; fi
else shar_n= shar_c='\c' ; fi
f=shar-touch.$$
st1=200112312359.59
st2=123123592001.59
st2tr=123123592001.5 # old SysV 14-char limit
st3=1231235901

if   touch -am -t ${st1} ${f} >/dev/null 2>&1 && \
     test ! -f ${st1} && test -f ${f}; then
  shar_touch='touch -am -t $1$2$3$4$5$6.$7 "$8"'

elif touch -am ${st2} ${f} >/dev/null 2>&1 && \
     test ! -f ${st2} && test ! -f ${st2tr} && test -f ${f}; then
  shar_touch='touch -am $3$4$5$6$1$2.$7 "$8"'

elif touch -am ${st3} ${f} >/dev/null 2>&1 && \
     test ! -f ${st3} && test -f ${f}; then
  shar_touch='touch -am $3$4$5$6$2 "$8"'

else
  shar_touch=:
  echo
  ${echo} 'WARNING: not restoring timestamps.  Consider getting and
installing GNU '\''touch'\'', distributed in GNU coreutils...'
  echo
fi
rm -f ${st1} ${st2} ${st2tr} ${st3} ${f}
#
if test ! -d ${lock_dir} ; then :
else ${echo} "lock directory ${lock_dir} exists"
     exit 1
fi
if mkdir ${lock_dir}
then ${echo} "x - created lock directory ${lock_dir}."
else ${echo} "x - failed to create lock directory ${lock_dir}."
     exit 1
fi
# ============= flag ==============
if test -n "${keep_file}" && test -f 'flag'
then
${echo} "x - SKIPPING flag (file already exists)"

else
${echo} "x - extracting flag (text)"
  sed 's/^X//' << 'SHAR_EOF' | uudecode &&
begin 600 flag
M(3QA<F-H/@IF;&%G+R`@("`@("`@("`@,"`@("`@("`@("`@,"`@("`@,"`@
M("`@-C0T("`@("`Q,#(T("`@("`@8`K'<6D`&[RD@0`````!````,&(\-P4`
M``#_`69L86<``$)::#DQ05DF4UG8%@C,```E___[Y[M[G]GO[=^W[_N__^6^
MYJGOD+YKS[D]VU]`>Q]/?;`!&;"0&@:`!H:`T:9-`#3330T:::`!H-'J:``8
MC0:!H,C1HR#1HR,C)ZFFCU-'E'J8T:AR`Q#1B`-`&3330`80:`!B,!,1DT-`
M`#$&1ID9#!,@R::&$PAHR#3"JGZ4R,C1HTT#U&(80#1H`9,C1ZF0Q`9``>H`
M!D````]3$`,F(`T&AHT!`$`-$2N?R0*H(%R04*<D(7$`\"P"6J(/ORS5EV'E
MY1A`\T1>[HJ%R[CD]7UCS7E.#93IHR*#^?R7/$W6*1]HGQ=6EJ_/A$B_2<_G
M5]3/.*(B)V8P\40AS.5X<KE?9IM4'Q<3&PH+K"FJ)I6/1XOFW@W<,00<]B>2
MPX5/>V_P:DLC2^>A1^[>Y#?DS"9KG7[]/=<ASJ7MJ$$R&\`6.9W")P6VS9LD
M.F7L4"\Y$H\1@O$:/N]]<+E+8B9)"'%;)PX-A@F\-3%=ICS(%E2AC+#,!8,<
MZ%O`<_HMM@M%6#]!6"7]`2W:!\.3@RYX$/2&/(\:I$<N@*34)6G+(BNGHY5V
M0T)XU&!)Q5B-(=%VD-NN'6ZZ(BF`XC3PJ\R/QN6:)#XCNK?X%$*H>1Z(HQ>C
M#5HSE`/XJAZ-J?*((R/%CB[DBG"A(;`L$9@`QW$``````````````0``````
M```+``````!44D%)3$52(2$A````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
,````````````````
`
end
SHAR_EOF
  (set 20 22 03 15 06 50 36 'flag'
   eval "${shar_touch}") && \
  chmod 0644 'flag'
if test $? -ne 0
then ${echo} "restore of flag failed"
fi
  if ${md5check}
  then (
       ${MD5SUM} -c >/dev/null 2>&1 || ${echo} 'flag': 'MD5 check failed'
       ) << \SHAR_EOF
b5cc2c5756410f2467168f6d4c468f52  flag
SHAR_EOF

else
test `LC_ALL=C wc -c < 'flag'` -ne 1092 && \
  ${echo} "restoration warning:  size of 'flag' is not 1092"
  fi
fi
if rm -fr ${lock_dir}
then ${echo} "x - removed lock directory ${lock_dir}."
else ${echo} "x - failed to remove lock directory ${lock_dir}."
     exit 1
fi
exit 0
```
:::

## Exploit - Google and Uncompress
:::spoiler whole process
```bash!
# shell script
$ file Flag.pdf  
Flag.pdf: POSIX shell script, ASCII text executable, with CRLF line terminators
$ mv Flag.pdf Flag.sh

# debug
$ chmod 777 Flag.sh
$ ./Flag.sh 
zsh: ./Flag.sh: bad interpreter: /bin/sh^M: no such file or directory
$ sed -i -e 's/\r$//' Flag.sh
$ ./Flag.sh 
x - created lock directory _sh00046.
x - extracting flag (text)
x - removed lock directory _sh00046.

# ar
$ ls
Flag.pdf  Flag.sh  flag
$ file flag 
flag: current ar archive
$ mv flag flag.ar
$ ar -x flag.ar  

# cpio
$ ls
Flag.pdf  Flag.sh  flag  flag.ar
$ file flag 
flag: cpio archive
$ mv flag flag.cpio   
$ cpio -iv < flag.cpio
flag
2 blocks

# bzip2
$ ls
Flag.pdf  Flag.sh  flag  flag.ar  flag.cpio
$ file flag 
flag: bzip2 compressed data, block size = 900k
$ mv flag flag.bz2    
$ bzip2 -d flag.bz2   

# gzip
$ ls
Flag.pdf  Flag.sh  flag  flag.ar  flag.cpio
$ file flag 
flag: gzip compressed data, was "flag", last modified: Tue Mar 15 06:50:36 2022, from Unix, original size modulo 2^32 329
$ mv flag flag.gz
$ gzip -d flag.gz

# lzip
$ ls
Flag.pdf  Flag.sh  flag  flag.ar  flag.cpio
$ file flag 
flag: lzip compressed data, version: 1
$ mv flag flag.lz
$ lzip -d flag.lz

# lz4
$ ls
Flag.pdf  Flag.sh  flag  flag.ar  flag.cpio
$ file flag 
flag: LZ4 compressed data (v1.4+)
$ mv flag flag.lz4    
$ lz4 -d flag.lz4
Decoding file flag
flag.lz4   : decoded 266 bytes

# lzma
$ ls
Flag.pdf  Flag.sh  flag  flag.ar  flag.cpio  flag.lz4
$ file flag 
flag: LZMA compressed data, non-streamed, size 255
$ mv flag flag.lzma
$lzma -d flag.lzma

# lzop
$ ls
Flag.pdf  Flag.sh  flag  flag.ar  flag.cpio  flag.lz4
$ file flag 
flag: lzop compressed data - version 1.040, LZO1X-1, os: Unix
$ mv flag flag.lzo
$ lzop -d flag.lzo

# lzip
$ ls
Flag.pdf  Flag.sh  flag  flag.ar  flag.cpio  flag.lz4  flag.lzo
$ file flag 
flag: lzip compressed data, version: 1
$ mv flag flag.lz
$ lzip -d flag.lz

# xz
$ls
Flag.pdf  Flag.sh  flag  flag.ar  flag.cpio  flag.lz4  flag.lzo
$file flag 
flag: XZ compressed data
$mv flag flag.xz
 ~/CTF/P/M/File_types
$ xz -d flag.xz  

# Completely Uncompressed
$ls
Flag.pdf  Flag.sh  flag  flag.ar  flag.cpio  flag.lz4  flag.lzo
$file flag 
flag: ASCII text
$cat flag | xxd -r -p
picoCTF{f1len@m3_m@n1pul@t10n_f0r_0b2cur17y_3c79c5ba}
```
:::

## Reference
[Bash script – "/bin/bash^M: bad interpreter: No such file or directory"](https://stackoverflow.com/questions/14219092/bash-script-bin-bashm-bad-interpreter-no-such-file-or-directory)
[Convert Hex to ASCII](https://www.baeldung.com/linux/character-hex-to-ascii)