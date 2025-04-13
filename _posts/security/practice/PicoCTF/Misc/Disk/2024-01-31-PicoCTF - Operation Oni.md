---
title: PicoCTF - Operation Oni
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/Disk"
---

# PicoCTF - Operation Oni

## Background
[How to View Your SSH Keys in Linux, macOS and Windows](https://www.techrepublic.com/article/how-to-view-your-ssh-keys-in-linux-macos-and-windows/)

[ISO和IMG有哪些區別](https://docs.pingcode.com/ask/16621.html)
> ### ISO和IMG的區別
> ISO和IMG都是操作系統鏡像文件的擴展名，它們的主要區別在以下幾個方面：
> 1. 來源不同
> ISO文件通常來自光盤鏡像，例如Windows安裝光盤的ISO鏡像文件。而IMG文件可以來自多種渠道，例如從移動設備制造商下載的Android操作系統鏡像文件，或者是從虛擬機軟件中制作的虛擬機磁盤鏡像文件。
> 2. 文件格式不同
> ISO文件使用ISO 9660標準格式，而IMG文件可以使用多種格式，例如RAW、VMDK、VDI等。
> 3. 兼容性不同
> ISO文件在各種操作系統和軟件中都有良好的兼容性，而IMG文件在一些操作系統或軟件中可能存在兼容性問題。
> 4. 使用範圍不同
> ISO文件主要用於制作光盤或者USB啟動盤，用於安裝操作系統或者救援系統等。而IMG文件主要用於移動設備或者虛擬機等環境下的操作系統安裝或備份。
> 總之，ISO和IMG都是操作系統鏡像文件的擴展名，雖然它們在一些方面有類似之處，但在來源、文件格式、兼容性和使用範圍等方面存在差異，應根據具體的需求來選擇使用哪種格式。

## Description
Download this disk image, find the key and log into the remote machine. Note: if you are using the webshell, download and extract the disk image into /tmp not your home directory.
* Download disk image
* Remote machine: `ssh -i key_file -p 59801 ctf-player@saturn.picoctf.net`

## Recon
這一題和DF有關，主要就是分析拿到的img file，可以用Autopsy之類的分析軟體
1. ssh參數
先看launch instance之後出現的連線command，ssh帶有`-i`的參數，根據tldr的常用說明，代表需要給他一個private key file，這也是description中有提到的部分
    ```bash!
    $ tldr ssh
    ...
      - Connect to a remote server using a specific port:
        ssh username@remote_host -p 2222
    ...
    ```
2. Using Autopsy
使用Autopsy分析img file，會面臨到ssh private key在哪裡的問題，根據[^picoctf-forensics-wp-almond-force]的說明通常會放在`~/.ssh/`或是`/root/.ssh/`的folder中，所以我們就可以往這個方向找看看
![](https://hackmd.io/_uploads/S1m4W6R1p.png)
果不其然，的確有一個pub檔案和private key file，直接export出這個檔案，然後夾帶進command就可以了

3. Error
過程中可能會遇到`Permission Too Open`這個error，原因可以看[^ssh-error-permission-too-open]或是看Almond的WP[^picoctf-forensics-wp-almond-force]
    ```bash!
    $ ssh -i ssh-private-key -p 59801 ctf-player@saturn.picoctf.net
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    Permissions 0777 for 'ssh-private-key' are too open.
    It is required that your private key files are NOT accessible by others.
    This private key will be ignored.
    Load key "ssh-private-key": bad permissions
    ctf-player@saturn.picoctf.net's password:
    ```
    簡單來說就是ssh-private-key這個檔案的權限太多了，因為我是直接export到windows的主機，所以預設是777，根據[^ssh-error-permission-too-open]，只需要設定600就可以過了，同時也可以直接看該檔案在img file中的mode是多少
    ![](https://hackmd.io/_uploads/BJYm760JT.png)

## Exploit
```bash!
$ ll
-rwxrwxrwx 1 sbk6401 sbk6401  411 Sep 25 13:59 ssh-private-key
$ chmod 600 ssh-private-key
$ ssh -i ssh-private-key -p 57846 ctf-player@saturn.picoctf.net
Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.19.0-1024-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

ctf-player@challenge:~$ ls
flag.txt
ctf-player@challenge:~$ cat flag.txt
picoCTF{k3y_5l3u7h_af277f77}ctf-player@challenge:~$ Connection to saturn.picoctf.net closed by remote host.
Connection to saturn.picoctf.net closed.
```

Flag: `picoCTF{k3y_5l3u7h_af277f77}`

## Reference
[^ssh-error-permission-too-open]:[ssh "permissions are too open"](https://stackoverflow.com/questions/9270734/ssh-permissions-are-too-open)
[^picoctf-forensics-wp-almond-force]:[ picoGym (picoCTF) Exercise: Operation Oni ](https://youtu.be/fGWdueqArzE?si=Ci0W715ZjQ3vPD8m)