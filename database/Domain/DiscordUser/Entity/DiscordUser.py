from database.Domain.BaseClass import *


class DiscordUser(Base):
    __tablename__ = 'discord_user'

    discord_id = Column(BigInteger, primary_key=True, unique=True)
    display_name = Column(VARCHAR(255), nullable=False)
    global_name = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME, nullable=False, default=func.NOW())
