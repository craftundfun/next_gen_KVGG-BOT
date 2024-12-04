from datetime import datetime

from database.Domain.BaseClass import *


class WebsiteRoleUserMapping(Base):
    __tablename__ = "website_role_user_mapping"

    role_id = Column(Integer, ForeignKey("website_role.role_id"), primary_key=True, nullable=False)
    discord_id = Column(BigInteger, ForeignKey("website_user.discord_id"), primary_key=True, nullable=False)
    created_at = Column(DATETIME, default=datetime.now(), nullable=False)
    deleted_at = Column(DATETIME, nullable=True)

    website_role = relationship("WebsiteRole", uselist=False)
    website_user = relationship("WebsiteUser", uselist=False)
