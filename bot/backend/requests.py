from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from aiohttp import ClientResponse, ClientSession
from pydantic import BaseModel

from backend.exceptions import UnexpectedResponseStatusError


T = TypeVar("T", bound=BaseModel)


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
    def __init__(
        self,
        session: ClientSession,
        url_builder: IUrlBuilder,
        response_schema: type[BaseModel] = None,
        response_many: bool = False,
        success_statuses: Iterable[int] = (200, )
    ) -> None:
        self._session = session
        self._url_builder = url_builder
        self._response_schema = response_schema
        self._response_many = response_many
        self._allowed_response_statuses = success_statuses

    @abstractmethod
    async def __call__(self, *args, **kwargs) -> T:
        pass

    def _build_url(self, **kwargs) -> str:
        self.url = self._url_builder.build(**kwargs)
    
    def _check_status(self, status: int) -> None:
        if not status in self._allowed_response_statuses:
            raise UnexpectedResponseStatusError(self.url, status, self._allowed_response_statuses)
    
    def _build_response_schema(self, response: ClientResponse) -> T:
        if self._response_many:
            return [self._response_schema(**resp_instance) for resp_instance in response]
        else:
            return self._response_schema(**response)


class GetManager(AbstractRequestManager, Generic[T]):
    async def __call__(self, *args, **kwargs) -> T:
        self._build_url(**kwargs)

        async with self._session.get(self.url) as resp:
            self._check_status(resp.status)
            result = await resp.json()

        return self._build_response_schema(result)


class DeleteManager(AbstractRequestManager,Generic[T]):
    def __init__(
        self,
        session: ClientSession,
        url_builder: IUrlBuilder,
        success_statuses: Iterable[int] = (204, )
    ) -> None:
        super().__init__(session=session, url_builder=url_builder, success_statuses=success_statuses)

    async def __call__(self, *args, **kwargs) -> None:
        self._build_url(**args, **kwargs)

        async with self._session.delete(self.url) as resp:
            self._check_status(resp.status)


class CreateManager(AbstractRequestManager, Generic[T]):
    def __init__(
        self,
        session: ClientSession,
        url_builder: IUrlBuilder,
        create_schema: type[BaseModel],
        success_statuses: Iterable[int] = (201, )
    ) -> None:
        self._create_schema = create_schema,
        super().__init__(
            session=session,
            url_builder=url_builder,
            success_statuses=success_statuses,
            response_many=False,
        )
    
    async def __call__(self, *args, **kwargs) -> T:
        self._build_url(**args, **kwargs)
        json_data = self._create_schema(**kwargs).model_dump_json()

        async with self._session.post(
            self.url,
            data=json_data,
            headers={"Content-Type": "application/json"}
        ) as resp:
            self._check_status(resp.status)


class PutManager(AbstractRequestManager, Generic[T]):
    def __init__(
        self,
        session: ClientSession,
        url_builder: IUrlBuilder,
        update_schema: type[BaseModel],
        success_statuses: Iterable[int] = (200, 204),
    ) -> None:
        self._update_schema = update_schema
        super().__init__(
            session=session,
            url_builder=url_builder,
            success_statuses=success_statuses,
            response_many=False,
        )

    async def __call__(self, *args, **kwargs) -> T:
        self._build_url(**args, **kwargs)
        json_data = self._update_schema(**kwargs).model_dump_json()

        async with self._session.put(
            self.url,
            data=json_data,
            headers={"Content-Type": "application/json"},
        ) as resp:
            self._check_status(resp.status)

        return self._build_response_schema(json_data)


class PatchManager(AbstractRequestManager, Generic[T]):
    def __init__(
        self,
        session: ClientSession,
        url_builder: IUrlBuilder,
        update_schema: type[BaseModel],
        success_statuses: Iterable[int] = (200, 204),
    ) -> None:
        self._update_schema = update_schema
        super().__init__(
            session=session,
            url_builder=url_builder,
            success_statuses=success_statuses,
            response_many=False,
        )

    async def __call__(self, *args, **kwargs) -> T:
        self._build_url(**args, **kwargs)
        json_data = self._update_schema(**kwargs).model_dump_json()

        async with self._session.patch(
            self.url,
            data=json_data,
            headers={"Content-Type": "application/json"},
        ) as resp:
            self._check_status(resp.status)

        return self._build_response_schema(json_data)
