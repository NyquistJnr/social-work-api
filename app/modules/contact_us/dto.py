from pydantic import EmailStr, Field

from app.common.base_dto import AuditDTO, CreateDTO


class ContactUsCreateDTO(CreateDTO):
    full_name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    phone_number: str = Field(min_length=1, max_length=20)
    company_name: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1)


class ContactUsReadDTO(AuditDTO):
    full_name: str
    email: str
    phone_number: str
    company_name: str
    message: str
