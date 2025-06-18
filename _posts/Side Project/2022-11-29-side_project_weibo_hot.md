---
title: side_project_weibo_hot
tags: [Side Project]

category: "Side Project"
---

# side_project_weibo_hot
<!-- more -->

###### tags: `Side Project` `Browser Automation` `Selenium`
:::spoiler
[TOC]
:::

## Side Project Background
* Inspired by Bilingual Podcast is the best podcast channel in Taiwan that introduces interesting news happening around the world. They said they had a problem that they can not get the hot news from Weibo immediately before Xi made it disappear. For instance, Shuai Peng(彭帥) and Zhang Gaoli(張高麗) event. So, I wrote a side project about an automatic web system that can refresh the web page and download it automatically and keep the data safe.


## Installation
```bash
pip install pyautogui
pip install selenium
```


## Some Set-Up
1.	Make sure your web driver is the latest version. You can download it here(https://chromedriver.chromium.org/)
2.	Make sure your desktop is the idle one in your home that you'll not use it for a while.
3.	Make sure your desktop language keyboard is for English.


## Something can solve in the future
* The content data you download may not be the same as the latest because I just verify the hot news title before downloading.(Solved, I refresh the news_list.txt every day and then the page with the same title will download again.)

* Maybe someone can write about the login part that not only needs account and password but the id verification. This is very hard to solve in this system.

* (Solved)Someone can use a more efficient searching Algorithm instead of linear searching and clean up the news list in the file to speed up the searching time. For instance, clean up all titles saved a week ago and always make the list lighter. I used the method that I mentioned above that cleans up the news_list.txt every day and that'll make the searching time more efficient.

* (Solved)When you refresh the page many times, the server will reject the request from your desktop. So I add a file named run.py to solve this problem that used subprocess function independently in a while loop. That can lead the web to close completely and reboot again and again.

* The web driver will shut down when the times up. But that will make the downloading file be aborted. So, maybe someone can add a function to detect whether the download process succeed or not.

* To be continued...

## Update
* Time: 2022-11-29
    * In addition to update chrome driver, I also tried to run the whole program but not work because of the **wrong redirection** of weibo webpage.
The page I expected is shown as below.![weibo page I expect](https://imgur.com/G6p2qEu.png)
But actually, drive got the page as below →
![actual page it shown](https://imgur.com/phlJ6Ov.png)
In order to execute my program with slightly revise, I add these line to login. Refer to [使用Selenium实现微博爬虫：预登录、展开全文、翻页](https://blog.51cto.com/u_9177933/2985943)
        ```python
        wait = WebDriverWait(driver,5)
        time.sleep(60)
        ```
        :writing_hand:**Notes** This program became a semi-automatic features.
        
    * Becasue chrome driver halt with the message `Chrome is being controlled by automated test software`, I refer to (自動化初步-使用pyautogui)[https://ithelp.ithome.com.tw/articles/10267172] and set the code below to solve this problem.
        ```python
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})
        ```