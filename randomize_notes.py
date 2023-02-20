"""
This script will add a tag to a random subset of notes in a folder.
"""


import os
import re
import random
import yaml

folder_path = r"F:\SHARED\OBSIDIAN VAULT\10 Wiki\12 Notes"  # path to the folder containing the notes
n = 30  # number of random notes to tag
random_tag_name = "wiki/meta/random"  # name of the tag to add

files = os.listdir(folder_path)
random_files = random.sample(files, n)

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
        if random_tag_name in tags:
            tags.remove(random_tag_name)

        if filename in random_files:
            print(f"Adding {random_tag_name} to {filename}...")
            tags.append(random_tag_name)

        tags = [tag.strip() for tag in tags]

        frontmatter["tags"] = tags
        file_content = re.sub(r'---\n(.*?)\n---', f'---\n{yaml.dump(frontmatter)}---', file_content, 1, re.MULTILINE | re.DOTALL)

        with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as file:
            file.write(file_content)
