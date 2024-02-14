from http import HTTPStatus

from starlette.exceptions import HTTPException


class ExceptionBadRequest400(HTTPException):
    """400"""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)


class ExceptionUnauthorized401(HTTPException):
    """401"""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail=detail)


class ExceptionForbidden403(HTTPException):
    """403"""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=HTTPStatus.FORBIDDEN, detail=detail)


class ExceptionNotFound404(HTTPException):
    """404"""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)


class ExceptionMethodNotAllowed405(HTTPException):
    """405"""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=HTTPStatus.METHOD_NOT_ALLOWED, detail=detail)


class ExceptionNotAcceptable406(HTTPException):
    """406"""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=HTTPStatus.NOT_ACCEPTABLE, detail=detail)


class ExceptionUNProcessableEntity422(HTTPException):
    """422"""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail)


class ExceptionInternalServerError500(HTTPException):

    """500"""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=detail)
