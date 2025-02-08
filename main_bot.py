from dotenv import load_dotenv
import os, time

# Load environment variables before importing any other modules
load_dotenv()

# set global timezone to UTC
os.environ["TZ"] = "UTC"
time.tzset()

from src_bot.Controller import Controller
from src_bot.Logging.Logger import Logger

logger = Logger("main")

try:
    controller = Controller()
    controller.run()
except Exception as error:
    logger.error("Error while running controller", exc_info=error)

    exit(1)
