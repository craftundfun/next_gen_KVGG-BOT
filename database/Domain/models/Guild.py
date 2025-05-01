from database.Domain.BaseClass import *


class Guild(Base):
    __tablename__ = "guild"

    # id = Column(BigInteger, autoincrement=True, unique=True, nullable=False)
    guild_id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    name = Column(VARCHAR(255), nullable=False)
    joined_at = Column(DATETIME, nullable=True, server_default=func.utc_timestamp(6))
    icon = Column(TEXT, nullable=True)

    def __init__(self, guild_id: int, name: str, joined_at: datetime | None = None, icon: str | None = None):
        super().__init__()

        self.guild_id = guild_id
        self.name = name

        if joined_at is not None:
            self.joined_at = joined_at

        if icon is not None:
            self.icon = icon

    def to_dict(self):
        return {
            "guild_id": str(self.guild_id),
            "name": self.name,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "icon": self.icon,
        }

    def __repr__(self):
        return f"Guild(guild_id={self.guild_id}, name={self.name}, joined_at={self.joined_at})"
