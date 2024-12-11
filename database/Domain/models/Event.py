from database.Domain.BaseClass import *


class Event(Base):
    __tablename__ = "event"

    id = Column(BigInteger, primary_key=True)
    type = Column(VARCHAR(255), nullable=False)
