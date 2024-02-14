import datetime
import time
from typing import TYPE_CHECKING
from nanoid import generate

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings import settings_obj
from models.user import UsersOrm

from .base import (
    BaseModelORM,
    uuid_pk,
    uuid_type,
    timeSeconds,
)
from schemas import ReferralCodeInDB


class ReferralCodesOrm(BaseModelORM[ReferralCodeInDB]):
    __tablename__ = "referral_codes"
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid_type] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True,
    )
    referral_code: Mapped[str] = mapped_column(
        String(length=10),
        unique=True,
        nullable=False,
        default=generate(size=settings_obj.NANO_ID_LENGTH),
    )
    added_at: Mapped[timeSeconds]

    valid_until: Mapped[int] = mapped_column(
        nullable=False,
        default=time.time() + settings_obj.REFERRAL_CODE_EXPIRATION,
    )

    # Relationships for ORM
    user: Mapped["UsersOrm"] = relationship(back_populates="referral_code")

    def __str__(self) -> str:
        return f"Referral Code : {self.referral_code}, valid_until: {datetime.datetime.fromtimestamp(self.valid_until)}"

    def to_read_model(self) -> ReferralCodeInDB:
        return ReferralCodeInDB.model_validate(self, from_attributes=True)
