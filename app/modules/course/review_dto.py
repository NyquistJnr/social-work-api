import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.modules.user.dto import UserReadDTO


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    review_text: str | None = Field(None, max_length=2000, description="Optional text review")


class ReviewUpdate(BaseModel):
    rating: int | None = Field(None, ge=1, le=5, description="Rating from 1 to 5 stars")
    review_text: str | None = Field(None, max_length=2000, description="Optional text review")


class ReviewReplyDTO(BaseModel):
    reply_text: str = Field(..., max_length=2000, description="Instructor reply text")


class ReviewHideDTO(BaseModel):
    is_hidden: bool = Field(..., description="Whether the review is hidden from public view")


class ReviewRead(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    user_id: uuid.UUID
    rating: int
    review_text: str | None
    is_hidden: bool
    reply_text: str | None
    reply_created_at: datetime | None
    created_at: datetime
    updated_at: datetime | None = None
    user: UserReadDTO | None = None  # To include user details in the response

    class Config:
        from_attributes = True


class CourseBasicDTO(BaseModel):
    id: uuid.UUID
    title: str
    slug: str

    class Config:
        from_attributes = True


class ReviewAdminRead(ReviewRead):
    course: CourseBasicDTO | None = None

    class Config:
        from_attributes = True
