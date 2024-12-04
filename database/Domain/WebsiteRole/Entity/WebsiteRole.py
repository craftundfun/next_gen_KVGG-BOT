from datetime import datetime

from database.Domain.BaseClass import *


class WebsiteRole(Base):
    __tablename__ = "website_role"

    role_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    role_name = Column(VARCHAR(255), nullable=False, unique=True)
    created_at = Column(DATETIME, default=datetime.now(), nullable=False)
    deleted_at = Column(DATETIME, nullable=True)
    priority = Column(Integer, nullable=False, default=0)


