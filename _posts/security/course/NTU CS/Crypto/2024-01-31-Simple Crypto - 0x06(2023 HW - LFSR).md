---
title: Simple Crypto - 0x06(2023 HW - LFSR)
tags: [CTF, Crypto, eductf]

category: "Security/Course/NTU CS/Crypto"
---

# Simple Crypto - 0x06(2023 HW - LFSR)

## Background
* [Python – List XOR](https://www.geeksforgeeks.org/python-list-xor/)
    > ```python
    > from funtools import reduce
    > test_list = [4, 6, 2, 3, 8, 9]
    > res = reduce(lambda x, y: x ^ y, test_list) # The output is 2
    > ```
* [Numpy矩陣乘法，但不是乘法，而是XOR的元素](https://www.qiniu.com/qfans/qnso-67006518#comments)
    > ```python
    > import numpy as np
    > m1 = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    > m2 = np.array([[1, 0, 1], [0, 0, 1], [1, 1, 1]])
    > mr = np.empty((m2.shape[0], m1.shape[1]), dtype = np.int64)
    > for i in range(mr.shape[0]):
    >     for j in range(mr.shape[1]):
    >         mr[i, j] = np.sum(m1[:, j] ^ m2[i, :])
    > print(mr)
    > ```
* [使用 Python 來認識矩陣](https://pyradise.com/使用-python-來認識矩陣-915376207187)
* [[Day07]Learning Numpy - 建立、合併、分割 - CheetSheet for Numpy](https://ithelp.ithome.com.tw/articles/10203624)
* Sage
    ```bash
    $ sudo apt install sagemath -y # wsl/unix base可以直接安裝，如果是windows要下載sage binary，有1.4GB
    $ sage -n # 開起sage notebook，也就是可以用sage kernel運行jupyter
    $ sage <.py/.sage file> # 用sage運行腳本
    $ sage # 直接開啟sage interactive shell
    ```

## Recon
這一題和前面的triLFSR不一樣的地方在於他只有一層的LFSR，但他只會每個70個才會給一個state，換句話說我們只能拿到$S_{71*0+70},\ S_{71*1+70},\ S_{71*2+70},\ S_{71*3+70}...$(從0開始算)，而前面256個拿到的State最後會和flag進行XOR，只有最後70個是最純粹的State

* What we have
我們有的東西就是Companion Matrix，因為題目有給taps，所以可以建出上課提到的矩陣；另外我們還有最後出現的70個State，雖然是每格70個出現一次，換句話說就是$State_{71*256+70},\ State_{71*257+70},\ State_{71*258+70},\ ...State_{71*325+70}$(從0開始算)
* Goal
既然我們知道了State的公式為$s_m = p_0s_0 + p_1s_1 + … + p_{m-1}s_{m-1}$，也就是companion matrix的最後一列$*$那64個initial state就會是新的state，換句話說，繼續往下做，其實就只是把companion matrix多乘幾次，然後還是一樣乘以initial state，然後我們只要取得companion matrix乘完之後的最後一列，就是下一個新的state的特徵，如下圖所示:
![](https://hackmd.io/_uploads/HkwyVkGx6.jpg)

    在Round 0時，companion matrix的最後一列當然就是$S_{64}$的特徵，再往下做，也就是Round 1時，companion matrix的平方後，再取最後一列就是$S_{65}$的特徵，而題目給我們的ouptut[0]以state來說就是第70個(以0來說)，所以companion matrix的7次方，再取最後一列，以此類推，我們陸續算到output[256](這是第一個沒有和flag XOR的bit)，也就是companion matrix的$71*256+7=18183$次方再取最後一列，就是$S_{71*256+70}$的特徵，自此開始，我們就可以開始把這些特徵存起來，存滿64個後，再取反矩陣，乘上原本得到的那64個state，就可以得到一開始的initial state

* 完整的對應關係如下圖
![](https://hackmd.io/_uploads/SJcl-JGep.jpg)

## Exploit
1. 陷阱1: 此題所有的運算接在mod 2底下運算，包含內積和反矩陣，所以需要用sage的語法幫助我們快速算出答案(真的差很多，如果是手刻不用sage，至少要花一小時，但用了sage，只需要10秒，真香啊!!!)
    * 在Modular 2的情況下內積，乘法會對應到AND，而加法對應到XOR，在sage中語法如下
        ```sage
        sage: a = Matrix([[1,1,0],[0,1,0],[0,0,1]])
        sage: b = Matrix([[1,1,1],[1,1,0],[1,1,1]])
        sage: a * b
        [2 2 1]
        [1 1 0]
        [1 1 1]
        sage: a * b % 2
        [0 0 1]
        [1 1 0]
        [1 1 1]
        ```
    * 在sage中要計算modular下的inverse matrix，語法如下
        ```sage
        sage: a = Matrix([[1, 2], [3,4]])
        sage: b = Matrix(IntegerModRing(7), a).inverse()
        sage: b
        [5 1]
        [5 3]
        sage: a * b
        [1 0]
        [0 1]
        ```
2. 陷阱2: 其實也不算陷阱，反正就是要很細心處理每一個state和for loop中的i之間的關係變化，其實上面就有完整演練一遍，只要按圖施工保證成功
3. 陷阱3: 在sage中，如果要表達XOR是用`^^`表示，而非python常見的`^`，因為這在sage中代表次方
4. 小技巧: 如果不知道實作的方式對不對，可以直接用原本題目給的code，寫死已知的initial state，然後把output印出來後照著原本設計的邏輯，看能不能還原initial state
:::spoiler Whole Exploit with Sage
```python
from tqdm import trange
import numpy as np

class LFSR:
    def __init__(self, tap, state):
        self._tap = tap
        self._state = state

    def getbit(self):
        f = sum([self._state[i] for i in self._tap]) & 1
        x = self._state[0]
        self._state = self._state[1:] + [f]
        return x
    
def verification(taps, key):
    randomness = LFSR(taps, key)
    output = []
    for _ in range(256 + 64):
        for __ in range(70):
            randomness.getbit()
        output.append(randomness.getbit())
    
    return output[:256], output[256:]

def get_flag(cipher_flag, output):
    flag = ""
    plaintext_hex = ''
    for idx, i in enumerate(range(len(cipher_flag))):
        flag += str(output[i] ^^ cipher_flag[i])
        if (idx+1) % 8 == 0:
            plaintext_hex += hex(int(flag, 2))[2:]
            flag = ""
    return bytes.fromhex(plaintext_hex).decode("cp437")

if __name__ == '__main__':
    f = [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0]

    # Initialization
    taps = [0, 2, 17, 19, 23, 37, 41, 53]
    init_state_size = 64
    cipher_text_xor_flag, cipher_text = f[:len(f)-70], f[len(f)-70:]
    cipher_text = Matrix(np.array(cipher_text[:init_state_size]).reshape((init_state_size, 1)).tolist())

    # Create companion Matrix
    a = np.eye(init_state_size-1, dtype = int)    # 創造對角矩陣
    b = np.zeros((init_state_size-1, 1), dtype=int) # 創造最左邊全為0的行
    c = np.array([1 if i in taps else 0 for i in range(init_state_size)])   # 創造最後一列的taps
    comp_matrix = Matrix(np.vstack([np.hstack([b, a]), c]).tolist()) # 全部組合起來

    # 做內積的運算
    _comp_matrix = comp_matrix  # _comp_matrix代表會變動的companion matrix
    real_comp_matrix = np.empty(init_state_size, dtype=int)
    count = 256
    arr_merge = True
    for i in trange(71*319+6+1):
        _comp_matrix = comp_matrix * _comp_matrix % 2   # 因為是在mod 2底下處理，所以不是普通的dot運算，乘法對應到AND，加法對應到XOR
        if i == 71 * count + 5:
            real_comp_matrix = np.vstack([real_comp_matrix, _comp_matrix[-1]])
            count += 1

    # 計算在模2情況下的反矩陣
    inv_real_comp_matrix = Matrix(IntegerModRing(2), real_comp_matrix[1:]).inverse()

    # 算出initial state
    init_state = inv_real_comp_matrix * cipher_text % 2
    init_state = list(init_state.numpy().reshape(1, init_state_size)[0])
    print("Initial State = ", init_state)

    output, check = verification(taps, [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1])

    assert list(cipher_text.numpy().reshape(1, 64)[0]) == check

    # 如果assert通過，代表找到正確的initial state然後就可以反算flag
    print(get_flag(cipher_text_xor_flag, output))
```
:::

Flag: `FLAG{Lf5r_15_50_eZZzZzZZZzzZzzz}`