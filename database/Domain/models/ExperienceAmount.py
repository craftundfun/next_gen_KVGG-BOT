from database.Domain.BaseClass import *
from enum import Enum as PythonEnum


class ExperienceType(PythonEnum):
    ONLINE = "online"
    STREAM = "stream"
    MESSAGE = "message"
    COMMAND = "command"


class ExperienceAmount(Base):
    __tablename__ = "experience_amount"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    type = Column(Enum(ExperienceType, name='type_enum'), nullable=False, unique=True)
    amount = Column(BigInteger, nullable=False)
