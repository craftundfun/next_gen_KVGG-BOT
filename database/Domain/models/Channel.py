from database.Domain.BaseClass import *


class Channel(Base):
    __tablename__ = "channel"

    channel_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    type = Column(TEXT, nullable=False)
    deleted_at = Column(DATETIME, server_default=func.utc_timestamp(6))
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), nullable=False)

    relationship("Guild")

    def __repr__(self):
        return f"Channel(channel_id={self.channel_id}, name={self.name}, type={self.type}, deleted_at={self.deleted_at})"

    def __init__(self, channel_id: int, name: str, type: str, guild_id: int, deleted_at: datetime | None = None):
        super().__init__()

        self.channel_id = channel_id
        self.name = name
        self.type = type
        self.guild_id = guild_id

        if deleted_at is not None:
            self.deleted_at = deleted_at
