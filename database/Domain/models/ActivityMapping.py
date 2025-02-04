from database.Domain.BaseClass import *

if TYPE_CHECKING:
    from database.Domain.models.Activity import Activity


class ActivityMapping(Base):
    __tablename__ = "activity_mapping"

    primary_activity_id = Column(BigInteger, ForeignKey('activity.id'), primary_key=True, nullable=False)
    secondary_activity_id = Column(BigInteger, ForeignKey('activity.id'), primary_key=True, nullable=False, unique=True)

    # TODO fix mappings
    # primaryActivity: Mapped["Activity"] = relationship(
    #     "Activity",
    #     foreign_keys="primary_activity_id",
    #     uselist=False,
    # )
    # secondaryActivity: Mapped["Activity"] = relationship(
    #     "Activity",
    #     foreign_keys="secondary_activity_id",
    #     uselist=False,
    # )
