from typing import NamedTuple


class HttpResponse(NamedTuple):
    status_code: int
    body: bytes