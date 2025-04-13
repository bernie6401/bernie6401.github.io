---
title: CrewCTF - OhPHP
tags: [CTF, CrewCTF, Reverse]

category: "Security/Practice/CrewCTF/Reverse"
---

# CrewCTF - OhPHP
## Background
* [PHP - substr()](https://www.wibibi.com/info.php?tid=96)
    :::spoiler 
    > `substr( $string , $start , $length )`
    > `$strting` 是原始的字串，`$start` 是要開始擷取的位置，`$length` 則為要截取的字串長度，要注要的是 `$start` 與 $length 都必須為數字才有作用，可以是正整數，也可以是負整數，以下提供幾個範例參考。
    :::
* [PHP - strstr()](https://www.runoob.com/php/func-string-strstr.html)
    :::spoiler 
    > 查找 "world" 在 "Hello world!" 中是否存在，如果是，返回該字符串及後面剩餘部分
    > ```php
    > <?php
    >   echo strstr("Hello world!","world");  // 輸出 world!
    > ?>
    > ```
    :::
* [PHP - strrev()](https://www.runoob.com/php/func-string-strrev.html)
    :::spoiler 
    > 反轉字符串 "Hello World!"：
    > ```php
    > <?php
    >     echo strrev("Hello world!"); // 輸出!dlroW olleH 
    > ?>
    > ```
    :::
* [PHP  strnatcmp()](https://www.w3school.com.cn/php/func_string_strnatcmp.asp)
    :::spoiler 
    > 使用"自然"算法來比較兩個字符串（區分大小寫）：
    > ```php
    > <?php
    > echo strnatcmp("2Hello world!","10Hello world!"); // 輸出-1
    > echo "<br>";
    > echo strnatcmp("10Hello world!","2Hello world!"); // 輸出+1
    > ?>
    > ```
    > strnatcmp() 函數使用一種"自然"算法來比較兩個字符串。
    > 在自然算法中，數字 2 小於數字 10。在計算機排序中，10 小於 2，這是因為 10 中的第一個數字小於 2。
    :::
* [PHP - crc32()](https://www.w3schools.com/php/func_string_crc32.asp)
    :::spoiler
    > ```php
    >  <?php
    >  $str = crc32("Hello World!"); // Output: 472456355
    >  printf("%u\n",$str);
    >  ?> 
    >  ```
    :::
* [PHP - srand()](https://www.w3school.com.cn/php/func_math_srand.asp)
* [PHP - strpos()](https://www.w3school.com.cn/php/func_string_strpos.asp)
    :::spoiler
    > 查找 "php" 在字符串中第一次出現的位置：
    > ```php
    > <?php
    > echo strpos("You love php, I love php too!","php"); // Output: 9
    > ?>
    > ```
    :::
* [PHP - array_sum()](https://www.wibibi.com/info.php?tid=183)
    :::spoiler
    > array_sum 這個函式用來統計陣列 Array 中的數值總數，並回傳統計值，如果陣列內的數值為整數，array_sum 傳回統計值將為整數，若陣列內數值為浮點數，則 array_sum 可能會傳回整數或浮點數。
    > ```php
    > <?php
    > 　$a = array(2, 3, 4);
    > 　$b = array("a" => 1.2, "b" => 2.0, "c" => 3.3);
    > 　echo array_sum($a); // Output: 9
    > 　echo array_sum($b); // Output: 6.5
    > ?>
    > ```
    :::
* [PHP - pack()](https://www.w3school.com.cn/php/func_misc_pack.asp)
    :::spoiler
    > pack() 函數把數據裝入一個二進制字符串。詳細的格式可以看原網頁
    > ```php
    > <?php
    > echo pack("C3",80,72,80);
    > ?>
    > ```
    :::
* [PHP - Arrays](https://www.w3schools.com/php/php_arrays.asp)
* [PHP使用SHA256、SHA512等演算法的寫法](https://blog.longwin.com.tw/2015/10/php-sha256-sha512-hash-algorithm-2015/)
    :::spoiler
    > ```php
    >     <?php
    >         echo hash('sha256', 'abc');
    >         echo hash('sha512', 'abc');
    >         // md5, sha1.. 等等也都可以用此寫法
    >         echo hash('md5', 'abc');
    >         echo hash('sha1', 'abc');
    >     ?>
    > ```
    :::
* [PHP - base64_decode()](https://www.php.net/manual/en/function.base64-decode.php)
    :::spoiler
    > ```php
    > <?php
    > $str = 'VGhpcyBpcyBhbiBlbmNvZGVkIHN0cmluZw==';
    > echo base64_decode($str); // Output: This is an encoded string
    > ?>
    > ```
    :::

## Source Code
詳細的source code請參考[HackMD筆記](https://hackmd.io/@SBK6401/SJJk_NnKh)

## Recon
這一題很複雜也需要很多的步驟
## Exploit
1. 先利用別人的腳本把PHP fuck轉換回原本的code
    :::spoiler Script
    ```csharp
    using System;
    using System.IO;
    using System.Text.RegularExpressions;

    class Proj
    {
        // Fixes obfuscation pattern of the form ('['^'(').(')'^']')
        public static string RemoveParanthesisPattern(string data)
        {
            string pattern = @"\(('.'\^)+'.'\)"; // ('['^':')

            Regex regex = new Regex(pattern);
            MatchCollection matches = regex.Matches(data);

            int found = 0;
            foreach (Match match in matches)
            {
                // Console.WriteLine(match);
                // Console.WriteLine("----------------------------");

                // Removing the first two characters ('
                string tmp = match.ToString().Remove(0, 1).Remove(0, 1);
                // Removing the last two characters ')
                tmp = tmp.Remove(tmp.Length - 2, 1).Remove(tmp.Length - 2, 1);
                tmp = tmp.Replace("'^'", "\x01");

                int val = 0;
                foreach (var x in tmp.Split('\x01', StringSplitOptions.None))
                {
                    val ^= char.Parse(x);
                }

                data = data.Replace(match.ToString(), ((char)val).ToString());
                found += 1;
            }

            Console.WriteLine($"RemoveParanthesisPattern: Total Matches Found: {found}");
            return data;
        }

        // Fixes names of the form s.t.r.s.t.r --> strstr
        public static string FixDottedNames(string data, string pattern = "")
        {
            // XXX: Use this pattern if something breaks
            // string pattern = @"\((([a-z])\.)+[a-z]\)";
            pattern = pattern == "" ? @"\((([a-z0-9_])\.)+[a-z]\)" : pattern;

            Regex regex = new Regex(pattern);
            MatchCollection matches = regex.Matches(data);

            int found = 0;
            foreach (Match match in matches)
            {
                string tmp = match.ToString();
                if (tmp.StartsWith("("))
                {
                    tmp = tmp.Remove(tmp.Length - 1, 1).Remove(0, 1);
                }
                tmp = tmp.Replace(".", "");

                data = data.Replace(match.ToString(), tmp);
                found += 1;
            }

            Console.WriteLine($"FixDottedNames: Total Matches Found: {found}");
            return data;
        }

        static void Main(string[] args)
        {
            string filename = "obfuscated.php";
            string fileData = File.ReadAllText(filename);

            fileData = RemoveParanthesisPattern(fileData);
            fileData = FixDottedNames(fileData);

            // Step3
            fileData = fileData.Replace(@"''.abs(strstr('','.'))", "'0'");

            // Step4
            fileData = RemoveParanthesisPattern(fileData);

            fileData = FixDottedNames(fileData);
            fileData = FixDottedNames(fileData, @"(([a-z0-9A-Z_])\.)+[a-z0-9A-Z]");

            fileData = fileData.Replace(".'0'.", "0");

            File.WriteAllText("deobfuscated.php", "<?php\n" + fileData);

        }
    }
    ```
    :::
    
    :::spoiler Result
    ```php
    <?php
    (in_array(count(get_included_files()),[1])?(strcmp(php_sapi_name(),cli)?printf(Use. .php.-.cli. .to. .run. .the. .challenge.!.
    ):printf(gzinflate(base64_decode(1dTBDYAgDAXQe6fgaC8O4DDdfwyhVGmhbaKe./.BfQfF8gAQFKz8aRh0JEJY0qIIenINTBEY3qNNVUAfuXzIGitJVqpiBa4yp2U8ZKtKmANzewbaqG2lrAGbNWslOvgD52lULNLfgY9ZiZtdxCsLJ3.+.Q./.2RVuOxji0jyl9aJfrZLJzxhgtS65TWS66wdr7fYzRFtvc./.wU9Wpn6BQGc))).define(F,readline(Flag.':'. )).(strcmp(strlen(constant(F)),41)?printf(Nope.!.
    ):(in_array(substr(constant(F),'0',5),[crew.{])?(strstr(strrev((crc32)(substr(constant(F),5,4))),7607349263)?(strnatcmp(A../.k,substr(constant(F),5,4)^substr(constant(F),9,4))?printf(Nope. .xor.!.
    ):srand(31337).define(D,openssl_decrypt(wCX3NcMho0BZO0SxG2kHxA.=.=,aes.-.128.-.cbc,substr(constant(F),'0',16),2,pack(L.*,rand(),rand(),rand(),rand()))).(in_array(array_sum([ctype_print(constant(D)),strpos(substr(constant(F),15,17),constant(D))]),[2])?(strcmp(base64_encode(hash(sha256,substr(constant(F),'0',32))^substr(constant(F),32)),BwdRVwUHBQVF)?printf(Nope.!.
    ):printf(Congratulations.','. .this. .is. .the. .right. .flag.!.
    )):printf(Nope.!.
    ))):printf(Nope.!.
    )):printf(Nope.!.
    )))):printf(Nope.!.
    ));
    ?>
    ```
    :::
    我另外把這坨東西弄的比較好讀一點
    :::spoiler Beautiful Result
    ```php=
    <?php
    (in_array(count(get_included_files()),[1])?
        (
            strcmp(php_sapi_name(),cli)?
            printf(Use php-cli to run the challenge!):
            printf(gzinflate(base64_decode(1dTBDYAgDAXQe6fgaC8O4DDdfwyhVGmhbaKe/BfQfF8gAQFKz8aRh0JEJY0qIIenINTBEY3qNNVUAfuXzIGitJVqpiBa4yp2U8ZKtKmANzewbaqG2lrAGbNWslOvgD52lULNLfgY9ZiZtdxCsLJ3+Q/2RVuOxji0jyl9aJfrZLJzxhgtS65TWS66wdr7fYzRFtvc/wU9Wpn6BQGc)))
            define(F,readline(Flag':' ))
            (
                strcmp(strlen(constant(F)),41)?
                printf(Nope!):
                (
                    in_array(substr(constant(F),'0',5),[crew{])?
                    (
                        strstr(strrev((crc32)(substr(constant(F),5,4))),7607349263)?
                        (
                            strnatcmp(A/k,substr(constant(F),5,4)^substr(constant(F),9,4))?
                            printf(Nope xor!):
                            srand(31337)
                            define(D,openssl_decrypt(wCX3NcMho0BZO0SxG2kHxA==,aes-128-cbc,substr(constant(F),'0',16),2,pack(L*,rand(),rand(),rand(),rand())))
                            (
                                in_array(array_sum([ctype_print(constant(D)),strpos(substr(constant(F),15,17),constant(D))]),[2])?
                                (strcmp(base64_encode(hash(sha256,substr(constant(F),'0',32))^substr(constant(F),32)),BwdRVwUHBQVF)?
                                printf(Nope!):
                                printf(Congratulations',' this is the right flag!)):
                                printf(Nope!)
                            )
                        ):
                        printf(Nope!)
                    ):
                    printf(Nope!)
                )
            )
        ):
        printf(Nope!)
    );
    ?>
    ```
    :::

2. 依照上面的background reference慢慢分析
    * 首先第五行的printf不是很重要，他只是印出題目logo
        :::spoiler
        ![](https://hackmd.io/_uploads/HkCOpC3th.png)
        :::
    * 第12行開始就是flag的驗證，前五個字元是==crew{==
    * 第14行就是把我們輸入的flag從第五個字元開始算四個字元，先進行crc32的運算，然後在反轉string，然後看是不是等於`7607349263`，所以先reverse回去成正常的字串，然後用github上人家寫的crc32 unhash腳本[^crc32_tool]轉換有可能的字串，可以看到結果有幾種，不過因為這邊只有取4 bytes代表答案是==php_==
        ```bash!
        $ ./psysh
        > strrev(7607349263)
        = "3629437067"
        $ python crc32.py reverse 3629437067
        4 bytes: php_ {0x70, 0x68, 0x70, 0x5f}
        verification checksum: 0xd854d08b (OK)
        6 bytes: Jhj4VW (OK)
        6 bytes: KtdYLZ (OK)
        6 bytes: Lmcgfq (OK)
        6 bytes: Nlw5W4 (OK)
        6 bytes: OpyXM9 (OK)
        6 bytes: PNLKv5 (OK)
        6 bytes: TJQJwV (OK)
        6 bytes: WjZ94F (OK)
        6 bytes: ZENzKX (OK)
        6 bytes: apUQJ2 (OK)
        6 bytes: bmOnaz (OK)
        6 bytes: etHPKQ (OK)
        6 bytes: tEbsLS (OK)
        6 bytes: v4JPxF (OK)
        6 bytes: yjv03M (OK)
        6 bytes: yv9l2Y (OK)
        ```
    * 第17行他先把剛剛得到的`php_`和後面的四個字元做xor，並比對`A/k`，所以我們就把這幾個東西轉換成hex，再xor就好了
        ```python
        >>> bytes.fromhex('{:x}'.format(0x411b2F6B ^ 0x7068705F)).decode('utf-8')
        '1s_4'
        ```
    * 第20行比較複雜，他先固定rand的seed，然後用openssl_decrypt解密一串密文，並和我們輸入的flag前16個字元做比較，但剛剛我們得到的flag只有到`crew{php_1s_4`共13個字元，代表我們要爆破剩下三個字元，所以我寫了一個php script和python script去擷取可能的結果
        :::spoiler php script
        ```php!
        <?php
        $encryption = "wCX3NcMho0BZO0SxG2kHxA==";
        $ciphering = "AES-128-CBC";
        $decryption_key_ord = "crew{php_1s_4";
        $options = 2;
        $str=array('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_');
        for ($x = 0; $x <= 36; $x++)
        {
            for ($y = 0; $y <= 36; $y++)
            {
                for ($z = 0; $z <= 36; $z++)
                {
                    srand(31337);
                    $decryption_key = $decryption_key_ord.$str[$x].$str[$y].$str[$z];
                    // echo $decryption_key;
                    $decryption_iv = pack("L*",rand(),rand(),rand(),rand());
                    $decryption=openssl_decrypt ($encryption, $ciphering, $decryption_key, $options, $decryption_iv);
                    echo $str[$x].$str[$y].$str[$z]. " is " . $decryption. "\n";
                }
            }
        }
        ?>
        ```
        :::

        :::spoiler python script
        ```python
        import string

        candidate = string.ascii_lowercase + string.digits + "_ "
        def check_characters(string):
            for char in string:
                if char not in candidate:
                    return False
            return True

        f = open("./result.txt", "rb").read().splitlines()#D:/Download/Trash

        for i in range(len(f)):
            try:
                tmp = f[i].decode()
                if check_characters(tmp):
                    print(f[i].decode())
            except:
                pass
        ```
        :::
        ```bash
        $ php exp.php > result.txt
        $ python exp.py
        ...
        _l4 is ngu4ge_0f_m4g1c_
        ```
        在print出來的東西當中有一個特別長，那就是我們要找的三個字元和解密出來的東西，所以目前為止的flag是==crew{php_1s_4_l4ngu4ge_0f_m4g1c_==
    * 最後就是第22行的部分，他就是把`crew{php_1s_4_l4ngu4ge_0f_m4g1c_`進行SHA256和最後剩下的部分做XOR，再把結果進行base64，和`BwdRVwUHBQVF`比較(不知道為甚麼一樣的操作用python會失敗，我想應該是因為php有特別的操作?!)
        ```bash
        $ ./psysh
        > echo hash('sha256',"crew{php_1s_4_l4ngu4ge_0f_m4g1c_") ^ base64_decode("BwdRVwUHBQVF")
        5b0e7b6a}
        ```
    

Flag: `crew{php_1s_4_l4ngu4ge_0f_m4g1c_5b0e7b6a}`
## Reference
[^crc32_tool]:[crc32 Tool](https://github.com/theonlypwner/crc32)