import uuid

from pydantic import Field

from app.common.base_dto import AuditDTO, BaseDTO, CreateDTO, UpdateDTO
from app.modules.course.content_entity import VideoStatusEnum
from app.modules.course.dto import CourseReadDTO, PublicCourseReadDTO
from app.modules.course.entity import CourseItemTypeEnum

# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


class CourseSectionCreateDTO(CreateDTO):
    title: str = Field(min_length=1, max_length=255)
    order_index: int = 0


class CourseSectionUpdateDTO(UpdateDTO):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    order_index: int | None = None


class SectionOrderEntryDTO(BaseDTO):
    id: uuid.UUID
    order_index: int


class CourseSectionReorderDTO(BaseDTO):
    sections: list[SectionOrderEntryDTO]


# ---------------------------------------------------------------------------
# Items - create/update payloads
# ---------------------------------------------------------------------------


class CourseItemCreateDTO(CreateDTO):
    title: str = Field(min_length=1, max_length=255)
    item_type: CourseItemTypeEnum
    order_index: int = 0
    is_preview: bool = False
    # Required only when item_type == DOCUMENT, used to build the R2 storage key.
    file_name: str | None = Field(default=None, max_length=255)


class CourseItemUpdateDTO(UpdateDTO):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    order_index: int | None = None
    is_preview: bool | None = None


class ItemOrderEntryDTO(BaseDTO):
    id: uuid.UUID
    order_index: int


class CourseItemReorderDTO(BaseDTO):
    items: list[ItemOrderEntryDTO]


# ---------------------------------------------------------------------------
# Video
# ---------------------------------------------------------------------------


class CourseVideoPublicDTO(BaseDTO):
    status: VideoStatusEnum
    playback_url: str | None = None
    thumbnail_url: str | None = None
    duration_seconds: int | None = None


class CourseVideoManageDTO(CourseVideoPublicDTO):
    bunny_video_guid: str


class VideoUploadCredentialsDTO(BaseDTO):
    """Everything the frontend needs to start a resumable (TUS) upload directly
    to Bunny Stream - no file bytes ever touch our API."""

    tus_endpoint: str
    library_id: str
    video_id: str
    authorization_signature: str
    authorization_expire: int


# ---------------------------------------------------------------------------
# Document
# ---------------------------------------------------------------------------


class CourseDocumentPublicDTO(BaseDTO):
    file_name: str
    mime_type: str | None = None
    file_size_bytes: int | None = None
    is_uploaded: bool


class CourseDocumentManageDTO(CourseDocumentPublicDTO):
    storage_key: str


class DocumentUploadCredentialsDTO(BaseDTO):
    upload_url: str
    storage_key: str


class DocumentFinalizeDTO(BaseDTO):
    mime_type: str | None = None
    file_size_bytes: int | None = Field(default=None, ge=0)


# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------


class QuizOptionCreateDTO(CreateDTO):
    text: str = Field(min_length=1, max_length=500)
    is_correct: bool = False
    order_index: int = 0


class QuizOptionUpdateDTO(UpdateDTO):
    text: str | None = Field(default=None, min_length=1, max_length=500)
    is_correct: bool | None = None
    order_index: int | None = None


class QuizQuestionCreateDTO(CreateDTO):
    text: str = Field(min_length=1)
    order_index: int = 0
    allow_multiple_answers: bool = False
    options: list[QuizOptionCreateDTO] = Field(default_factory=list)


class QuizQuestionUpdateDTO(UpdateDTO):
    text: str | None = Field(default=None, min_length=1)
    order_index: int | None = None
    allow_multiple_answers: bool | None = None


class CourseQuizOptionPublicDTO(BaseDTO):
    id: uuid.UUID
    text: str
    order_index: int


class CourseQuizOptionManageDTO(CourseQuizOptionPublicDTO):
    is_correct: bool


class CourseQuizQuestionPublicDTO(BaseDTO):
    id: uuid.UUID
    text: str
    order_index: int
    allow_multiple_answers: bool
    options: list[CourseQuizOptionPublicDTO]


class CourseQuizQuestionManageDTO(BaseDTO):
    id: uuid.UUID
    text: str
    order_index: int
    allow_multiple_answers: bool
    options: list[CourseQuizOptionManageDTO]


class CourseQuizPublicDTO(BaseDTO):
    id: uuid.UUID
    passing_score_percentage: int
    questions: list[CourseQuizQuestionPublicDTO]


class CourseQuizManageDTO(BaseDTO):
    id: uuid.UUID
    passing_score_percentage: int
    questions: list[CourseQuizQuestionManageDTO]


# ---------------------------------------------------------------------------
# Items - read tiers (assembled by the service, not built via from_attributes,
# since video/document/quiz live in separate tables with no ORM relationship)
# ---------------------------------------------------------------------------


class CourseItemReadDTO(AuditDTO):
    section_id: uuid.UUID
    title: str
    item_type: CourseItemTypeEnum
    order_index: int
    is_preview: bool
    video: CourseVideoPublicDTO | None = None
    document: CourseDocumentPublicDTO | None = None
    quiz: CourseQuizPublicDTO | None = None


class CourseItemManageReadDTO(AuditDTO):
    section_id: uuid.UUID
    title: str
    item_type: CourseItemTypeEnum
    order_index: int
    is_preview: bool
    video: CourseVideoManageDTO | None = None
    document: CourseDocumentManageDTO | None = None
    quiz: CourseQuizManageDTO | None = None


class CourseSectionReadDTO(AuditDTO):
    course_id: uuid.UUID
    title: str
    order_index: int
    items: list[CourseItemReadDTO] = Field(default_factory=list)


class CourseSectionManageReadDTO(AuditDTO):
    course_id: uuid.UUID
    title: str
    order_index: int
    items: list[CourseItemManageReadDTO] = Field(default_factory=list)


class CourseDetailDTO(CourseReadDTO):
    sections: list[CourseSectionReadDTO] = Field(default_factory=list)


from app.modules.course.dto import CourseReadDTO, PublicCourseReadDTO
class CourseManageDetailDTO(CourseReadDTO):
    sections: list[CourseSectionManageReadDTO] = Field(default_factory=list)

class PublicCourseDetailDTO(PublicCourseReadDTO):
    sections: list[CourseSectionReadDTO] = Field(default_factory=list)
