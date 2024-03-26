from dataclasses import dataclass


@dataclass(slots=True)
class FieldItem:
    field_name: str
    message: str
    value: str | None = None