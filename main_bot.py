from dotenv import load_dotenv

# Load environment variables before importing any other modules
load_dotenv()

from src.Controller import Controller
from src.Logging.Logger import Logger

logger = Logger("main")

try:
    controller = Controller()
    controller.run()
except Exception as error:
    logger.error("Error while running controller", exc_info=error)

    exit(1)
