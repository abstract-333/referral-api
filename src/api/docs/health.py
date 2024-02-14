from typing import Any

from starlette import status

from api.docs.base import httpexceptiondict500

health_response: dict[int | str, dict[str, Any]] = {
    status.HTTP_503_SERVICE_UNAVAILABLE: {},
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
