import logging
import logging.handlers
import os
import sys
from logging import Logger as BaseLogger

from src_bot.Logging.CustomFormatters import CustomFormatterConsole, CustomFormatterFile


class Logger(BaseLogger):

    def __init__(self, name: str):
        super().__init__(name)

        filePath = os.getenv("LOG_FILE_BOT", "Logs/log.txt")
        directory = os.path.dirname(filePath)

        if not os.path.exists(directory):
            os.makedirs(directory)

        fileHandler = logging.handlers.TimedRotatingFileHandler(filename=filePath,
                                                                when="midnight",
                                                                backupCount=int(os.getenv("LOG_BACKUP_COUNT", 5)), )
        fileHandler.setFormatter(CustomFormatterFile())
        fileHandler.setLevel(os.getenv("LOG_LEVEL_FILE", "DEBUG"))

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(CustomFormatterConsole())
        consoleHandler.setLevel(os.getenv("LOG_LEVEL_CONSOLE", "INFO"))

        self.addHandler(fileHandler)
        self.addHandler(consoleHandler)

        logLevel = os.getenv("LOG_LEVEL", "DEBUG")

        self.setLevel(logLevel)
        self.propagate = False
