import os
import re
import argparse
import yaml


def _get_full_path(path):
    with open("config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f.read())
    return os.path.join(config["vault_path"], path)


def replace_in_file(path, regex, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(regex, new, content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def replace_in_folder(path, regex, new):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            replace_in_file(file_path, regex, new)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replace text in files.')
    parser.add_argument('--path', type=str, help='Path to folder', required=True)
    parser.add_argument('--regex', type=str, help='Regex to replace', required=True)
    parser.add_argument('--new', type=str, help='New text', required=True)
    args = parser.parse_args()

    full_path = _get_full_path(args.path)
    replace_in_folder(full_path, args.old, args.new)
