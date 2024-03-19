from abc import ABC, abstractmethod

from .response import HttpResponse


class IAsyncRequestRepository(ABC):
    @abstractmethod
    async def get(self) -> HttpResponse:
        pass

    @abstractmethod
    async def post(self) -> HttpResponse:
        pass

    @abstractmethod
    async def patch(self) -> HttpResponse:
        pass

    @abstractmethod
    async def put(self) -> HttpResponse:
        pass
