from database.Domain.BaseClass import *


class History(Base):
    __tablename__ = "history"

    id = Column(BigInteger, primary_key=True)
    discord_id = Column(BigInteger, ForeignKey("discord_users.id"), nullable=False)
    guild_id = Column(BigInteger, ForeignKey("guilds.id"), nullable=False)
    event_id = Column(BigInteger, ForeignKey("events.id"), nullable=False)
    time = Column(TIMESTAMP, nullable=False)
    additional_info = Column(TEXT, nullable=True)

    discord_user = relationship("DiscordUser")
    guild = relationship("Guild")
    event = relationship("Events")
