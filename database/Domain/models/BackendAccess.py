from database.Domain.BaseClass import *


class BackendAccess(Base):
    __tablename__ = "backend_access"

    id = Column(BigInteger, primary_key=True)
    ip_address = Column(VARCHAR(45), nullable=False)
    access_time = Column(DATETIME, nullable=False, server_default=func.utc_timestamp(6))
    authorized = Column(BOOLEAN, nullable=False)
    country_code = Column(VARCHAR(2), nullable=True)
    country_name = Column(VARCHAR(200), nullable=True)
    path = Column(TEXT, nullable=False)
    response_code = Column(Integer, nullable=False)
    response = Column(TEXT, nullable=True)

    def __init__(self,
                 ip_address: str,
                 access_time: datetime,
                 authorized: bool,
                 path: str,
                 response_code: int,
                 country_code: str | Null = null(),
                 country_name: str | Null = null(),
                 response: str | Null = null(), ):
        super().__init__()

        self.ip_address = ip_address
        self.access_time = access_time
        self.authorized = authorized
        self.path = path
        self.country_code = country_code
        self.country_name = country_name
        self.response_code = response_code
        self.response = response
