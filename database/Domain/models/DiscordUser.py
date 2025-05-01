from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.WebsiteUser import WebsiteUser


class DiscordUser(Base):
    __tablename__ = 'discord_user'

    discord_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    global_name = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=func.utc_timestamp(6))

    websiteUser: Mapped[Optional["WebsiteUser"]] = relationship("WebsiteUser",
                                                                back_populates="discordUser",
                                                                uselist=False, )

    def __init__(self, discord_id: int, global_name: str, created_at: datetime | None = None):
        super().__init__()

        self.discord_id = discord_id
        self.global_name = global_name

        if created_at is not None:
            self.created_at = created_at

    def __repr__(self):
        return (f"DiscordUser(discord_id={self.discord_id}, global_name={self.global_name}, "
                f"created_at={self.created_at})")

    def to_dict(self):
        return {
            # str because JavaScript can't handle BigInteger
            "discord_id": str(self.discord_id),
            "global_name": self.global_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
