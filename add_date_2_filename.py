import os
import re
from datetime import datetime

# 修改這裡成你存放文章的資料夾
POSTS_DIR = "_posts/"

# 確保資料夾存在
if not os.path.isdir(POSTS_DIR):
    print(f"資料夾不存在: {POSTS_DIR}")
    exit(1)

# 正規表達式：跳過已經有日期開頭的檔名
date_prefix_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}-")

for dirpath, dirnames, filenames in os.walk(POSTS_DIR):
    for filename in filenames:
        if not filename.endswith(".md"):
            continue

        if date_prefix_pattern.match(filename):
            # 已有日期前綴，跳過
            continue

        filepath = os.path.join(dirpath, filename)
        mtime = os.path.getmtime(filepath)
        date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

        new_filename = f"{date_str}-{filename}"
        new_filepath = os.path.join(dirpath, new_filename)

        print(f"🔄 Renaming: {filename} → {new_filename}")
        os.rename(filepath, new_filepath)
