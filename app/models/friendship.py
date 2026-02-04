import datetime
from enum import Enum
from sqlalchemy import Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base


class FriendStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Friendship(Base):
    __tablename__ = "friendships"

    id: Mapped[int] = mapped_column(primary_key=True)
    requester_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    addressee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[FriendStatus] = mapped_column(
        SAEnum(FriendStatus, name="status"),
        nullable=False,
        default=FriendStatus.pending
    )
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    requester: Mapped["User"] = relationship(
        back_populates="friendship_requesters",
        foreign_keys="[Friendship.requester_id]"
    )

    addressee: Mapped["User"] = relationship(
        back_populates="friendship_addressees",
        foreign_keys="[Friendship.addressee_id]"
    )