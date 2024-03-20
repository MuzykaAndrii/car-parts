from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Case


def cart_is_present(data: dict, case: Case, manager: DialogManager) -> bool:
    return bool(data.get("cart", None))