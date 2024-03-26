from dataclasses import dataclass
from typing import Any, Callable

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram.types import User
from pydantic import BaseModel


@dataclass(slots=True)
class SchemaComponent:
    field_name: str
    message: str
    value: str | None = None


class SchemaInput:
    def __init__(self, schema: type[BaseModel], on_end: Callable, show_mode: ShowMode, invalid_input_msg: str):
        self.schema = schema
        self.on_end = on_end
        self.invalid_input_msg = invalid_input_msg
        self.show_mode = show_mode


    async def handle_input(self, msg: Message, widget: ManagedTextInput, manager: DialogManager, schema_item: Any):
        manager.show_mode = self.show_mode
        current = manager.dialog_data.get("current")
        to_fill_remain = manager.dialog_data.get("to_fill")

        try:
            validator = self.schema.__pydantic_validator__.validate_assignment(
                self.schema.model_construct(),
                current.field_name, schema_item,
            )
        except Exception as e:
            return await self.handle_invalid_input(msg, widget, manager, e)
        
        current.value = getattr(validator, current.field_name)

        manager.dialog_data.get("filled").append(current)

        if not to_fill_remain:
            fields = dict()
            for filled in manager.dialog_data.get("filled"):
                fields.update({filled.field_name: filled.value})

            return await self.on_end(msg.from_user.id, manager, **fields)

        await manager.switch_to(manager.current_context().state)
        

    async def getter(self, dialog_manager: DialogManager, event_from_user: User, **kwargs):
        to_fill = dialog_manager.dialog_data.get("to_fill")
        current = dialog_manager.dialog_data.get("current")

        if not to_fill and not current:
            to_fill: list[self.schema] = []

            for field_name, info in self.schema.model_fields.items():
                to_fill.append(SchemaComponent(
                    field_name=field_name,
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
    

    async def handle_invalid_input(self, message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error):
        await message.reply(self.invalid_input_msg)
        dialog_manager.dialog_data.update({"error": True})
    
    # def get_current_field(self, manager: DialogManager):
    #     return self._get_dialog_data(manager, "current")
    
    # def get_fields_remain(self, manager: DialogManager):
    #     return self._get_dialog_data(manager, "remain")
    
    # def get_filled_fields(self, manager: DialogManager):
    #     return self._get_dialog_data(manager, "filled")
    
    # def get_validation_error(self, manager: DialogManager):
    #     return self._get_dialog_data(manager, "error")

    # def _get_dialog_data(self, dialog_manager: DialogManager, key: str) -> Any:
    #     return dialog_manager.dialog_data.get(key)
