import uuid

from pydantic import BaseModel, PositiveInt


class ReferralCodeBase(BaseModel):
    referral_code: str
    valid_until: PositiveInt
    added_at: PositiveInt


class ReferralCodeInDB(ReferralCodeBase):
    user_id: uuid.UUID


class ReferralCodeRead(ReferralCodeBase):
    pass


class ReferralCodeCreate(BaseModel):
    user_id: uuid.UUID
