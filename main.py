import os
import shutil


def move_file(path):
    lines = []
    with open(path, 'r', encoding='latin-1') as f:
        lines = f.readlines()

    for line in lines:
        if "tags: zettelkasten/moc" in line:
            new_path = 'N:\\Obsidian Vault\\100 Zettelkasten\\120 MOC\\' + path.split('\\')[-1]
            shutil.move(path, new_path)
            print(new_path)

if __name__ == '__main__':
    folder_path = r"N:\Obsidian Vault\100 Zettelkasten"
    for file in os.listdir(folder_path):
        if file.endswith('.md'):
            move_file(os.path.join(folder_path, file))
