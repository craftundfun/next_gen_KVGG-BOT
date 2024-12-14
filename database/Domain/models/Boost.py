from database.Domain.BaseClass import *


class Boost(Base):
    __tablename__ = "boost"

    boost_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    description = Column(TEXT, nullable=True)
    amount = Column(BigInteger, nullable=False, default=0)
    duration = Column(BigInteger, nullable=False, default=0)
