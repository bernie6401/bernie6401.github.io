import os
import re
from datetime import datetime

POSTS_DIR = "myblog/_posts/"
date_prefix_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}-")

# 確保資料夾存在
if not os.path.isdir(POSTS_DIR):
    print(f"資料夾不存在: {POSTS_DIR}")
    exit(1)

for dirpath, _, filenames in os.walk(POSTS_DIR):
    for filename in filenames:
        if not filename.endswith(".md"):
            continue

        # 檔案完整路徑
        filepath = os.path.join(dirpath, filename)

        # 相對路徑從 POSTS_DIR 開始（用於算 category）
        rel_path = os.path.relpath(filepath, POSTS_DIR)
        parts = rel_path.split(os.sep)

        # 最後一段是檔名（移除）
        category_parts = parts[:-1]
        category = " > ".join(category_parts)

        # 讀檔案內容
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 處理 YAML front matter（以 `---` 區塊為界）
        if lines[0].strip() == "---":
            end_index = 1
            while end_index < len(lines) and lines[end_index].strip() != "---":
                end_index += 1

            front_matter = lines[1:end_index]
            content = lines[end_index+1:]

            # 檢查是否已有 category，有的話就取代，否則加入
            updated = False
            for i, line in enumerate(front_matter):
                if line.startswith("category:"):
                    front_matter[i] = f'category: "{category}"\n'
                    updated = True
                    break
            if not updated:
                front_matter.append(f'category: "{category}"\n')
            else:
                continue

            new_lines = ["---\n"] + front_matter + ["---\n"] + content

            # 寫回檔案
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)