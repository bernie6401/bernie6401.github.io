---
title: PicoCTF - m00nwalk
tags: [PicoCTF, CTF, Misc]

category: "Security｜Practice｜PicoCTF｜Misc｜Image Stego"
date: 2023-02-22
---

# PicoCTF - m00nwalk
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [m00nwalk](https://play.picoctf.org/practice/challenge/26?category=4&page=3)

## Description & Hint
Decode this [message](https://jupiter.challenges.picoctf.org/static/fc1edf07742e98a480c6aff7d2546107/message.wav) from the moon.
Hint:
* How did pictures from the moon landing get sent back to Earth?
* What is the CMU mascot?, that might help select a RX option

## Background
[慢掃描電視 - slow-scan television(sstv)](https://zh.wikipedia.org/wiki/%E6%85%A2%E6%89%AB%E6%8F%8F%E7%94%B5%E8%A7%86#%E5%9C%A8%E8%88%AA%E5%A4%A9%E9%A2%86%E5%9F%9F%E7%9A%84%E6%97%A9%E6%9C%9F%E5%BA%94%E7%94%A8)

## Source code

## Exploit - qsstv + 
1. First, I thought it might be a `mp3stego` problem but found nothing. So, I tried to find the write up about this question.
2. Use QSSTV
    ```bash!
    $ sudo apt-get install pavucontrol
    $ sudo apt-get install qsstv
    $ pactl load-module module-null-sink sink_name=virtual-cable
    22
    ```
3. The Setting
* `pavucontrol`
    ```bsh!
    $ pavucontrol # then it should show up a GUI interface
    ```
    ![](https://i.imgur.com/yScUDWN.png)
    ![](https://i.imgur.com/BMQf2CP.png)
    * Note that must set the output from Null(Monitor of Null Output)

* `qsstv`
    ```bash!
    $ qsstv # again, it should show up a GUI interface
    ```
    ![](https://i.imgur.com/R3OYHMi.png)
        * Note that the `Audio Interface` should be `PaulseAudio`
    * Then we can start to record in qsstv and set the command
    ```bash!
    $ paplay -d virtual-cable message.wav
    ```

4. After finish the recording, we'll got a `png` file that contains the flag
* Note that, the sequence of the audio is `message.wmv` $\to$ `pavucontrol` $\to$ `qsstv`. The main job of `pavucontrol` is to manage the audio that we play and send it to the right application(e.g. `qsstv`)


## Reference
[m00nwalk - write up](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/m00nwalk.md)