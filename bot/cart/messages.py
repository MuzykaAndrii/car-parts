

cart_empty = "Ваша корзина поки порожня("

cart_header = """
<b>🛒 Ваша корзина:</b>

<b>🛍️ Всього товарів:</b> {{cart.total_quantity}}
<b>💸 Сумма:</b> <u>{{cart.total}}</u>"""

cart_product = "⏺️ {item.part.name} до {item.part.belongs_to} {item.quantity}шт."