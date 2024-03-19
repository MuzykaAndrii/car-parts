from functools import lru_cache

from aiohttp import ClientSession

from sessions import session_factory
from config import settings


@lru_cache
def backend_session() -> ClientSession:
    return session_factory(
        base_url=settings.BACKEND_URL,
    )