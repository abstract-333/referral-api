from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from schemas import ReferralInDB
from .base import (
    BaseModelORM,
    uuid_pk,
    uuid_type,
)


class ReferralsOrm(BaseModelORM[ReferralInDB]):
    id: Mapped[uuid_pk]
    referral_id: Mapped[uuid_type] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True,
    )
    referrer_id: Mapped[uuid_type] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "referral_id",
            "referrer_id",
            name="referral_id_referrer_id_constraint",
        ),
    )

    def __str__(self) -> str:
        return f"Referral  referral_id: {self.referral_id}, referrer_id: {self.referrer_id}"

    def to_read_model(self) -> ReferralInDB:
        return ReferralInDB.model_validate(self, from_attributes=True)
