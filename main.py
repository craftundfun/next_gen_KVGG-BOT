from dotenv import load_dotenv

from src.Controller import Controller

load_dotenv()

try:
    controller = Controller()
    controller.run()
except Exception as error:
    print(f"Error: {error}")
    exit(1)