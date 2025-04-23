from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.DiscordUser import DiscordUser
    from database.Domain.models.ActivityMapping import ActivityMapping
    from database.Domain.models.Event import Event
    from database.Domain.models.Guild import Guild


class ActivityHistory(Base):
    __tablename__ = "activity_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    discord_id = Column(BigInteger, ForeignKey('discord_user.discord_id'), nullable=False)
    guild_id = Column(BigInteger, ForeignKey('guild.guild_id'), nullable=False)
    primary_activity_id = Column(BigInteger, ForeignKey('activity.id'), nullable=False)
    event_id = Column(BigInteger, ForeignKey('event.id'), nullable=False)
    time = Column(DATETIME, nullable=False, server_default=func.utc_timestamp(6))

    discordUser: Mapped["DiscordUser"] = relationship("DiscordUser", uselist=False)
    activityMapping: Mapped["ActivityMapping"] = relationship("Activity", uselist=False)
    event: Mapped["Event"] = relationship("Event", uselist=False)
    guild: Mapped["Guild"] = relationship("Guild", uselist=False)

    def __init__(self,
                 discord_id: int,
                 guild_id: int,
                 primary_activity_id: int,
                 event_id: int,
                 time: datetime | None = None,
                 id: int | None = None, ):
        super().__init__()

        self.discord_id = discord_id
        self.guild_id = guild_id
        self.primary_activity_id = primary_activity_id
        self.event_id = event_id

        if time is not None:
            self.time = time

        if id is not None:
            self.id = id
