import logging
import re

import yaml


class FrontmatterApi:
    def __init__(self, fs_api):
        self._fs_api = fs_api
        self._yaml_frontmatter_regex = r"^---([\s\S]+?)---"

    def get_yaml_frontmatter(self, file):
        file_content = self._fs_api.read_file(file)
        matches = re.findall(self._yaml_frontmatter_regex, file_content)
        if matches:
            yaml_string = matches[0]
            metadata = yaml.safe_load(yaml_string)
            if "tags" in metadata and isinstance(metadata["tags"], str):
                metadata["tags"] = metadata["tags"].split()
            return metadata

    def write_yaml_frontmatter(self, file, yaml_dict):
        file_content = self._fs_api.read_file(file)
        new_yaml_string = yaml.safe_dump(yaml_dict).strip()
        matches = re.findall(self._yaml_frontmatter_regex, file_content)
        if matches:
            yaml_string = matches[0].strip()
            new_content = file_content.replace(yaml_string, new_yaml_string)
        else:
            new_content = f"---\n{new_yaml_string}\n---\n{file_content}"

        self._fs_api.write_file(file, new_content)

    def update_yaml_frontmatter(self, file, attr, value):
        logging.info(f"Updating {attr} in frontmatter of {file} to {value}")
        yaml_frontmatter = self.get_yaml_frontmatter(file)
        yaml_frontmatter[attr] = value
        self.write_yaml_frontmatter(file, yaml_frontmatter)

    def get_yaml_value_from_str(self, yaml_str):
        return yaml.safe_load(yaml_str)

    def remove_yaml_attr(self, file, attr):
        yaml_frontmatter = self.get_yaml_frontmatter(file)
        if attr in yaml_frontmatter:
            del yaml_frontmatter[attr]
            self.write_yaml_frontmatter(file, yaml_frontmatter)
        else:
            logging.warning(f"Attribute {attr} not found in frontmatter of {file}")
