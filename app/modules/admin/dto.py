from pydantic import EmailStr, Field, model_validator

from app.common.base_dto import BaseDTO, CreateDTO
from app.modules.auth.dto import USERNAME_PATTERN
from app.modules.user.dto import UserReadDTO
from app.modules.user.entity import PlatformEnum


class InviteAdminRequestDTO(CreateDTO):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    phone_number: str | None = Field(default=None, max_length=20)
    platform: PlatformEnum

    @model_validator(mode="after")
    def validate_username(self) -> "InviteAdminRequestDTO":
        if not USERNAME_PATTERN.match(self.username.lower()):
            raise ValueError(
                "Username must be 3-30 characters and contain only lowercase letters, "
                "numbers, dots, or underscores"
            )
        self.username = self.username.lower()
        return self


class AcceptAdminInviteRequestDTO(BaseDTO):
    token: str = Field(min_length=1)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "AcceptAdminInviteRequestDTO":
        if self.password != self.confirm_password:
            raise ValueError("password and confirm_password do not match")
        return self


class AdminInviteResponseDTO(BaseDTO):
    user: UserReadDTO
