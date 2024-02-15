import re
import uuid
from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    Field,
    model_validator,
    PositiveInt,
    field_validator,
)

password_type = Annotated[str, Field(min_length=8, max_length=32)]
name_type = Annotated[
    str, Field(min_length=3, max_length=20, examples=["John", "Robert"])
]


def email_validator(email: EmailStr) -> EmailStr:
    """
    Deletes . and + from email, also deletes all characters after +
    in order to avoid email duplication
    :param email:
    :return:
    """
    deleting_after_plus_enabled: bool = False
    text_for_delete: str = ""
    # Remove all dots excluding the last one
    if email.count(".") > 1:
        email = email.replace(".", "", email.count(".") - 1)

    for index in range(len(email) - 1):
        if email[index] == "@":
            break

        if deleting_after_plus_enabled:
            text_for_delete += email[index]

        elif email[index] == "+":
            deleting_after_plus_enabled = True
            text_for_delete += email[index]

    if deleting_after_plus_enabled:
        email = email.replace(text_for_delete, "")

    return email


class BaseUser(BaseModel):
    first_name: name_type = Field(description="Not unique", max_length=30, min_length=4)
    last_name: name_type = Field(description="Not unique", max_length=30, min_length=4)
    email: EmailStr = Field(description="Unique")

    model_config = ConfigDict(str_strip_whitespace=True)


class ExtenedUser(BaseUser):
    is_verified: bool = Field(description="Default False")
    is_superuser: bool = Field(description="Default False")
    is_active: bool = Field(description="Default True")


class UserCreate(ExtenedUser):
    password: password_type = Field(description="Should not be contained in email")
    _validate_email = field_validator("email")(email_validator)
    is_verified: bool = Field(description="Default False")
    is_superuser: bool = Field(description="Default False")
    is_active: bool = Field(description="Default True")

    @model_validator(mode="after")
    def check_password(self):
        """
        Validate that password:
         # does not contain email nor username
         # has at least one uppercase character
         # has at least one lowercase character
         # has at least one special character
         # has at least one digit
        """

        if self.password.lower() in self.email.lower():
            raise ValueError("Password should not contain email")

        if self.password.lower() in self.first_name.lower() + self.last_name.lower():
            raise ValueError("Password should not contain full_name")

        uppercase_pattern = re.compile(r"[A-Z]")
        lowercase_pattern = re.compile(r"[a-z]")
        digit_pattern = re.compile(r"\d")
        special_pattern = re.compile(r'[!@#$%^&*()_+{}|\[\]:";<>,.?/~`]')

        if not uppercase_pattern.search(self.password):
            raise ValueError("Password should contain at least one uppercase character")

        if not lowercase_pattern.search(self.password):
            raise ValueError("Password should contain at least one lowercase character")

        if not digit_pattern.search(self.password):
            raise ValueError("Password should contain at least one digit")

        if not special_pattern.search(self.password):
            raise ValueError("Password should contain at least one special character")

        return self


class UserHashedPassword(ExtenedUser):
    hashed_password: str


class UserRead(ExtenedUser):
    id: uuid.UUID = Field(
        examples=["018b97b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    added_at: PositiveInt = Field(
        examples=[1699057255], description="Unix time in seconds"
    )
    updated_at: PositiveInt = Field(
        examples=[1699057255], description="Unix time in seconds"
    )

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserRead):
    hashed_password: str


class UserUpdate(BaseModel):
    first_name: Optional[name_type] = None
    last_name: Optional[name_type] = None
    email: Optional[EmailStr] = None
