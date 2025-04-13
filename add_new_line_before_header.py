import os
import re

def process_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    add_excerpt = False
    for i, line in enumerate(lines):
        stripped_line = line.lstrip()

        # 判斷是不是 ##、###、#### 開頭，並且不是 > 開頭的 blockquote
        if re.match(r'^(#{2,4})\s', stripped_line):
            # 如果前一行不是空行，就補一個空行
            if i > 0 and lines[i - 1].strip() != '':
                new_lines.append('\n')

        new_lines.append(line)

        # if re.match(r'^(#)\s', stripped_line) and not add_excerpt:
        #     # 如果前一行不是空行，就補一個空行
        #     if i > 0 and lines[i + 1].strip() != '<!-- more -->':
        #         new_lines.append('<!-- more -->\n')
        #         add_excerpt = True

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def walk_markdown_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(dirpath, filename)
                print(f"🔧 Processing: {filepath}")
                process_markdown_file(filepath)

# 使用範例：修改你要處理的資料夾
walk_markdown_files('_posts')
