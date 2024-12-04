import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker

from src_bot.Logging.Logger import Logger

logger = Logger("DatabaseConnection")

_engine = create_engine(
    f'mysql+mysqlconnector://{os.getenv("DATABASE_USER")}'
    f':{os.getenv("DATABASE_PASSWORD")}'
    f'@{os.getenv("DATABASE_HOST")}'
    f'/{os.getenv("DATABASE_NAME")}',
    echo=False,
    pool_recycle=60,
    pool_size=5,
    max_overflow=10,
    pool_timeout=5, )
metadata = MetaData()
metadata.reflect(bind=_engine)

SessionFactory = sessionmaker(bind=_engine)


def getSession() -> Session | None:
    try:
        return SessionFactory()
    except Exception as error:
        logger.error(f"Failed to get session: {error}", exc_info=error)

        return None
