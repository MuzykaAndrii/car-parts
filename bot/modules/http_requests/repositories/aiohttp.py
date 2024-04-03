from .interface import IAsyncRequestRepository
from ..response import HttpResponse
from ..headers import HttpHeaders

from aiohttp import ClientSession, ClientResponse



class AioHttpRepository(IAsyncRequestRepository):
    def __init__(self, session: ClientSession) -> None:
        self.session = session

    async def _process_response(self, response: ClientResponse) -> HttpResponse:
        status_code = response.status
        body = await response.read()
        return HttpResponse(status_code=status_code, body=body)

    async def get(self, url: str, **kwargs) -> HttpResponse:
        async with self.session.get(url, **kwargs) as resp:
            return await self._process_response(resp)

    async def post(self, url: str, data: str) -> HttpResponse:
        async with self.session.post(url, data=data, headers=HttpHeaders.application_json) as resp:
            return await self._process_response(resp)

    async def delete(self, url: str) -> HttpResponse:
        async with self.session.delete(url) as resp:
            return await self._process_response(resp)

    async def patch(self, url: str, data: str) -> HttpResponse:
        async with self.session.patch(url, data=data, headers=HttpHeaders.application_json) as resp:
            return await self._process_response(resp)

    async def put(self, url: str, data: str) -> HttpResponse:
        async with self.session.put(url, data=data, headers=HttpHeaders.application_json) as resp:
            return await self._process_response(resp)