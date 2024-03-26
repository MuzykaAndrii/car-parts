from typing import Any

from pydantic import BaseModel


def validate_single_field(schema: type[BaseModel], field_name: str, field_value: Any) -> Any:
    validator = schema.__pydantic_validator__.validate_assignment(
        schema.model_construct(),
        field_name, field_value,
    )

    return getattr(validator, field_name)