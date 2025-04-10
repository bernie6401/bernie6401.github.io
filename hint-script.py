import os
import re

def convert_hackmd_to_hugo(content):
    # Convert admonitions (info, warning, danger)
    content = re.sub(
        r"::: *(info|warning|danger)\n(.*?)\n:::",
        lambda m: f"{{% hint {m.group(1)} %}}\n{m.group(2)}\n{{% /hint %}}",
        content,
        flags=re.DOTALL
    )

    # Convert spoiler
    content = re.sub(
        r"::: *spoiler *(.*?)\n(.*?)\n:::",
        lambda m: f'{{% details title="{m.group(1).strip()}" open=false %}}\n{m.group(2)}\n{{% /details %}}',
        content,
        flags=re.DOTALL
    )

    # Convert LaTeX display math
    content = re.sub(
        r"\$\$(.*?)\$\$",
        lambda m: f"{{< katex display=true >}}\n{m.group(1)}\n{{< /katex >}}",
        content,
        flags=re.DOTALL
    )

    # Convert LaTeX inline math
    content = re.sub(
        r"\$(.+?)\$",
        lambda m: f"{{< katex >}}{m.group(1)}{{< /katex >}}",
        content
    )

    # Highlight text from ==xxx==
    content = re.sub(r"==(.+?)==", r"<mark>\1</mark>", content)

    return content

# Path to directory containing markdown files
directory = "./demo/content/test/"

for filename in os.listdir(directory):
    if filename.endswith(".md"):
        path = os.path.join(directory, filename)
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
        converted = convert_hackmd_to_hugo(original)
        with open(path, "w", encoding="utf-8") as f:
            f.write(converted)

print("✅ HackMD 語法已轉換為 Hugo Book 相容格式")