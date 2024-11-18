from sqlalchemy import BigInteger, Column, DATETIME
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.sql import func

from database.Domain.BaseClass import Base


class DiscordUser(Base):
    __tablename__ = 'discord_user'

    id = Column(BigInteger, autoincrement=True, primary_key=True, nullable=False)
    display_name = Column(VARCHAR(255), nullable=False)
    global_name = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME, nullable=False, default=func.NOW())
