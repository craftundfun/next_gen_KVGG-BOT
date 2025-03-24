from database.Domain.BaseClass import *
from datetime import date


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

    def __init__(self,
                 discord_id: int,
                 guild_id: int,
                 date: date,
                 online_time: int = 0,
                 stream_time: int = 0,
                 mute_time: int = 0,
                 deaf_time: int = 0,
                 message_count: int = 0,
                 command_count: int = 0, ):
        super().__init__()

        self.discord_id = discord_id
        self.guild_id = guild_id
        self.date = date
        self.online_time = online_time
        self.stream_time = stream_time
        self.mute_time = mute_time
        self.deaf_time = deaf_time
        self.message_count = message_count
        self.command_count = command_count

    def to_dict(self):
        dictionary = {
            "discord_id": str(self.discord_id),
            "guild_id": str(self.guild_id),
            "date": self.date.isoformat(),
            "online_time": int(self.online_time),
            "stream_time": int(self.stream_time),
            "mute_time": int(self.mute_time),
            "deaf_time": int(self.deaf_time),
            "message_count": int(self.message_count),
            "command_count": int(self.command_count),
        }

        return dictionary
