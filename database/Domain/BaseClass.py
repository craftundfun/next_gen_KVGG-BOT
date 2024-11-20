# tell the IDE to ignore the import error, otherwise the Entity classes will not have any imported classes
# noinspection PyUnresolvedReferences
from sqlalchemy import Column, BigInteger, VARCHAR, ForeignKey, DATETIME
# noinspection PyUnresolvedReferences
from sqlalchemy.orm import DeclarativeBase, relationship
# noinspection PyUnresolvedReferences
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass
