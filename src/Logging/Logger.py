import logging
import logging.handlers
import os
import sys
from logging import Logger as BaseLogger

from src.Logging.CustomFormatters import CustomFormatterConsole, CustomFormatterFile


class Logger(BaseLogger):

    def __init__(self, name: str):
        super().__init__(name)

        filePath = os.getenv("LOG_FILE", "Logs/log.txt")
        directory = os.path.dirname(filePath)

        if not os.path.exists(directory):
            os.makedirs(directory)

        fileHandler = logging.handlers.TimedRotatingFileHandler(filename=filePath,
                                                                when="midnight",
                                                                backupCount=int(os.getenv("LOG_BACKUP_COUNT", 5)), )
        fileHandler.setFormatter(CustomFormatterFile())

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(CustomFormatterConsole())

        self.addHandler(fileHandler)
        self.addHandler(consoleHandler)

        logLevel = os.getenv("LOG_LEVEL")

        if not logLevel:
            logLevel = "DEBUG"

            self.warning("No log level found in .env file. Using default log level DEBUG")

        self.setLevel(logLevel)
        self.propagate = False
