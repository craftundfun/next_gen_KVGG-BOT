from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.DiscordUser import DiscordUser


class WebsiteUser(Base):
    __tablename__ = "website_user"

    discord_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), primary_key=True)
    created_at = Column(DATETIME, default=datetime.now(), nullable=False)
    email = Column(VARCHAR(255), nullable=True)

    discordUser: Mapped[Optional["DiscordUser"]] = relationship("DiscordUser",
                                                                back_populates="websiteUser",
                                                                uselist=False, )

    relationship("DiscordUser")

    def as_dict(self) -> dict:
        return {
            "discord_id": self.discord_id,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at,
            "email": self.email,
        }
