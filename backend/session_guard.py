from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import RedirectResponse

class SessionGuardMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        protected_paths = (
            "/dashboard"
        )

        if request.method == "OPTIONS":
            return await call_next(request)

        if request.url.path.startswith(protected_paths):
            if not request.session.get("user_id"):
                return RedirectResponse("/auth/login", status_code=303)

        return await call_next(request)
