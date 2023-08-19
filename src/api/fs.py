import logging
import os
import re

import yaml


class FSApi:
    def __init__(self, config_path):
        self._config_path = config_path
        self._root = None

    def isdir(self, path):
        path = self.format_path(path)
        return os.path.isdir(path)

    def isfile(self, path):
        path = self.format_path(path)
        return os.path.isfile(path)

    def path_is_in_vault(self, path):
        path = self.format_path(path)
        return path.startswith(self._root)

    def get_vault_path(self):
        with open(self._config_path, "r", encoding="latin-1") as f:
            config = yaml.safe_load(f.read())

        vault_path = config["vault_path"]
        if os.path.exists(vault_path):
            logging.info(f"Got vault path: {vault_path}")
            self._root = vault_path
            return vault_path
        raise Exception(f"Can't find vault at {vault_path}")

    def read_file(self, file_path, encoding="latin-1"):
        file_path = self.format_path(file_path)

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{file_path} is not a file")

        with open(file_path, "r", encoding=encoding) as f:
            logging.debug(f"Reading {file_path}")
            return f.read()

    def listdir(self, dir_path, recursive=False):
        dir_path = self.format_path(dir_path)

        if not os.path.isdir(dir_path):
            raise Exception(f"{dir_path} is not a directory")

        logging.debug(f"Listing {dir_path}")

        if recursive:
            files_ = []
            for root, _, files in os.walk(dir_path):
                for file in files:
                    files_.append(os.path.join(root, file))
            return [file for file in files_ if file.endswith(".md")]

        return [
            os.path.join(dir_path, file)
            for file in os.listdir(dir_path)
            if file.endswith(".md")
        ]

    def write_file(self, file_path, content, encoding="latin-1"):
        file_path = self.format_path(file_path)

        if os.path.isfile(file_path):
            logging.debug(f"Overwriting {file_path}")

        with open(file_path, "w", encoding=encoding) as f:
            logging.debug(f"Writing to {file_path}")
            f.write(content)

    def replace_in_file(self, file_path, regex, new):
        file_path = self.format_path(file_path)

        content = self.read_file(file_path)
        new_content = re.sub(regex, new, content)
        self.write_file(file_path, new_content)

    def replace_in_dir(self, dir_path, regex, new, recursive=False):
        dir_path = self.format_path(dir_path)

        files = self.listdir(dir_path, recursive)
        for file in files:
            logging.debug(f"Replacing {file}")
            self.replace_in_file(file, regex, new)

    def format_path(self, path):
        if not os.path.isabs(path):
            path = os.path.join(self._root, path)
        return os.path.normpath(path)
