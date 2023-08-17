from termcolor import colored
import logging


class ColoredFormatter(logging.Formatter):
    LOG_COLORS = {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }

    def format(self, record):
        levelname = record.levelname
        level_color = self.LOG_COLORS.get(levelname, 'white')
        colored_levelname = colored(levelname, color=level_color)
        record.levelname = colored_levelname

        return super().format(record)
