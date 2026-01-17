import os
import re

def fetch_category_in_posts(filepath):
    # 相對路徑從 POSTS_DIR 開始（用於算 category）
    rel_path = os.path.relpath(filepath, POSTS_DIR)
    parts = rel_path.split(os.sep)

    # 最後一段是檔名（移除）
    category_parts = parts[:-1]
    category = "｜".join(category_parts)

    return category

def fetch_date_in_filename(filepath):
    filename = os.path.basename(filepath)
    match = date_prefix_pattern.match(filename)
    if match:
        return match.group(0).rstrip("-")
    return None

def file_io(io: str, new_lines=None):
    with open(filepath, io, encoding="utf-8") as f:
        if io == "r":
            return f.readlines()
        elif io == "w":
            f.writelines(new_lines)
        

if __name__ == "__main__":
    
    POSTS_DIR = "_posts/"
    # POSTS_DIR = "_posts/Test"
    date_prefix_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}-")
    count = 0

    # 確保資料夾存在
    if not os.path.isdir(POSTS_DIR):
        print(f"資料夾不存在: {POSTS_DIR}")
        exit(1)
    

    for dirpath, _, filenames in os.walk(POSTS_DIR):
        for filename in filenames:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(dirpath, filename) # 檔案完整路徑
            date = fetch_date_in_filename(filepath) # fetch date in filename
            category = fetch_category_in_posts(filepath) # fetch category in filepath

            lines = file_io(io="r", new_lines=None)

            # 處理 YAML front matter（以 `---` 區塊為界）
            if lines[0].strip() == "---":
                end_index = 1
                while end_index < len(lines) and lines[end_index].strip() != "---":
                    end_index += 1

                front_matter = lines[1:end_index]
                content = lines[end_index+1:]

                # 檢查是否已有 [category, date]，有的話就取代，否則加入
                category_updated = False
                date_updated = False
                for i, line in enumerate(front_matter):
                    if line.startswith("category:"):
                        origin_category = front_matter[i].split("category:")[1].strip().strip('"')
                        if origin_category != category:
                            front_matter[i] = f'category: "{category}"\n'
                            print(f"更新{filename}的分類: {origin_category} -> {category}")
                        category_updated = True
                    elif line.startswith("date:") and date:
                        origin_date = front_matter[i].split("date:")[1].strip()
                        if origin_date != date:
                            front_matter[i] = f'date: {date}\n'
                            print(f"更新{filename}的日期: {origin_date} -> {date}")
                        date_updated = True
                
                if not category_updated:
                    front_matter.append(f'category: "{category}"\n')
                if not date_updated:
                    front_matter.append(f'date: {date}\n')

                new_lines = ["---\n"] + front_matter + ["---\n"] + content

                file_io(io="w", new_lines=new_lines)
    print(f"✅ 已更新：{count}")