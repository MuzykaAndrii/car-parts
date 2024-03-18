from functools import lru_cache

from aiohttp import ClientSession

from backend.repository import AiohttpRepository
from sessions import session_factory
from backend.services import BackendService
from config import settings


@lru_cache
def backend_session() -> ClientSession:
    return session_factory(
        base_url=settings.BACKEND_URL,
    )

def backend_repo():
    return AiohttpRepository(backend_session())

def backend_service():
    return BackendService(backend_repo())