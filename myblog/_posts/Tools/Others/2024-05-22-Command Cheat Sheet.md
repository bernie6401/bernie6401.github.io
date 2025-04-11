---
title: Command Cheat Sheet
tags: [Tools]

---

# Command Cheat Sheet
## Python 基本用語
* Bytes $\to$ Hex
    ```python
    >>> example_str = b'\x17\x10\x06Ar\xe4G\xc9\xb5\xd7y\xbc'
    >>> example_str.hex()
    '1710064172e447c9b5d779bc'
    ```

* Hex $\to$ String
    ```python
    >>> bytes.fromhex('68656c6c6f').decode('utf-8')
    'hello'
    >>> # or
    >>> import binascii
    >>> binascii.unhexlify('68656c6c6f')
    b'hello"
    
    >>> # or
    >>> import codecs
    >>> decode_hex = codecs.getdecoder("hex_codec")
    >>> decode_hex(s)[0]
    b'hello'
    ```
    
* String $\to$ Hex
    ```python
    >>> str= 'linuxhint'.encode('utf-8')
    >>> str.hex()
    '6c696e757868696e74'
    ```

* Hex(String Type) $\to$ Decimal
    ```python
    >>> a = '123456'
    >>> int(a, 16)
    1193046
    ```

* Decimal $\to$ Hex
    ```python
    >>> a = 1234
    >>> hex(a)
    '0x4d2'
    ```
    
* Hex $\to$ Binary
    ```python
    >>> bin(int('abc', 16))[2:].zfill(8)
    '101010111100'
    ```

* String $\to$ Binary
    :::info
    if you'd like to do this transformation, 1st conversion is better
    :::
    ```python
    # string to hex to binary
    >>> bin(int('I love CNS'.encode('utf-8').hex(), 16))[2:].zfill(8)
    '1001001001000000110110001101111011101100110010100100000010000110100111001010011'
    >>> ''.join(format(ord(x), 'b') for x in 'I love CNS')
    '10010011000001101100110111111101101100101100000100001110011101010011'
    ```

* Byte $\to$ String
    ```python
    >>> b'abc\n'.decode('utf-8')
    'abc\n'
    ```

* Binary $\to$ Hex
    ```python
    >>> hex(int('010110', 2))
    '0x16'
    >>> hex(int('0000010010001101', 2))
    '0x48d'
    ```

* Binary $\to$ Hex $\to$ String
    ```python
    def binToHexa(n):
        bnum = int(n)
        temp = 0
        mul = 1
        count = 1
        hexaDeciNum = ['0'] * 100
        i = 0
        while bnum != 0:
            rem = bnum % 10
            temp = temp + (rem*mul)
            if count % 4 == 0:
                if temp < 10:
                    hexaDeciNum[i] = chr(temp+48)
                else:
                    hexaDeciNum[i] = chr(temp+55)
                mul = 1
                temp = 0
                count = 1
                i = i+1
            else:
                mul = mul*2
                count = count+1
            bnum = int(bnum/10)
        if count != 1:
            hexaDeciNum[i] = chr(temp+48)
        if count == 1:
            i = i-1
        hex_string = ''
        while i >= 0:
            hex_string += hexaDeciNum[i]
            i = i-1
        if hex_string == '':
            hex_string = '00'
        return hex_string
    
    plaintext_hex = binToHexa(plaintext_bin).encode().hex() 
    print(bytes.fromhex(plaintext_hex).decode())
    ```

* Decimal(int type) $\to$ Hex(String type)
    ```python
    >>> '{0:0>2x}'.format(0)
    '00'
    >>> '{0:0>2x}'.format(255)
    'ff'
    >>> '{:x}'.format(290275030195850039473456618367455885069965748851278076756743720446703314517401359267322769037469251445384426639837648598397)
    '7069636f4354467b6d347962335f54683073655f6d337335346733735f3472335f646966757272656e745f313737323733357d'
    ```

* String(`str` type) $\iff$ Decimal
    ```python!
    >>> chr(97)
    'a'
    >>> ord('a')
    97
    ```
