from pydantic import EmailStr
import httpx
from exceptions.base import ExceptionBadRequest400
from exceptions.error_code import ErrorCode
from settings import settings_obj

from http import HTTPStatus


class EmailService:
    @classmethod
    async def verify_email(cls, email: EmailStr) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response: httpx.Response = await client.get(
                    url=f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings_obj.EMAIL_VERIFIER_API_KEY}"
                )
                if response.status_code != HTTPStatus.OK:
                    raise ExceptionBadRequest400(detail=ErrorCode.EMAIL_INVALID)

                email_validity: str | None = response.json()["data"]["result"]

                if email_validity == "deliverable":
                    return email

                raise ExceptionBadRequest400(detail=ErrorCode.EMAIL_INVALID)

        except Exception as e:
            raise e
