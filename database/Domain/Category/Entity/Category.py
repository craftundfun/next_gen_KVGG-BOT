from database.Domain.BaseClass import *


class Category(Base):
    __tablename__ = "category"

    category_id = Column(BigInteger, unique=True, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    deleted_at = Column(DATETIME, nullable=True, default=None)
