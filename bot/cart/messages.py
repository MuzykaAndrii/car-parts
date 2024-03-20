

cart_empty = "Ваша корзина поки порожня("

cart_header = """
<b>🛒 Ваша корзина:</b>

<b>🛍️ Всього товарів:</b> {{cart.total_quantity}}
<b>💸 Сумма:</b> <u>{{cart.total}}</u>"""

cart_product = "⏺️ {item.part.name} до {item.part.belongs_to} {item.quantity}шт."

cart_item_detail = """
<b>Товар:</b> {{ product.part.name }} 📦
<b>До авто:</b> {{ product.part.belongs_to }} 🚗
<b>Артикул:</b> {{ product.part.articul }} 🔖
<b>Виробник:</b> <a href="{{ product.part.producer_detail_url }}">{{ product.part.producer }}</a> 🏭

<b>Кількість:</b> {{ product.quantity }} ⚖️
<b>Ціна за одиницю:</b> {{ product.sell_price }} 💰
<b>Ціна загалом:</b> {{ product.total_price }} 💵
"""