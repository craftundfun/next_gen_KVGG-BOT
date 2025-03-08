"""
tell the IDE to ignore the import error, otherwise the Entity classes will not have any imported classes
"""
# noinspection PyUnresolvedReferences
from datetime import datetime
# noinspection PyUnresolvedReferences
from typing import Optional, TYPE_CHECKING

# noinspection PyUnresolvedReferences
from sqlalchemy import Column, BigInteger, VARCHAR, ForeignKey, DATETIME, TEXT, Integer, TIMESTAMP, JSON, BOOLEAN, Enum
# noinspection PyUnresolvedReferences
from sqlalchemy import null, Date
# noinspection PyUnresolvedReferences
from sqlalchemy.orm import DeclarativeBase, relationship
# noinspection PyUnresolvedReferences
from sqlalchemy.orm import Mapped
# noinspection PyUnresolvedReferences
from sqlalchemy.sql import func
# noinspection PyUnresolvedReferences
from sqlalchemy.inspection import inspect


class Base(DeclarativeBase):
    pass
