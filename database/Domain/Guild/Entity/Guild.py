from database.Domain.BaseClass import *


class Guild(Base):
    __tablename__ = "guild"

    guild_id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    name = Column(VARCHAR(255), nullable=False)
    joined_at = Column(DATETIME)

    def __repr__(self):
        return f"Guild(guild_id={self.guild_id}, name={self.name}, joined_at={self.joined_at})"
