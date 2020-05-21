from fastapi import FastAPI

from . import config, logger  # noqa: F401
from .routers import router

app = FastAPI()

app.include_router(router)
