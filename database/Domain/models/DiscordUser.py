from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.WebsiteUser import WebsiteUser


class DiscordUser(Base):
    __tablename__ = 'discord_user'

    discord_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    global_name = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=func.utc_timestamp(6))
    profile_picture = Column(TEXT)

    websiteUser: Mapped[Optional["WebsiteUser"]] = relationship("WebsiteUser",
                                                                back_populates="discordUser",
                                                                uselist=False, )

    def __repr__(self):
        return (f"DiscordUser(discord_id={self.discord_id}, global_name={self.global_name}, "
                f"created_at={self.created_at})")

    def as_dict(self):
        return {
            "discord_id": self.discord_id,
            "global_name": self.global_name,
            "created_at": self.created_at,
            "profile_picture": self.profile_picture,
        }
