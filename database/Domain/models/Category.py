from database.Domain.BaseClass import *


class Category(Base):
    __tablename__ = "category"

    category_id = Column(BigInteger, unique=True, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    deleted_at = Column(DATETIME, nullable=True, default=None)
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), nullable=False)

    relationship("Guild")

    def __repr__(self):
        return f"Category(category_id={self.category_id}, name={self.name}, deleted_at={self.deleted_at})"
