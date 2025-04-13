---
title: Simple Web 0x06(Lab - Image Space 0x03)
tags: [NTUSTWS, CTF, Web]

category: "Security/Course/NTUST WS/Upload"
---

# Simple Web 0x06(Lab - Image Space 0x03)
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:9012

## Background
[file signature](https://en.wikipedia.org/wiki/List_of_file_signatures)

## Source code
:::spoiler
```php!=
 <?php
    if (isset($_GET['source'])) {
        highlight_file(__FILE__);
        exit;
    }
?>
<h1>Image Uploader</h1>
<p>Only supports: jpg, jpeg, png</p>
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
    $extension = strtolower(explode(".", $filename)[1]);

    if (!in_array($extension, ['png', 'jpeg', 'jpg']) !== false) {
        die("Invalid file extension: $extension.");
    }

    if (in_array($_FILES['image_file']['type'], ["image/png", "image/jpeg", "image/jpg"]) === false) {
        die("Invalid file type: " . $_SERVER["CONTENT_TYPE"]);
    }

    list($_, $_, $type) = getimagesize($_FILES['image_file']['tmp_name']);

    if ($type !== IMAGETYPE_JPEG && $type !== IMAGETYPE_PNG) {
        die("Invalid image type.");
    }

    $prefix = bin2hex(random_bytes(8));
    move_uploaded_file($_FILES['image_file']['tmp_name'], "images/${prefix}_${filename}");
    echo "<img src=\"/images/${prefix}_${filename}\">";
?>
```
:::
It has 2 extra constraint must be bypassed. Use `burpsuite` and change valid file signature

## Exploit - bypass `IMAGETYPE` + bypass `$_FILES['image_file']['type']`
1. `HxD` - bypass `IMAGETYPE`
Add valid file signature at the beginning from [wiki page](https://en.wikipedia.org/wiki/List_of_file_signatures)
png: `89 50 4E 47 0D 0A 1A 0A`
jpg: `FF D8 FF DB`
2. `burpsuite` - bypass file type
![](https://i.imgur.com/02Mh97T.png)
3. Then we got shell!!!
payload: `http://h4ck3r.quest:9012/images/353d74c11becb9b1_webshell_valid_filetype.png.php?sh=cat%20../../../../flag`