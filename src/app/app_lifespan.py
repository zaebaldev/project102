from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.clients.redis import redis_client
from app.db.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    await redis_client.init()
    yield
    # shutdown
    await db_helper.dispose()
    await redis_client.close()
