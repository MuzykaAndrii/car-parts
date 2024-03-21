from aiogram import Router

from orders.windows import order_dialog


router = Router()
router.include_router(order_dialog)