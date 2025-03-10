from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.DiscordUser import DiscordUser


class WebsiteUser(Base):
    __tablename__ = "website_user"

    discord_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), primary_key=True)
    created_at = Column(DATETIME, server_default=func.utc_timestamp(6), nullable=False)
    deleted_at = Column(DATETIME, nullable=True)
    email = Column(VARCHAR(255), nullable=True)
    refresh_token = Column(TEXT, nullable=True)

    discordUser: Mapped[Optional["DiscordUser"]] = relationship("DiscordUser",
                                                                back_populates="websiteUser",
                                                                uselist=False, )

    relationship("DiscordUser")

    def __init__(self,
                 discord_id: int,
                 created_at: datetime | None = None,
                 email: str | None = None,
                 refresh_token: str | None = None):
        super().__init__()

        self.discord_id = discord_id
        self.created_at = created_at
        self.email = email
        self.refresh_token = refresh_token

    # noinspection PyUnresolvedReferences
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
