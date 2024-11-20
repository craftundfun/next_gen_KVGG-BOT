from database.Domain.BaseClass import *


class GuildDiscordUserMapping(Base):
    __tablename__ = 'guild_discord_user_mapping'

    guild_id = Column(BigInteger, ForeignKey('guild.guild_id'), primary_key=True)
    discord_user_id = Column(BigInteger, ForeignKey('discord_user.discord_id'), primary_key=True)

    guild = relationship('Guild')
    discord_user = relationship('DiscordUser')
