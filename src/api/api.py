import os
import logging
from termcolor import colored
import yaml

from src.api.fs import FSApi
from src.api.backlinks import BacklinksApi
from src.api.frontmatter import FrontmatterApi
from src.colored_formatter import ColoredFormatter


class Api:

    def __init__(self, config_path='config.yaml'):
        if not os.path.exists(config_path):
            raise Exception(f"Config not found: {config_path}")
        self._config_path = config_path

        self._configure_logging()

        self.fs_api = FSApi(self._config_path)
        self.root = self.fs_api.get_vault_path()

        self.backlinks_api = BacklinksApi(self.fs_api)
        self.frontmatter_api = FrontmatterApi(self.fs_api)

        logging.info("API configured")

    def _configure_logging(self):

        time_color = 'cyan'
        formatter = ColoredFormatter(fmt=colored('%(asctime)s', time_color) + ' - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        with open(self._config_path, 'r') as f:
            yaml_metadata = yaml.safe_load(f)
            level_str = yaml_metadata['logging_level'] if 'logging_level' in yaml_metadata else 'INFO'

        logging.basicConfig(level=level_str, handlers=[handler])

        logging.info('Logging configured')
