from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class HttpResponse:
    status_code: int
    body: bytes