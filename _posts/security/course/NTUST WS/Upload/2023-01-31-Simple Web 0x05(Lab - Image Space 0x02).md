---
title: Simple Web 0x05(Lab - Image Space 0x02)
tags: [NTUSTWS, CTF, Web]

category: "Security > Course > NTUST WS > Upload"
---

# Simple Web 0x05(Lab - Image Space 0x02)
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:9011

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

    $prefix = bin2hex(random_bytes(8));
    move_uploaded_file($_FILES['image_file']['tmp_name'], "images/${prefix}_${filename}");
    echo "<img src=\"/images/${prefix}_${filename}\">";
?>
```
:::
* Extension checked by white list: `.png`, `.jpeg`, `jpg`
## Exploit - bypass extension
Change the filename to `webshell.png.php` then upload to get shell.