from database.Domain.BaseClass import *


class WebsiteRole(Base):
    __tablename__ = "website_role"

    role_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    role_name = Column(VARCHAR(255), nullable=False, unique=True)
    created_at = Column(DATETIME, server_default=func.utc_timestamp(6), nullable=False)
    priority = Column(Integer, nullable=False, default=0)

    def __init__(self, role_id: int, role_name: str, created_at: datetime | None = None, priority: int = 0):
        super().__init__()

        self.role_id = role_id
        self.role_name = role_name
        self.priority = priority

        if created_at is not None:
            self.created_at = created_at
