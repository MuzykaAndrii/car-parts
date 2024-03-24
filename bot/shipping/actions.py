from dataclasses import dataclass
from typing import Literal
from aiogram.types import User
from aiogram_dialog import DialogManager

from backend.schemas import ShippingSchema, CreateShippingSchema
from components import backend_service


async def get_user_shipping(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> dict[Literal["shipping"], ShippingSchema | None]:
    account = await backend_service().get_account(event_from_user.id)
    shipping = await backend_service().get_user_shipping(account.user.id)

    return {"shipping": shipping}


@dataclass(slots=True)
class SchemaComponent:
    field_name: str
    annotation: type
    message: str
    value: str | None = None


async def get_shipping_component(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    to_fill = dialog_manager.dialog_data.get("to_fill")
    current = dialog_manager.dialog_data.get("current")

    if not to_fill and not current:
        to_fill: list[SchemaComponent] = []

        for field_name, info in CreateShippingSchema.model_fields.items():
            to_fill.append(SchemaComponent(
                field_name=field_name,
                annotation=info.annotation,
                message=info.title,
            ))

        dialog_manager.dialog_data.update(to_fill=to_fill)
        dialog_manager.dialog_data.update(filled=list())
    
    validation_error = dialog_manager.dialog_data.get("error")

    if validation_error:
        current_component = current
        dialog_manager.dialog_data.update(error=False)
    else:
        current_component = dialog_manager.dialog_data.get("to_fill").pop(0)
        dialog_manager.dialog_data.update(current=current_component)

    return {"component": current_component}