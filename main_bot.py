from dotenv import load_dotenv

# Load environment variables before importing any other modules
load_dotenv()

from src_bot.Controller import Controller
from src_bot.Logging.Logger import Logger

logger = Logger("main")

try:
    controller = Controller()
    controller.run()
except Exception as error:
    logger.error("Error while running controller", exc_info=error)

    exit(1)
