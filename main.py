import os
import shutil


def replace_file(path):
    file_name = os.path.basename(path)
    book_title = file_name.split('-')[0].strip()
    isbn = file_name.split('-')[1].strip()
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(f"[[{book_title}]]", f"[[{book_title} - {isbn}]]")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Replaced {path}")

if __name__ == '__main__':
    folder_path = r"F:\SHARED\OBSIDIAN VAULT\10 Wiki\14 References\Goodreads"
    for file in os.listdir(folder_path):
        if file.endswith('.md'):
            replace_file(os.path.join(folder_path, file))
