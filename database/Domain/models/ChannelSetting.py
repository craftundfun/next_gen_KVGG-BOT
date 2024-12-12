from database.Domain.BaseClass import *


class ChannelSetting(Base):
    __tablename__ = "channel_setting"

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    channel_id = Column(BigInteger, ForeignKey("channel.channel_id"), nullable=False)
    track_time = Column(BOOLEAN, nullable=False, default=False)

    relationship("Channel")
