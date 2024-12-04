from datetime import datetime

from database.Domain.BaseClass import *
from database.Domain.DiscordUser.Entity.DiscordUser import DiscordUser


class WebsiteUser(Base):
    __tablename__ = "website_user"

    discord_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), primary_key=True)
    created_at = Column(DATETIME, default=datetime.now(), nullable=False)
    deleted_at = Column(DATETIME, default=None, nullable=True)

    discordUser = relationship("DiscordUser", back_populates="websiteUser", uselist=False)

    relationship(DiscordUser)
