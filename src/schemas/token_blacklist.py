import uuid

from pydantic import BaseModel, PositiveInt, ConfigDict


class TokenBlacklistBase(BaseModel):
    user_id: uuid.UUID
    token: str


class TokenBlacklistInDB(TokenBlacklistBase):
    id: uuid.UUID
    added_at: PositiveInt
    model_config = ConfigDict(from_attributes=True)


class TokenBlacklistCreate(TokenBlacklistBase):
    pass
