from functools import lru_cache

from aiohttp import ClientSession
from sessions import session_factory


@lru_cache
def backend_session() -> ClientSession:
    return session_factory(
        base_url="http://127.0.0.1:8000",
    )