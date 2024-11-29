from database.Domain.BaseClass import *
from database.Domain.Channel.Entity.Channel import Channel
from database.Domain.Guild.Entity.Guild import Guild


class ChannelGuildMapping(Base):
    __tablename__ = "channel_guild_mapping"

    channel_id = Column(BigInteger, ForeignKey("channel.channel_id"), nullable=False, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), nullable=False, primary_key=True)

    channel = relationship(Channel)
    guild = relationship(Guild)

    def __repr__(self):
        return f"ChannelGuildMapping(channel_id={self.channel_id}, guild_id={self.guild_id})"
