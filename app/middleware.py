from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class RedirectUnauthorizedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if response.status_code == HTTP_401_UNAUTHORIZED:
            return RedirectResponse(url="/login/")

        return response
