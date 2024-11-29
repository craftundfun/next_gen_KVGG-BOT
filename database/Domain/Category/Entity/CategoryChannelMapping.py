from database.Domain.BaseClass import *
from database.Domain.Category.Entity.Category import Category
from database.Domain.Channel.Entity.Channel import Channel


# TODO evaluate if this is necessary, could be removed for a foreign key in the Channel table
class CategoryChannelMapping(Base):
    __tablename__ = "category_channel_mapping"

    category_id = Column(BigInteger, ForeignKey("category.category_id"), primary_key=True)
    channel_id = Column(BigInteger, ForeignKey("channel.channel_id"), primary_key=True)

    category = relationship(Category)
    channel = relationship(Channel)

    def __repr__(self):
        return f"CategoryChannelMapping(category_id={self.category_id}, channel_id={self.channel_id})"
