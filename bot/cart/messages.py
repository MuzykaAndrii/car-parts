

cart_checkout = """
<b>🛒 Ваша корзина:</b>

{% for product in cart.products %}
{{loop.index}}. <i>{{product.part.name}}</i> ({{product.part.producer}}) до {{product.part.belongs_to}}
💰 {{product.sell_price}} x {{product.quantity}}шт = {{product.total_price}}

{% endfor %}
<b>🛍️ Всього товарів:</b> {{cart.total_quantity}}
<b>💸 Сумма:</b> <u>{{cart.total}}</u>
"""

cart_header = """
<b>🛒 Ваша корзина:</b>

<b>🛍️ Всього товарів:</b> {{cart.total_quantity}}
<b>💸 Сумма:</b> <u>{{cart.total}}</u>"""

cart_product = "⏺️ {item.part.name} до {item.part.belongs_to} {item.quantity}шт."