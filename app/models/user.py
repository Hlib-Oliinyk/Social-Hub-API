import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    friendship_requesters: Mapped[list["Friendship"]] = relationship(back_populates="requester", foreign_keys="[Friendship.requester_id]")
    friendship_addressees: Mapped[list["Friendship"]] = relationship(back_populates="addressee", foreign_keys="[Friendship.addressee_id]")
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")