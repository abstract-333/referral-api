import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import (
    BaseModelORM,
    uuid_pk,
    uuid_type,
)
from schemas import ReferralInDB

if TYPE_CHECKING:
    from models.user import UsersOrm


def _get_userslorm() -> type["UsersOrm"]:
    from .user import UsersOrm

    return UsersOrm


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

    # Relationships for ORM
    # referral_user: Mapped["UsersOrm"] = relationship(
    #     back_populates="referral",
    #     # foreign_keys=["ReferralsOrm.referral_id"],
    #     # primaryjoin="referral_id == UsersOrm.id",
    # )
    # referrer_user: Mapped["UsersOrm"] = relationship(
    #     back_populates="referrer",
    #     # foreign_keys=["ReferralsOrm.referrer_id"],
    #     # primaryjoin="referrer_id == UsersOrm.id",
    # )

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
