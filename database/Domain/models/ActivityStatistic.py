from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.DiscordUser import DiscordUser
    from database.Domain.models.Guild import Guild
    from database.Domain.models.Activity import Activity


class ActivityStatistic(Base):
    __tablename__ = "activity_statistic"

    discord_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), primary_key=True)
    activity_id = Column(BigInteger, ForeignKey("activity.id"), primary_key=True)
    date = Column(Date, primary_key=True)
    time = Column(BigInteger, nullable=False, server_default="0")

    discordUser: Mapped[Optional["DiscordUser"]] = relationship("DiscordUser")
    guild: Mapped[Optional["Guild"]] = relationship("Guild")
    activity: Mapped[Optional["Activity"]] = relationship("Activity")

    def __init__(self, discord_id: int, guild_id: int, activity_id: int, date: datetime.date, time: int = 0):
        super().__init__()

        self.discord_id = discord_id
        self.guild_id = guild_id
        self.activity_id = activity_id
        self.date = date
        self.time = time
