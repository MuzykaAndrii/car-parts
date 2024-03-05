from functools import lru_cache

from aiohttp import ClientSession

from sessions import session_factory
from backend.services import BackendService


@lru_cache
def backend_session() -> ClientSession:
    return session_factory(
        base_url="http://127.0.0.1:8000",
    )


def backend_service():
    return BackendService(backend_session())