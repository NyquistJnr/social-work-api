import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.base_entity import BaseEntity


class CourseReview(BaseEntity):
    __tablename__ = "course_reviews"
    __table_args__ = (
        UniqueConstraint("course_id", "user_id", name="uq_course_user_review"),
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, server_default="false")
    
    reply_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    reply_created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
