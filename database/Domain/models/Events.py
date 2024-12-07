from database.Domain.BaseClass import *


class Events(Base):
    __tablename__ = "events"

    id = Column(BigInteger, primary_key=True)
    type = Column(VARCHAR(255), nullable=False)
