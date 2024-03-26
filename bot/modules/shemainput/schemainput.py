from typing import Any, Callable, Literal

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from pydantic import BaseModel

from .field import FieldItem
from .validators import validate_single_field


class SchemaInput:
    def __init__(
        self,
        schema: type[BaseModel],
        on_end: Callable,
        show_mode: ShowMode = ShowMode.DELETE_AND_SEND,
        invalid_input_msg: str = "Invalid data received. Please try again.",
    ):
        self.schema = schema
        self.on_end = on_end
        self.invalid_input_msg = invalid_input_msg
        self.show_mode = show_mode


    async def handle_input(self, msg: Message, widget: ManagedTextInput, manager: DialogManager, user_input: Any):
        manager.show_mode = self.show_mode
        self._load_dialog_data(manager)

        try:
            self.current.value = validate_single_field(self.schema, self.current.field_name, user_input)
        except Exception as e:
            self.error = True
            return await self.handle_invalid_input(msg, widget, manager, e)

        self._record_filled(self.current)

        if not self.to_fill:
            fields = self._build_result()
            return await self.on_end(msg.from_user.id, manager, **fields)

        await self._retake_window(manager)
        

    async def getter(self, dialog_manager: DialogManager, **kwargs) -> dict[Literal["item"], FieldItem]:
        self._load_dialog_data(dialog_manager)

        if self.empty:
            self._init_data()

        if self.error:
            self.error = False
        else:
            self.current = self._get_next()

        return {"item": self.current}
    

    async def handle_invalid_input(self, message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error):
        await message.reply(self.invalid_input_msg)    

    def _load_dialog_data(self, manager: DialogManager):
        self.dialog_data = manager.dialog_data

    def _init_data(self):
        to_fill: list[FieldItem] = []

        for field_name, info in self.schema.model_fields.items():
            to_fill.append(FieldItem(
                field_name=field_name,
                message=info.title,
            ))

        self._init_to_fill(to_fill)
        self._init_filled()

    def _build_result(self) -> dict:        
        return {field.field_name: field.value for field in self.filled}
    
    async def _retake_window(self, manager: DialogManager):
        await manager.switch_to(manager.current_context().state)

    @property
    def filled(self) -> list[FieldItem]:
        return self.dialog_data.get("filled")
    
    def _init_filled(self):
        self.dialog_data.update({"filled": []})

    def _record_filled(self, item: FieldItem) -> None:
        self.filled.append(item)

    def _get_next(self) -> FieldItem:
        return self.to_fill.pop(0)

    @property
    def to_fill(self) -> list[FieldItem]:
        return self.dialog_data.get("to_fill")
    
    def _init_to_fill(self, items: list[FieldItem]):
        self.dialog_data.update({"to_fill": items})
    
    @property
    def current(self) -> FieldItem:
        return self.dialog_data.get("current")
    
    @current.setter
    def current(self, field: FieldItem):
        self.dialog_data.update({"current": field})

    @property
    def error(self) -> bool:
        return self.dialog_data.get("error")
    
    @error.setter
    def error(self, value: bool):
        self.dialog_data.update({"error": value})
    
    @property
    def empty(self) -> bool:
        if not self.to_fill and not self.current:
            return True
        return False


