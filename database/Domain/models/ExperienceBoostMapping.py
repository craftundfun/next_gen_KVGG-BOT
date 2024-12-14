from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.Boost import Boost
    from database.Domain.models.DiscordUser import DiscordUser
    from database.Domain.models.Guild import Guild


class ExperienceBoostMapping(Base):
    __tablename__ = "experience_boost_mapping"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    boost_id = Column(BigInteger, ForeignKey("boost.boost_id"), nullable=False)
    discord_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), nullable=False)
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), nullable=False)
    remaining_time = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    boost: Mapped[Optional["Boost"]] = relationship("Boost")
    discord_user: Mapped[Optional["DiscordUser"]] = relationship("DiscordUser")
    guild: Mapped[Optional["Guild"]] = relationship("Guild")
