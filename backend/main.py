import asyncio
from fastapi import HTTPException, status
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

from config import SECRET_KEY
#from worker import send_email_task
from routes import auth, files
from starlette.middleware.sessions import SessionMiddleware
#from session_guard import SessionGuardMiddleware


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
) 


# Middleware
#app.add_middleware(SessionGuardMiddleware)
app.add_middleware(
    SessionMiddleware,
    same_site="lax",
    secret_key=SECRET_KEY,
    https_only=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["*"],
    max_age=3600,
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
        return response

app.add_middleware(SecurityHeadersMiddleware)

#-------------Register-Routes---------------
app.include_router(auth.router)
app.include_router(files.router)


@app.get("/")
def root():
    return {"Server's Alive"}
