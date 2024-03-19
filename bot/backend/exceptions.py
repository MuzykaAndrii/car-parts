

from typing import Iterable


class UnexpectedResponseStatusError(Exception):
    message: str = "Unexpected response status from: '{url}' expected: '{expected}' got: '{received}'"

    def __init__(self, url: str, status: int, allowed_statuses: Iterable[int]) -> None:
        super().__init__(self.message.format(url=url, expected=allowed_statuses, received=status))