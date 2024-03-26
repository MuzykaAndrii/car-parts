from abc import ABC, abstractmethod

from ..response import HttpResponse


class IAsyncRequestRepository(ABC):
    @abstractmethod
    async def get(self, url) -> HttpResponse:
        pass

    @abstractmethod
    async def delete(self, url) -> HttpResponse:
        pass

    @abstractmethod
    async def post(self, url, data) -> HttpResponse:
        pass

    @abstractmethod
    async def patch(self, url, data) -> HttpResponse:
        pass

    @abstractmethod
    async def put(self, url, data) -> HttpResponse:
        pass
