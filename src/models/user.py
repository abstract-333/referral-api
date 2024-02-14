from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from schemas import (
    UserInDB,
)
from .base import (
    BaseModelORM,
    uuid_pk,
    timeSeconds,
    timeSecondsOnUpdate,
    boolTrue,
    boolFalse,
)

if TYPE_CHECKING:
    from .token_blacklist import TokensBlacklistOrm
    from .referral_code import ReferralCodesOrm


class UsersOrm(BaseModelORM[UserInDB]):
    id: Mapped[uuid_pk]
    first_name: Mapped[String] = mapped_column(String(length=64), nullable=False)
    last_name: Mapped[String] = mapped_column(String(length=64), nullable=False)
    email: Mapped[str] = mapped_column(
        String(length=128 * 5),
        nullable=False,
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(String(length=256), nullable=False)
    added_at: Mapped[timeSeconds]
    updated_at: Mapped[timeSecondsOnUpdate]
    is_active: Mapped[boolTrue]
    is_verified: Mapped[boolFalse]
    is_superuser: Mapped[boolFalse]

    # Relationships for ORM
    tokens: Mapped[list["TokensBlacklistOrm"]] = relationship(
        back_populates="user",
    )
    referral_code: Mapped["ReferralCodesOrm"] = relationship(back_populates="user")

    repr_cols_num = 5
    repr_cols = ("is_active", "is_superuser")

    def __str__(self) -> str:
        return f"User full_name: {self.first_name} {self.last_name}"

    def to_read_model(self) -> UserInDB:
        return UserInDB.model_validate(self, from_attributes=True)
