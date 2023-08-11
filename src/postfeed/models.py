from datetime import datetime
from sqlalchemy import Integer, String, TIMESTAMP, Text, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    add_message_at = mapped_column(TIMESTAMP, default=datetime.utcnow)
    title: Mapped[str] = mapped_column(String(length=50))
    message: Mapped[str] = mapped_column(Text, nullable=False)
    user = relationship("User", lazy="select")
    like_post_id: Mapped[int] = mapped_column(Integer, ForeignKey("like_post.id"), nullable=True, )
    like = relationship("LikePost", lazy="select", cascade="all, delete")


class LikePost(Base):
    __tablename__ = "like_post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    like_q: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    dislike_q: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    who: Mapped[list] = mapped_column(ARRAY(item_type=Integer), default={}, nullable=True, )

