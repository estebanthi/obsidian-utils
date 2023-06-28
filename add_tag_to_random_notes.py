"""
This script will add a tag to a random subset of notes in a folder.
"""


import os
import re
import random
import yaml
import argparse


with open("config.yaml", 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)


vault_path = config["vault_path"]


def get_random_files(folder_path, n):
    files = os.listdir(folder_path)
    return random.sample(files, n)


def add_tag_to_files(folder_path, files, tag):
    for filename in files:
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            file_content = file.read()

            frontmatter = re.findall(r'---\n(.*?)\n---', file_content, re.MULTILINE | re.DOTALL)
            if frontmatter:
                frontmatter = frontmatter[0]  # get the first match (there should only be one)
                frontmatter = yaml.safe_load(frontmatter)

            tags = frontmatter.get("tags", []) or []
            if isinstance(tags, str):
                tags = tags.split(",")  # because I usually use a comma-separated string instead of a list
            if tag in tags:
                tags.remove(tag)

            if filename in files:
                print(f"Adding {tag} to {filename}...")
                tags.append(tag)

            tags = [tag.strip() for tag in tags]

            frontmatter["tags"] = tags
            file_content = re.sub(r'---\n(.*?)\n---', f'---\n{yaml.dump(frontmatter)}---', file_content, 1, re.MULTILINE | re.DOTALL)

            with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as file:
                file.write(file_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a tag to a random subset of notes in a folder.")
    parser.add_argument("--path", help="Path to the folder containing the notes to randomize", required=True)
    parser.add_argument("--n", help="Number of random notes to tag", type=int, required=True)
    parser.add_argument("--tag", help="Tag to add", required=True)
    args = parser.parse_args()

    notes_path = os.path.join(vault_path, args.notes_path)
    files = get_random_files(notes_path, args.n)
    add_tag_to_files(notes_path, files, args.tag)
