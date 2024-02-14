import datetime

from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.user import UsersOrm
from schemas import TokenBlacklistInDB
from .base import (
    BaseModelORM,
    uuid_pk,
    uuid_type,
    timeSeconds,
)


class TokensBlacklistOrm(BaseModelORM[TokenBlacklistInDB]):
    __tablename__ = "tokens_blacklist"
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid_type] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    token: Mapped[str] = mapped_column(String(length=512), unique=True, nullable=False)
    added_at: Mapped[timeSeconds]

    # Relationships for ORM
    user: Mapped["UsersOrm"] = relationship(back_populates="tokens")

    def __str__(self) -> str:
        return f"Token added_at: {datetime.datetime.fromtimestamp(self.added_at)}"

    def to_read_model(self) -> TokenBlacklistInDB:
        return TokenBlacklistInDB.model_validate(self, from_attributes=True)
