from database.Domain.BaseClass import *


class DiscordUser(Base):
    __tablename__ = 'discord_user'

    discord_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    global_name = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME, nullable=False, default=func.NOW())

    def __repr__(self):
        return (f"DiscordUser(discord_id={self.discord_id}, global_name={self.global_name}, "
                f"created_at={self.created_at})")
