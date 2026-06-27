import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.base_entity import BaseEntity


class VideoProviderEnum(str, enum.Enum):
    BUNNY = "BUNNY"


class VideoStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


class CourseVideo(BaseEntity):
    __tablename__ = "course_videos"

    course_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("course_items.id"), unique=True, nullable=False, index=True
    )
    provider: Mapped[VideoProviderEnum] = mapped_column(
        Enum(VideoProviderEnum, name="video_provider_enum", native_enum=True),
        nullable=False,
        default=VideoProviderEnum.BUNNY,
    )
    bunny_video_guid: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[VideoStatusEnum] = mapped_column(
        Enum(VideoStatusEnum, name="video_status_enum", native_enum=True),
        nullable=False,
        default=VideoStatusEnum.PENDING,
    )
    playback_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)


class CourseDocument(BaseEntity):
    __tablename__ = "course_documents"

    course_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("course_items.id"), unique=True, nullable=False, index=True
    )
    storage_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_uploaded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class CourseQuiz(BaseEntity):
    __tablename__ = "course_quizzes"

    course_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("course_items.id"), unique=True, nullable=False, index=True
    )
    passing_score_percentage: Mapped[int] = mapped_column(Integer, nullable=False, default=70)


class CourseQuizQuestion(BaseEntity):
    __tablename__ = "course_quiz_questions"

    quiz_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("course_quizzes.id"), nullable=False, index=True
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    allow_multiple_answers: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class CourseQuizOption(BaseEntity):
    __tablename__ = "course_quiz_options"

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("course_quiz_questions.id"), nullable=False, index=True
    )
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
