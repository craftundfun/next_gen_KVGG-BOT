from database.Domain.BaseClass import *


class Statistic(Base):
    __tablename__ = "statistic"

    discord_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), primary_key=True, nullable=False)
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    online_time = Column(BigInteger, nullable=False, default=0)
    stream_time = Column(BigInteger, nullable=False, default=0)
    mute_time = Column(BigInteger, nullable=False, default=0)
    deaf_time = Column(BigInteger, nullable=False, default=0)
    message_count = Column(BigInteger, nullable=False, default=0)
    command_count = Column(BigInteger, nullable=False, default=0)

    discord_user = relationship("DiscordUser")
    guild = relationship("Guild")

    def to_dict(self):
        dictionary = {
            "discord_id": str(self.discord_id),
            "guild_id": str(self.guild_id),
            "date": self.date.isoformat(),
            "online_time": self.online_time,
            "stream_time": self.stream_time,
            "mute_time": self.mute_time,
            "deaf_time": self.deaf_time,
            "message_count": self.message_count,
            "command_count": self.command_count,
        }

        return json.dumps(dictionary, default=str)
