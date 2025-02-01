from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.DiscordUser import DiscordUser
    from database.Domain.models.Guild import Guild
    from database.Domain.models.Event import Event


class History(Base):
    __tablename__ = "history"

    id = Column(BigInteger, primary_key=True)
    discord_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), nullable=False)
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), nullable=False)
    event_id = Column(BigInteger, ForeignKey("event.id"), nullable=False)
    time = Column(DATETIME, nullable=False, default=func.current_timestamp(6))
    channel_id = Column(BigInteger, nullable=True, default=null())
    additional_info = Column(JSON, nullable=True)

    discord_user: Mapped[Optional["DiscordUser"]] = relationship("DiscordUser")
    guild: Mapped[Optional["Guild"]] = relationship("Guild")
    event: Mapped[Optional["Event"]] = relationship("Event")

    def __repr__(self):
        return (
            f"History(id={self.id}, "
            f"discord_id={self.discord_id}, "
            f"guild_id={self.guild_id}, "
            f"event_id={self.event_id}, "
            f"time={self.time}, "
            f"channel_id={self.channel_id}, "
            f"additional_info={self.additional_info})"
        )
