from database.Domain.BaseClass import *


class Channel(Base):
    __tablename__ = "channel"

    channel_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    type = Column(TEXT, nullable=False)
    deleted_at = Column(DATETIME, default=None)
