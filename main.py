import os
import yaml
import shutil


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), 'config.yml')) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    obsidian_vault_path = config['obsidian_vault_path']
    obsidian_vault_path = os.path.expanduser(obsidian_vault_path)

    # count the number of .md files in the vault and subfolders
    md_files = []
    for root, dirs, files in os.walk(obsidian_vault_path):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))

    print(f'Found {len(md_files)} .md files in the vault and subfolders')
