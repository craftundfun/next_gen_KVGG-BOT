import logging
import logging.handlers
import os
import sys
from logging import Logger as BaseLogger

from src_backend.Logging.CustomFormatters import CustomFormatterFile, CustomFormatterConsole


class Logger(BaseLogger):

    def __init__(self, name: str):
        super().__init__(name)

        filePath = os.getenv("LOG_FILE_BACKEND", "Logs/log.txt")
        directory = os.path.dirname(filePath)

        try:
            testing = os.environ.get("IS_TEST")
        except KeyError:
            testing = "false"

        # isolate if for future additions
        if testing is None:
            testing = "false"

        if testing == "false":
            if not os.path.exists(directory):
                os.makedirs(directory)

            fileHandler = logging.handlers.TimedRotatingFileHandler(filename=filePath,
                                                                    when="midnight",
                                                                    backupCount=int(os.getenv("LOG_BACKUP_COUNT", 5)), )
            fileHandler.setFormatter(CustomFormatterFile())
            fileHandler.setLevel(os.getenv("LOG_LEVEL_FILE", "DEBUG"))

            self.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(CustomFormatterConsole())
        consoleHandler.setLevel(os.getenv("LOG_LEVEL_CONSOLE", "INFO"))

        self.addHandler(consoleHandler)

        logLevel = os.getenv("LOG_LEVEL", "DEBUG")

        self.setLevel(logLevel)
        self.propagate = False
