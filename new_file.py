import os
import argparse
from datetime import datetime

def generate_post(file_path):
    # 解析絕對路徑與元件
    file_path = os.path.normpath(file_path)
    dir_path, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)

    if ext != ".md":
        print("❌ 請提供 .md 檔案")
        return

    # 取得 category 路徑（去除 _posts 開頭）
    categories = dir_path.replace("\\", "/")  # Windows fix
    if categories.startswith("_posts/"):
        categories = categories[len("_posts/"):]
    elif categories.startswith("myblog/_posts/"):
        categories = categories[len("myblog/_posts/"):]

    # 把 path 轉成 a/b/c 格式 category
    category_str = categories.strip("/")

    # 產生時間與檔名
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    date_full = now.strftime("%Y-%m-%d")
    new_filename = f"{date_str}-{name}.md"

    # 組成 front matter
    front_matter = f"""---
layout: post
title: "{name}"
date: {date_full}
categories: "{category_str}"
tags: []
draft: false
toc: true
comments: true
---

# {name}
<!--more-->

"""

    # 寫入檔案
    output_dir = "_posts/" + category_str
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, new_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(front_matter)

    print(f"✅ 已建立：{output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="建立新的 Jekyll Post")
    parser.add_argument("--file_path", required=True, help="範例：a/b/c/d.md")

    args = parser.parse_args()
    generate_post(args.file_path)
