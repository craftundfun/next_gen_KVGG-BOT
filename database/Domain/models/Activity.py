from database.Domain.BaseClass import *


# if TYPE_CHECKING:
#     from database.Domain.models.ActivityMapping import ActivityMapping


class Activity(Base):
    __tablename__ = "activity"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    external_activity_id = Column(BigInteger, nullable=True, server_default=null())
    name = Column(VARCHAR(255), nullable=False)

    def __init__(self, id: int | None = None, external_activity_id: int | None = None, name: str = ""):
        super().__init__()

        if id is not None:
            self.id = id

        if external_activity_id is not None:
            self.external_activity_id = external_activity_id

        self.name = name

    # activityMappings: Mapped["ActivityMapping"] = relationship(
    #     "ActivityMapping",
    #     foreign_keys=lambda: [
    #         __import__("database.Domain.models.ActivityMapping", fromlist=["ActivityMapping"])
    #         .ActivityMapping.secondary_activity_id
    #     ],
    # )
