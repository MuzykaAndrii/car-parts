from functools import lru_cache

from aiohttp import ClientSession

from .http import AioHttpRepository
from .sessions import session_factory
from backend.services import BackendService
from config import settings


@lru_cache
def backend_session() -> ClientSession:
    return session_factory(base_url=settings.BACKEND_URL)

def backend_repo():
    return AioHttpRepository(backend_session())

def backend_service():
    return BackendService(backend_repo())


__all__ = ("backend_session", "backend_service")