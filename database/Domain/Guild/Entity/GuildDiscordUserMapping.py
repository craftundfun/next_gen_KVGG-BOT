from database.Domain.BaseClass import *
from database.Domain.DiscordUser.Entity.DiscordUser import DiscordUser
from database.Domain.Guild.Entity.Guild import Guild


class GuildDiscordUserMapping(Base):
    __tablename__ = "guild_discord_user_mapping"

    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), primary_key=True, nullable=False)
    discord_user_id = Column(BigInteger, ForeignKey("discord_user.discord_id"), primary_key=True, nullable=False)
    display_name = Column(VARCHAR(255), nullable=False)

    guild = relationship(Guild)
    discord_user = relationship(DiscordUser)

    def __repr__(self):
        return f"GuildDiscordUserMapping(guild_id={self.guild_id}, discord_user_id={self.discord_user_id})"
