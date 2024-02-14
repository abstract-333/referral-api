import uuid
from pydantic import BaseModel


class ReferralBase(BaseModel):
    referral_id: uuid.UUID
    referrer_id: uuid.UUID


class ReferralInDB(ReferralBase):
    pass


class ReferralCreate(ReferralBase):
    pass
