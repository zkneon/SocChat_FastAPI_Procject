import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from auth.manager import get_user_manager
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead
from auth.router import get_register_router
"""Add router here"""
from operations.router import router as router_operation
from postfeed.router import router as router_postfeed
from pages.router import router as router_register


app = FastAPI(
    title="SocForSocial",
    debug=True,

)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_home_page() -> RedirectResponse:
    """Redirect to post page"""
    return RedirectResponse(url="postfeed/lastpost", status_code=307)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    get_register_router(get_user_manager, UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operation)
app.include_router(router_postfeed)
app.include_router(router_register)


origins = [
    "http://localhost:3000",
    "http://localhost:8000"
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80, log_level="debug")
