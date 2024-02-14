from pydantic import BaseModel


class BaseModelException(BaseModel):
    detail: str | dict[str, str]


class HTTPException500(BaseModelException):
    detail: str | dict[str, str]

    class Config:
        json_schema_extra = {
            "example": {"detail": "Will return what cause exception"},
        }


http_exception_dict500: dict[str, str] = {
    "model": HTTPException500,
    "description": "Internal Server Error",
}
