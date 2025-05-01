from database.Domain.BaseClass import *


class Category(Base):
    __tablename__ = "category"

    category_id = Column(BigInteger, unique=True, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    deleted_at = Column(DATETIME, nullable=True, server_default=func.utc_timestamp(6))
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), nullable=False)

    relationship("Guild")

    def __repr__(self):
        return f"Category(category_id={self.category_id}, name={self.name}, deleted_at={self.deleted_at})"

    def __init__(self, category_id: int, name: str, guild_id: int, deleted_at: datetime | None = None):
        super().__init__()

        self.category_id = category_id
        self.name = name
        self.guild_id = guild_id

        if deleted_at is not None:
            self.deleted_at = deleted_at
