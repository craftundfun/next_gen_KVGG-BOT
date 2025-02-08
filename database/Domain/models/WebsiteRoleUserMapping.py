from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.WebsiteRole import WebsiteRole
    from database.Domain.models.WebsiteUser import WebsiteUser


class WebsiteRoleUserMapping(Base):
    __tablename__ = "website_role_user_mapping"

    role_id = Column(Integer, ForeignKey("website_role.role_id"), primary_key=True, nullable=False)
    discord_id = Column(BigInteger, ForeignKey("website_user.discord_id"), primary_key=True, nullable=False)
    created_at = Column(DATETIME, server_default=func.utc_timestamp(6), nullable=False)

    website_role: Mapped[Optional["WebsiteRole"]] = relationship("WebsiteRole", uselist=False)
    website_user: Mapped[Optional["WebsiteUser"]] = relationship("WebsiteUser", uselist=False)
