from datetime import date as datetimeDate

from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.DiscordUser import DiscordUser


class StatusActivity(Base):
    __tablename__ = "status_activity"

    discord_id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, primary_key=True)
    date = Column(Date, primary_key=True)
    online_time = Column(BigInteger, default=0, nullable=False)
    idle_time = Column(BigInteger, default=0, nullable=False)
    dnd_time = Column(BigInteger, default=0, nullable=False)

    discordUser: Mapped[DiscordUser] = relationship("DiscordUser", uselist=False, )

    def __init__(self,
                 discord_id: int,
                 guild_id: int,
                 date: datetimeDate | None = None,
                 online_time: int = 0,
                 idle_time: int = 0,
                 dnd_time: int = 0, ):
        super().__init__()

        self.discord_id = discord_id
        self.guild_id = guild_id

        if date:
            self.date = date

        self.online_time = online_time
        self.idle_time = idle_time
        self.dnd_time = dnd_time