* Decimal $\to$ Binary
    ```python!
    >>> bin(10)
    '0b1010'
    ```
* Decimal $\to$ Bytes Type
    ```python
    >>> bytes([10])
    b'\n'
    >>> bytes([70])
    b'F'
    ```
    
* Array $\to$ List
    ```python!
    >>> import numpy as np
    >>> a = np.array([1,2,3])
    >>> a.tolist()
    [1, 2, 3]
    ```
---
## Python 組合技
* XOR Two Decimal
    ```python
    >>> from itertools import cycle
    >>> def hex_xor(s1, s2):
    ...    b = bytearray()
    ...    for c1, c2 in zip(bytes.fromhex(s1), cycle(bytes.fromhex(s2))):
    ...        b.append(c1 ^ c2)
    ...    return b.hex()
    >>> s1 = 'aaab'
    >>> s2 = 'ccbc'
    >>> hex_xor(s1, s2)
    '6617'
    ```
* Decimal $\to$ Ascii String
    ```python
    >>> tmp = 4028375274964940959047587304025089628177332141172593013450629550958369516176531641246900741346661851279741
    >>> bytes.fromhex('{:x}'.format(tmp)).decode('utf-8')
    'picoCTF{p0ll4rd_f4ct0r1z4at10n_FTW_7c8625a1}'
    ```
    
## Python 酷酷的寫法
* string倒續輸出
    ```python
    >>> "galf"[::-1]
    'flag'
    ```
* 取2的補數(取有號數的負號)
    ```python
    >>> import ctypes
    >>> a = 0x17c7cc6e
    >>> ctypes.c_int32(a).value
    398969966
    >>> b = 0xc158a854
    >>> ctypes.c_int32(b).value
    -1051154348
    ```

## Linux 奇技淫巧語法
* 設定英文+數字的亂碼 - [Linux - tr語法](https://www.runoob.com/linux/linux-comm-tr.html)
    `$ tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 16`
* 計算行數 - [Linux 使用 wc 指令計算字數、行數教學與範例](https://blog.gtwang.org/linux/linux-wc-command-tutorial-examples/)
    ```bash
    $ cat document.xml | wc -l
    10
    ```
* 透過搜尋特定字串找尋哪一個file含有相關字串 - [CyberDefenders: Spotlight](https://forensicskween.com/ctf/cyberdefenders/spotlight/#)
    ```bash
    $ grep -i -r '{specific strings}' *
    # grep -i -r 'eno' *
    ```
* sort - [Linux 的 sort 排序指令教學與常用範例整理](https://blog.gtwang.org/linux/linux-sort-command-tutorial-and-examples/)
    ```bash
    # 倒序
    $ ls -l | sort -r
    ```
* uniq - [Linux 的 uniq 指令教學與範例：刪除重複文字行、去除相同的內容](https://blog.gtwang.org/linux/linux-uniq-command-tutorial/)
* cut - [Linux 的 cut 擷取部份字元、欄位指令教學與常用範例整理](https://blog.gtwang.org/linux/linux-cut-command-tutorial-and-examples/)
    ```bash
    # 用key word切分，再用-f選出要顯示哪一塊
    $ cut -d {key word} -f {number}    # cut -d '"' -f 6
    ```
* diff - [Linux diff 命令](https://www.runoob.com/linux/linux-comm-diff.html)
    ```bash
    $ diff log2013.log log2014.log  -y -W 50
    2013-01                 2013-01
    2013-02                 2013-02
    2013-03               | 2014-03
    2013-04                 2013-04
    2013-05                 2013-05
    2013-06                 2013-06
    2013-07                 2013-07
    2013-08               | 2013-07
    2013-09                 2013-09
    2013-10                 2013-10
                          > 2013-11
                          > 2013-12
    ```
    `-y`或`--side-by-side`: 以並列的方式顯示文件的異同之處</br>
    `-W<寬度>`或`--width<寬度>`: 在使用`-y`參數時，指定欄寬</br>
    `|`表示前後2個文件內容有不同</br>
    `<`表示後面文件比前面文件少了1行內容</br>
    `>`表示後面文件比前面文件多了1行內容
    