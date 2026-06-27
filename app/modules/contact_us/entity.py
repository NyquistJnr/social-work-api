from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.common.base_entity import BaseEntity


class ContactUsMessage(BaseEntity):
    __tablename__ = "contact_us_messages"

    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
