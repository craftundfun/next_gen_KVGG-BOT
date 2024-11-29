from database.Domain.BaseClass import *
from database.Domain.Category.Entity.Category import Category
from database.Domain.Guild.Entity.Guild import Guild


class CategoryGuildMapping(Base):
    __tablename__ = "category_guild_mapping"

    category_id = Column(BigInteger, ForeignKey("category.category_id"), nullable=False, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guild.guild_id"), nullable=False, primary_key=True)

    category = relationship(Category)
    guild = relationship(Guild)

    def __repr__(self):
        return f"CategoryGuildMapping(category_id={self.category_id}, guild_id={self.guild_id})"
