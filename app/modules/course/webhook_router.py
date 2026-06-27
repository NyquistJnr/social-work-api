from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.responses import ApiResponse
from app.core.config import settings
from app.core.database import get_db
from app.modules.course.content_service import CourseContentService

router = APIRouter(prefix="/webhooks/bunny", tags=["Webhooks"])


@router.post(
    "/video-status",
    response_model=ApiResponse[None],
    summary="Bunny Stream encoding-status callback (configure the URL with ?secret=... in the Bunny panel)",
    include_in_schema=False,
)
async def bunny_video_status(
    request: Request, secret: str, db: AsyncSession = Depends(get_db)
) -> ApiResponse[None]:
    if secret != settings.bunny_webhook_secret:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid webhook secret")

    payload = await request.json()
    video_guid = payload.get("VideoGuid")
    bunny_status = payload.get("Status")
    if video_guid is not None and bunny_status is not None:
        await CourseContentService(db).handle_bunny_webhook(video_guid, bunny_status)

    return ApiResponse(message="Webhook processed successfully")
