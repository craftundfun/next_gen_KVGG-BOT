from database.Domain.BaseClass import *


class Statistic(Base):
    __tablename__ = "statistic"

    id = Column(BigInteger, primary_key=True, nullable=False)
    discord_user_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), nullable=False)
    guild_id = Column(BigInteger, ForeignKey("guild.id"), nullable=False)
    online_time = Column(BigInteger, nullable=False, default=0)
    stream_time = Column(BigInteger, nullable=False, default=0)
    mute_time = Column(BigInteger, nullable=False, default=0)
    deaf_time = Column(BigInteger, nullable=False, default=0)
    message_count = Column(BigInteger, nullable=False, default=0)
    command_count = Column(BigInteger, nullable=False, default=0)

    discord_user = relationship("DiscordUser")
    guild = relationship("Guild")
