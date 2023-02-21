import os
import re


path = r"F:\SHARED\OBSIDIAN VAULT\10 Wiki\13 Plantations"

old = "100 Zettelkasten/120 MOC/Meteorology"
new = "Meteorology - 20230221103137|Meteorology"


def replace_in_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def replace_in_folder(path, old, new):
    for file in os.listdir(path):
        replace_in_file(os.path.join(path, file), old, new)


if __name__ == "__main__":
    replace_in_folder(path, old, new)