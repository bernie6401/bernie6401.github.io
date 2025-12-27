import os
import argparse
from datetime import datetime

import requests

def crawl_book_cover(bid, book_cover_file_path):
    # Download book cover image
        book_img_url = (
            f"https://www.books.com.tw/img/"
            f"{bid[0:3]}/{bid[3:6]}/{bid[6:8]}/{bid}.jpg"
        )
        book_img = requests.get(book_img_url)
        
        if book_img.status_code == 200:
            img_dir = "/assets/posts/"
            os.makedirs(img_dir, exist_ok=True)
            with open(book_cover_file_path, "wb") as img_file:
                img_file.write(book_img.content)
            print(f"✅ 已下載書籍封面至：{book_cover_file_path}")
        else:
            print("❌ 無法下載書籍封面圖片。")

def crawl_book_info(books_id):
    # 爬蟲書籍資訊
    import requests
    from bs4 import BeautifulSoup

    books_url = f"https://www.books.com.tw/products/{books_id}"
    response = requests.get(books_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        info = {}

        info_block = soup.find("div", class_="type02_p003")

        if info_block:
            text = ""
            for li in info_block.find_all("li"):
                text += li.get_text(strip=True).replace("新功能介紹", "")


            text = text.split("語言：")[0]
            book_info_list = ["出版日期：", "出版社：", "譯者：", "原文作者：", "作者："]
            info = {"publish_date":"", "publisher":"", "translator":"", "original_author":"", "author":""}

            for item, key in zip(book_info_list, info.keys()):
                # info
                if item in text:
                    info[key] = text.split(item)[-1]
                    text = text.split(item)[0]
        print(info)
    else:
        print("❌ 無法取得書籍資訊，請確認書籍 ID 是否正確。")
    
    return info

def generate_post(file_path):
    # 解析絕對路徑與元件
    file_path = os.path.normpath(file_path)
    dir_path, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)

    if ext != ".md":
        print("❌ 請提供 .md 檔案")
        return

    # 取得 category 路徑（去除 _posts 開頭）
    categories = dir_path.replace("\\", "｜")  # Windows fix
    if categories.startswith("_posts/"):
        categories = categories[len("_posts/"):]
    elif categories.startswith("myblog/_posts/"):
        categories = categories[len("myblog/_posts/"):]

    # 把 path 轉成 a/b/c 格式 category
    category_str = categories.strip("/")

    book_cover_file_name = os.path.splitext(args.file_path.split('/')[-1])[0].replace(" ", "_") + ".jpg"
    book_cover_file_path = os.path.join("/assets/posts/", book_cover_file_name)
    if args.books_id:
        info = crawl_book_info(args.books_id)
        crawl_book_cover(args.books_id, book_cover_file_path)
    else:
        info = {}
    
    # 產生時間與檔名
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    date_full = now.strftime("%Y-%m-%d")
    new_filename = f"{date_str}-{name}.md"
    if not info.get("translator", ""):
        author_info = f'* 作者: {info.get("author", "")}\n* 出版社: {info.get("publisher", "")}\n* 出版日期: {info.get("publish_date", "")}\n'
    elif info.get("original_author", ""):
        author_info = f'* 作者: {info.get("original_author", "")}\n* 出版社: \n* 出版日期: \n* 譯者: {info.get("translator", "")}\n* 譯版出版社: {info.get("publisher", "")}\n* 譯版出版日期: {info.get("publish_date", "")}\n'
    elif info.get("author", ""):
        author_info = f'* 作者: {info.get("author", "")}\n* 出版社: \n* 出版日期: \n* 譯者: {info.get("translator", "")}\n* 譯版出版社: {info.get("publisher", "")}\n* 譯版出版日期: {info.get("publish_date", "")}\n'
    else:
        author_info = f'* 作者: \n* 出版社: \n* 出版日期: \n* 譯者: \n* 譯版出版社: \n* 譯版出版日期: \n'

    author_info += f'\n<img src="{book_cover_file_path}" alt=""width="300">\n'

    # 組成 front matter
    front_matter = f"""---
layout: post
title: "{name}"
date: {date_full}
category: "{category_str}"
tags: []
draft: false
toc: true
comments: true
---

# {name}
"""

    # 寫入檔案
    output_dir = "_posts/" + category_str
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, new_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(front_matter)
        if any(cat in category_str for cat in ["Books Notes", "Test"]):
            f.write(f"{author_info}")
        f.write(f"<!-- more -->\n\n")

    print(f"✅ 已建立：{output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="建立新的 Jekyll Post")
    parser.add_argument("--file_path", required=True, help="範例：a/b/c/d.md")
    parser.add_argument("--books_id", nargs="?", help="博客來書城上的書籍 ID（Optional）")

    args = parser.parse_args()
    generate_post(args.file_path)
