import re
import yaml
import frontmatter


class FrontmatterApi:

    def __init__(self, fs_api):
        self._fs_api = fs_api
        self._yaml_frontmatter_regex = r'^---([\s\S]+?)---'

    def get_yaml_frontmatter(self, file):
        file_content = self._fs_api.read_file(file)
        matches = re.findall(self._yaml_frontmatter_regex, file_content)
        if matches:
            yaml_string = matches[0]
            metadata = yaml.safe_load(yaml_string)
            if 'tags' in metadata and type(metadata['tags']) == str:
                metadata['tags'] = metadata['tags'].split()
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
        yaml_frontmatter = self.get_yaml_frontmatter(file)
        yaml_frontmatter[attr] = value
        self.write_yaml_frontmatter(file, yaml_frontmatter)
