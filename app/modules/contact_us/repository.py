from sqlalchemy.ext.asyncio import AsyncSession

from app.common.base_repository import BaseRepository
from app.modules.contact_us.entity import ContactUsMessage


class ContactUsRepository(BaseRepository[ContactUsMessage]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ContactUsMessage)
