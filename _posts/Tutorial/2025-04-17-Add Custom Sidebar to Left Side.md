---
layout: post
title: "Add Custom Sidebar to Left Side"
date: 2025-04-17
category: "Tutorial"
tags: [Tutorial]
draft: false
toc: true
comments: true
---

# Add Custom Sidebar to Left Side
因為想要達到類似HackMD的書籤效果，就是在右邊可以有摺疊/展開的書籤，所以找了一個[類似風格的Theme](https://next-sidebar.netlify.app/html/blank.html#)，並且寫一些Liquid Code盡量和他類似，這個語言有點麻煩
<!-- more -->

## Prerequisite
如果可以盡量先熟悉Liquid語法: [Tutorial](https://liquid.bootcss.com/tags/variable/)

## 修改的文件
### `_includes/_layout.html`
這個比較簡單理解，我預計是要寫一個html file，然後把他插在最外圍的頁面，而定義整個網站最外圍的就是`_includes/_layout.html`，我插在main tag中
{% gist dc65e323b171dc290a244673f216d166 %}

### `_includes/_custom/sidebar-post.html`
這個就比較複雜了，我的目標是可以parse三層的folder structure就好，所以當每一層中，每一個file/folder包含`.md`我就直接設定a tag和href，如果沒有代表是folder就繼續往下parse，需要特別注意的是，我在字串比對的時候需要先利用**capture**這個語法，意思是把`leveln.name`轉換成字串(意義不明的語法)
{% raw %}
```html
<aside id="custom-sidebar" class="custom-sidebar">
  <div class="custom-sidebar-inner">
    <div class="custom-sidebar-logo">Post Tree</div>
      <ul class="custom-sidebar-menu">
        {% assign posts = site.posts | sort: "path" %}
        {% assign level1_groups = posts | group_by_exp: "post", "post.path | split: '/' | slice: 1,1 | join: ''" %}
        {% for level1 in level1_groups %}
          <li>
            <details>
              <summary>{{ level1.name }}</summary>
              <ul>
                {% assign level2_groups = level1.items | group_by_exp: "post", "post.path | split: '/' | slice: 2,1 | join: ''" %}
                {% for level2 in level2_groups %}
                  {% capture level2_name %}{{ level2.name }}{% endcapture %}
                  {% if level2_name contains 'md' %}
                    <ul>
                      {% for post in level2.items %}
                        <li><a href="{{ post.url }}">{{ post.title }}</a></li>
                      {% endfor %}
                    </ul>
                  {% else %}
                    <li>
                      <details>
                        <summary>{{ level2.name }}</summary>
                        <ul>
                          {% assign level3_groups = level2.items | group_by_exp: "post", "post.path | split: '/' | slice: 3,1 | join: ''" %}
                          {% for level3 in level3_groups %}
                            {% capture level3_name %}{{ level3.name }}{% endcapture %}
                            {% if level3_name contains '.md' %}
                              <ul>
                                {% for post in level3.items %}
                                  <li><a href="{{ post.url }}">{{ post.title }}</a></li>
                                {% endfor %}
                              </ul>
                            {% else %}
                              {% assign filenames = level3.items | map: "path" | map: "split" | map: "last" %}
                              <li>
                                <details>
                                  <summary>{{ level3.name }}</summary>
                                  <ul>
                                    {% for post in level3.items %}
                                      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
                                    {% endfor %}
                                  </ul>
                                </details>
                              </li>
                            {% endif %}
                          {% endfor %}
                        </ul>
                      </details>
                    </li>
                  {% endif %}
                {% endfor %}
              </ul>
            </details>
          </li>
        {% endfor %}
    </ul>
  </div>
</aside>
```
{% endraw %}

### `_sass/_custom/custom.scss`
這是本來就存在的文件，只不過裡面是空的，就先拿來用，到這一步是相對花時間的，因為要慢慢在前端用DevTools查看比例，而且還要看不同裝置的layout有沒有跑掉
1. 首先，我希望Post Tree這個sidebar可以一直存在於左側，所以和原本sidebar不同的是position和width
    ```css
    .custom-sidebar {
        position: fixed;
        ...
        width: 250px;
        ...
    }
    ```
    其他部分就和原本sidebar差不多
2. 為了要有Indentation的layer效果，所以新增如下
    ```css
    // Indentation for tree level
    .custom-sidebar-menu > li {
        padding-left: 0.5em;
    }
    .custom-sidebar-menu li ul > li {
        padding-left: 1.5em;
    }
    .custom-sidebar-menu li ul li ul > li {
        padding-left: 2.5em;
    }
    ```
3. 特別針對sidebar顯示出來的title以及link做hover的效果以及定義顏色之類k2
    ```css
    .custom-sidebar-menu a {
        color: $gainsboro;
        text-decoration: none;
    }

    .custom-sidebar-menu a:hover {
        color: white;
        background-color: rgba(255, 255, 255, 0.1);
    }

    .custom-sidebar-menu a.active {
        font-weight: bold;
        color: white;
    }
    ```
4. 顯示分類的箭頭，點開detail標籤時，箭頭會右轉90度
    ```css
    // Custom sidebar styles
    details summary {
        cursor: pointer;
        list-style: none;
        position: relative;
    }

    details summary::before {
        content: '›';
        position: absolute;
        right: 0.5rem;
        top: 2px;
        font-size: 1rem;
        transform-origin: center;
        transition: transform 0.2s ease;
    }

    details[open] summary::before {
        transform: rotate(90deg);
    }
    ```
5. 另外像是footer就需要特別注意，因為在`./_common/outline/outline.scss`有特別定義footer的position以及width
    ```css
    .footer {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    min-height: $footer-height;
    }
    ```
    但是這會造成總畫面的寬度超過100%，這樣會變成底下一定會有一個scrollbar，並且右上角也有一些空白的缺口
    ![](/assets/posts/螢幕擷取畫面 2025-04-17 004943.png)
    所以我直接設定.footer的width和position為relative和auto，並且為了不要讓視窗縮小的時候，sidebar擋住content，.main/.header/.footer我都設定margin-left為250px，這個數值和前面第一點是一樣的
    ```css
    // Push main layout next to sidebar
    .footer {
        position: relative;
        width: auto;
    }

    .main,
    .header,
    .footer {
    margin-left: 250px;

    @include tablet() {
        margin-left: 0;
    }

    @include mobile() {
        margin-left: 0;
    }
    }

    .footer,
    .header {
        background: #FFF6E5;
    }
    ```