---
title: PicoCTF - NSA Backdoor
tags: [PicoCTF, CTF, Crypto]

---

# PicoCTF - NSA Backdoor
###### tags: `PicoCTF` `CTF` `Crypto`

## Background
[Baby Step Giant Step - BSGS](https://blog.csdn.net/ACdreamers/article/details/8579511)
> 用来解决如下方程最小正整數解的
> $A^x\equiv B(mod\ C)$，其中$0\le x\lt C$
> 如果$A\ge C, B\ge C$，那麼我們可以先取模，即$A\% = C, B\% = C$，所以在這裡我們只討論$0\le A, B\lt C$的情況。
> 普通的BSGS的步驟是這樣的：
> 1. 首先確定$x$的下限是$0$，上限是$C$，我們令$M=\lceil C\rceil$
> 2. 把$A^0~A^M\ mod\ C$的值存到一个Hash表裡面
> 3. 把$(A^M)^0~(A^M)^M\ mod\ C$的值一一枚舉出來，每枚舉一個就在Hash表裡面尋找是否有一個$val$值滿足$val \cdot (A^M)^i\ mod\ C=B$，如果有則找到答案，否則繼續
> 4. 最終答案就是$i\cdot M+val$的值對應的原來$A$的冪
> 上面是普通Baby Step Giant Step的步驟，比較簡單，只適用為素數的情況。如果為合數呢？

拓展的過程詳見全文

---
[離散對數問題 - pohlig-hellman算法講解](https://blog.csdn.net/oampamp1/article/details/104061969)
> 1. 需要注意的是，pohlig-hellman算法的覆雜度在一般情況下比BSGS高！
因此，使用pohlig-hellman的場合只能是較為特殊的情況，即:$p$是質數，且$p-1$包含的質因子較少&較小。
>2. 和BSGS算法一樣，pohlig-hellman算法也是用於解決離散對數問題（也有很多文獻提到是解決橢圓曲線之類的）。即給定$a,b,p$,求 $a^x \equiv b(mod\ p)$。
>3. 歐拉定理: 若$(a,p)=1$，那麽$a^{φ(p)} \equiv1(mod\ p)······(*)$
>證明略。
>4. 費馬小定理: 如果$p$是質數，那$φ(p)=p-1$。
>
>5. 對於$a^x\equiv b(mod\ p)$，記其原根為$g$，則$a=g^{a_i},b=g^{b_i}$(原根的次冪可以在[1,p-1]中一一對應，故$a_i,b_i$必定存在)，即$g^{a_ix}\equiv g^{b_i}(mod\ p)$，所以$a_ix\equiv b_i(mod\ p-1)$，(因為$g^{p-1}\equiv 1(mod\ p)$，$p−1$是最小循環節，即階)，故利用egcd求出$x$即可。，於是我們的問題就變成了如何求$a_i,b_i$。

之後詳細的步驟詳見原文

## Source code
* output.txt
    ```
    n = 98a3425eee4016a2592706867127e6c52ab2cf8077806f5626095e3afadc73cb4d0e747c5b9bf6234242e9578b12aba5e391e04a5cd2730f6e45d9f0758fb69eb32e0070b9efd3470f6571a8443bae63cd16efcb3e945dc3da1ce46993be4c8b4467ffb4e0525428bb8673ba144b0d36d1c34fe87307d68439070da27a8809551aa6cdf55c39c79bb7b6b7b9c26b45ef79f6c1ebf68033e4beab2d24df66f69dfb7f54d70d3b477fc7b67592cb029dfe6341c591c34a127f84b33626cd117707b69d1ed55f1773e3ba8d26b76f2db95e85de14a6aa1ff3de7fa23ce9f7ebd0e6c18c2fef4bbff47b6bd632d2d767aab7d35bf4d8577e50556626096704f0c425
    c = 8788542cefd7490c9282c06b8d24280d56c6706b996bdf580290cdf2cb90e45efd2ce185fc07d2b916c24b0512d38ca14de0ee608a9d6003f258859bbbed97dad15c1d07410a34fd55cd8305eb43418d38f1ca6e024725b97fd9da701a39c23fe55a13d43b4bf9a3d9ebb44d7fe67bd60beffc29ec27bb4baf05ec5b250bfa68360df0d1379c066297a7878e59d27e68cf6a0da90755450827623e54e4f3d9f280fef53c7620d58decfbd10dd64e9d1d5507b5460603c58f5be70c82e2a8e613d730a950caea4c4389c5fc0521f8207ead5fb26c04eb6d0486fd6fe8d015fdabbda00139b42163acc86ffb30c12988058c6247344c42b8f3cdc984c06f4276f8
    ```
* `gen.py`
    :::spoiler Source Code
    ```python
    #!/usr/bin/python

    from binascii import hexlify
    from gmpy2 import *
    import math
    import os
    import sys

    if sys.version_info < (3, 9):
        math.gcd = gcd
        math.lcm = lcm

    _DEBUG = False

    FLAG  = open('flag.txt').read().strip()
    FLAG  = mpz(hexlify(FLAG.encode()), 16)
    SEED  = mpz(hexlify(os.urandom(32)).decode(), 16)
    STATE = random_state(SEED)

    def get_prime(state, bits):
        return next_prime(mpz_urandomb(state, bits) | (1 << (bits - 1)))

    def get_smooth_prime(state, bits, smoothness=16):
        p = mpz(2)
        p_factors = [p]
        while p.bit_length() < bits - 2 * smoothness:
            factor = get_prime(state, smoothness)
            p_factors.append(factor)
            p *= factor

        bitcnt = (bits - p.bit_length()) // 2

        while True:
            prime1 = get_prime(state, bitcnt)
            prime2 = get_prime(state, bitcnt)
            tmpp = p * prime1 * prime2
            if tmpp.bit_length() < bits:
                bitcnt += 1
                continue
            if tmpp.bit_length() > bits:
                bitcnt -= 1
                continue
            if is_prime(tmpp + 1):
                p_factors.append(prime1)
                p_factors.append(prime2)
                p = tmpp + 1
                break

        p_factors.sort()

        return (p, p_factors)

    while True:
        p, p_factors = get_smooth_prime(STATE, 1024, 16)
        if len(p_factors) != len(set(p_factors)):
            continue
        # Smoothness should be different or some might encounter issues.
        q, q_factors = get_smooth_prime(STATE, 1024, 17)
        if len(q_factors) == len(set(q_factors)):
            factors = p_factors + q_factors
            break

    if _DEBUG:
        import sys
        sys.stderr.write(f'p = {p.digits(16)}\n\n')
        sys.stderr.write(f'p_factors = [\n')
        for factor in p_factors:
            sys.stderr.write(f'    {factor.digits(16)},\n')
        sys.stderr.write(f']\n\n')

        sys.stderr.write(f'q = {q.digits(16)}\n\n')
        sys.stderr.write(f'q_factors = [\n')
        for factor in q_factors:
            sys.stderr.write(f'    {factor.digits(16)},\n')
        sys.stderr.write(f']\n\n')

    n = p * q
    c = pow(3, FLAG, n)

    print(f'n = {n.digits(16)}')
    print(f'c = {c.digits(16)}')
    ```
    :::

## Recon
這一題有點難，應該說觀念很簡單，我也有想到但不知道怎麼實作，簡單來說就是解discrete log的問題，總而言之，這一題和[Very Smooth](https://hackmd.io/@SBK6401/HyTTXZnPh)幾乎一樣，差別在於他把flag當成exponent，i.e. $c=3^{flag}\ mod\ n$，並且提供$n, c$，所以我們要解出flag為多少
## Exploit - Pohlig-Hellman(SageMath)
1. Factor $p$ and $q$
    1. Method 1
        ```python
        from gmpy2 import *
        from Crypto.Util.number import long_to_bytes

        a = 2
        n = 2
        N = "98a3425eee4016a2592706867127e6c52ab2cf8077806f5626095e3afadc73cb4d0e747c5b9bf6234242e9578b12aba5e391e04a5cd2730f6e45d9f0758fb69eb32e0070b9efd3470f6571a8443bae63cd16efcb3e945dc3da1ce46993be4c8b4467ffb4e0525428bb8673ba144b0d36d1c34fe87307d68439070da27a8809551aa6cdf55c39c79bb7b6b7b9c26b45ef79f6c1ebf68033e4beab2d24df66f69dfb7f54d70d3b477fc7b67592cb029dfe6341c591c34a127f84b33626cd117707b69d1ed55f1773e3ba8d26b76f2db95e85de14a6aa1ff3de7fa23ce9f7ebd0e6c18c2fef4bbff47b6bd632d2d767aab7d35bf4d8577e50556626096704f0c425"
        c = "8788542cefd7490c9282c06b8d24280d56c6706b996bdf580290cdf2cb90e45efd2ce185fc07d2b916c24b0512d38ca14de0ee608a9d6003f258859bbbed97dad15c1d07410a34fd55cd8305eb43418d38f1ca6e024725b97fd9da701a39c23fe55a13d43b4bf9a3d9ebb44d7fe67bd60beffc29ec27bb4baf05ec5b250bfa68360df0d1379c066297a7878e59d27e68cf6a0da90755450827623e54e4f3d9f280fef53c7620d58decfbd10dd64e9d1d5507b5460603c58f5be70c82e2a8e613d730a950caea4c4389c5fc0521f8207ead5fb26c04eb6d0486fd6fe8d015fdabbda00139b42163acc86ffb30c12988058c6247344c42b8f3cdc984c06f4276f8"
        c = int(c, 16)
        N = int(N, 16)
        while True:
            a = powmod(a, n, N)
            res = gcd(a-1, N)
            if res != 1 and res != N:
                q = N // res
                print("q = {}\np = {}".format(q, res))
                break
            n += 1
        ```
    3. Method 2
        ```python
        import primefac

        n = 0xd63c7cb032ae4d3a43ecec4999cfa8f8b49aa9c14374e60f3beeb437233e44f988a73101f9b20ffb56454350b1c9032c136142220ded059876ccfde992551db46c27f122cacdd38c86acb844032f8600515aa6ccb7a1d1ac62d04b51b752476d2d6ee9f22d0f933bebdd833a71fd30510479fcc7ba0afb1d4b0a1622cdc2a48341010dffdcfc8d9af45959fb30b692dc2c9e181ac6bcd6a701326e3707fb19b7f9dfe1c522c68f9b0d229d384be1e1c58f72f8df60ca5172a341a7ee81428a064beedd6af7b89cc6079f2b6d3717f0d29330f0a70acca05bf67ab60c2e5cb0b86bfca2c9b8d50d79d24371432a1efb243f3c5f15b377ccc51f6e69bfbf5ecc61
        c = 0x51099773fd2aafd5f84dfe649acbb3558797f58bdc643ac6ee6f0a6fa30031767966316201c36be69241d9d05d0bd181ced13809f57b0c0594f6b29ac74bc7906dae70a2808799feddc71cf5b28401100e5e7e0324b9d8b56e540c725fa4ef87b9e8d0f901630da5f7f181f6d5b4cdc00d5f5c3457674abcb0d0c173f381b92bdfb143c595f024b98b9900410d502c87dfc1633796d640cb5f780fa4b6f0414fb51e34700d9096caf07b36f4dcd3bb5a2d126f60d3a802959d6fadf18f4970756f3099e14fa6386513fb8e6cdda80fdc1c32a10f6cdb197857caf1d7abf3812e3d9dcda106fa87bac382d3e6fc216c55da02a0c45a482550acb2f58bea2cfa03
        q = primefac.pollard_pm1(n)
        p = n//q
        print(f'p = {p}')
        print(f'q = {q}')
        ```
2. Use [SageMath](https://sagecell.sagemath.org/) to address Discrete Log Problem
    ```python
    p = 117635180960139721127318189832610714114593440637486157582828661167364276581210599344857316369131977790468647533227778603367761815400416396281259234299247850289710613080530669849409358755399675041263469367135430665518150110493389671646158566214130516002949975036799297119111385228596853422400303735447298026283
    q = 163800729847029979711295941089800020300275211671661376396219775666688832353701752860857691086339595920419175562271802936423756228938551439950541873798393442729921516031775531740506399414675546114663346731428381174638773512946351966471041847661507898143967764453261943807056370639171597924004988320983393199599
    c = 0x8788542cefd7490c9282c06b8d24280d56c6706b996bdf580290cdf2cb90e45efd2ce185fc07d2b916c24b0512d38ca14de0ee608a9d6003f258859bbbed97dad15c1d07410a34fd55cd8305eb43418d38f1ca6e024725b97fd9da701a39c23fe55a13d43b4bf9a3d9ebb44d7fe67bd60beffc29ec27bb4baf05ec5b250bfa68360df0d1379c066297a7878e59d27e68cf6a0da90755450827623e54e4f3d9f280fef53c7620d58decfbd10dd64e9d1d5507b5460603c58f5be70c82e2a8e613d730a950caea4c4389c5fc0521f8207ead5fb26c04eb6d0486fd6fe8d015fdabbda00139b42163acc86ffb30c12988058c6247344c42b8f3cdc984c06f4276f8
    g = Mod(3,p)
    m = discrete_log(c,g)
    print(hex(m))
    g2 = Mod(3,q)
    m2 = discrete_log(c,g2)
    print(m2)
    print(hex(m2)[2:])
    ```
    * Output
        ```bash
        0x7069636f4354467b6233773472335f30665f63306d7030733174335f6d3064756c315f39396633383833377d
        4028375274964940959020413024799108535910958820283330112174774258028392431441247073675773191542213151242109
        7069636f4354467b6233773472335f30665f63306d7030733174335f6d3064756c315f39396633383833377d
        ```
        
Flag: `picoCTF{b3w4r3_0f_c0mp0s1t3_m0dul1_99f38837}`
## Reference
[pico2022 nsa backdoor](https://youtu.be/pARmkuMg5tk)