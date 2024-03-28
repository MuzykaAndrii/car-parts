from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from pydantic import BaseModel, TypeAdapter
from aiohttp import ClientSession


T = TypeVar("T", bound=BaseModel)


class UnexpectedResponseStatusError(Exception):
    message: str = "Unexpected response status from: '{url}' expected: '{expected}' got: '{received}'"

    def __init__(self, url: str, status: int, allowed_statuses: Iterable[int]) -> None:
        super().__init__(self.message.format(url=url, expected=allowed_statuses, received=status))


class IUrlBuilder(ABC):
    @abstractmethod
    def build(self) -> str:
        pass


class UrlBuilder(IUrlBuilder):
    def __init__(self, url: str) -> None:
        self.url = url

    def build(self, **kwargs) -> str:
        return self.url.format(**kwargs)


class AbstractRequestManager(Generic[T], ABC):
    url_builder: IUrlBuilder
    response_schema: type[BaseModel] = None,
    response_many: bool = False,
    success_statuses: Iterable[int] = (200, )

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def __call__(self, **kwargs) -> T | None:
        status, body = await self._make_request(**kwargs)
        self.check_status(status)
        return self.build_response(body)

    def build_url(self, **kwargs) -> str:
        self.url = self.url_builder.build(**kwargs)
    
    @abstractmethod
    async def _make_request(self, **kwargs):
        pass
    
    def check_status(self, status: int) -> None:
        if not status in self.success_statuses:
            raise UnexpectedResponseStatusError(self.url, status, self.success_statuses)
    
    def build_response(self, data: bytes) -> T:
        if self.response_many:
            adapter = TypeAdapter(list[self.response_schema])
        else:
            adapter = TypeAdapter(self.response_schema)
        
        return adapter.validate_json(data)


class GetRequest(AbstractRequestManager, Generic[T]):
    async def _make_request(self):
        async with self._session.get(self.url) as resp:
            status = resp.status
            body = await resp.read()
        return status, body