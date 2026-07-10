import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.activity_entity import ActivityLog, ActivityTypeEnum
from app.modules.user.entity import User


class ActivityService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_activity(
        self, user_id: uuid.UUID, activity_type: ActivityTypeEnum, metadata: dict | None = None
    ) -> ActivityLog:
        """Helper to create an activity log entry."""
        log = ActivityLog(
            user_id=user_id,
            activity_type=activity_type,
            metadata_json=metadata or {}
        )
        self.db.add(log)
        # We don't commit here so that the caller can wrap this in their own transaction
        # if they choose to, but it will be flushed/committed when the caller commits.
        return log
