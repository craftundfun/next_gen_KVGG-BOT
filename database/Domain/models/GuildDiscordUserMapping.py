from database.Domain.BaseClass import *


class GuildDiscordUserMapping(Base):
    __tablename__ = "guild_discord_user_mapping"

    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), primary_key=True, nullable=False)
    discord_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), primary_key=True, nullable=False)
    display_name = Column(VARCHAR(255), nullable=False)
    profile_picture = Column(TEXT, nullable=True)
    joined_at = Column(DATETIME, nullable=False)
    left_at = Column(DATETIME, nullable=True)

    guild = relationship("Guild")
    discord_user = relationship("DiscordUser")

    def __init__(self,
                 guild_id: int,
                 discord_id: int,
                 display_name: str,
                 joined_at: datetime,
                 profile_picture: str | None = None,
                 left_at: datetime | None = None):
        super().__init__()

        self.guild_id = guild_id
        self.discord_id = discord_id
        self.display_name = display_name
        self.joined_at = joined_at

        if profile_picture is not None:
            self.profile_picture = profile_picture

        if left_at is not None:
            self.left_at = left_at

    def to_dict(self):
        return {
            "guild_id": str(self.guild_id),
            "discord_id": str(self.discord_id),
            "display_name": self.display_name,
            "profile_picture": self.profile_picture,
            "joined_at": self.joined_at.isoformat(),
            "left_at": self.left_at.isoformat() if self.left_at else None,
        }

    def __repr__(self):
        return f"GuildDiscordUserMapping(guild_id={self.guild_id}, discord_id={self.discord_id})"
