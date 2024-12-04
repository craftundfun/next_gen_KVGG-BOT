import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = (f'mysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}'
                               f'@{os.getenv("DATABASE_HOST")}/{os.getenv("DATABASE_NAME")}')

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)

    PRODUCTION = bool(int(os.getenv("PRODUCTION", 0)))

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    FRONTEND_URL = os.getenv("FRONTEND_URL")
