from database.Domain.BaseClass import *
from database.Domain.Guild.Entity.Guild import Guild


class Channel(Base):
    __tablename__ = "channel"

    channel_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    type = Column(TEXT, nullable=False)
    deleted_at = Column(DATETIME, default=None)
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), nullable=False)

    relationship(Guild)

    def __repr__(self):
        return f"Channel(channel_id={self.channel_id}, name={self.name}, type={self.type}, deleted_at={self.deleted_at})"
