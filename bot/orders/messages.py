

cart_checkout = """
<b>🛒 Ваша корзина:</b>

{% for product in cart.products %}
{{loop.index}}. <a href='{{product.part.part_url}}'><i>{{product.part.name}}</i></a> ({{product.part.producer}}) до {{product.part.belongs_to}}
💰 {{product.sell_price}} x {{product.quantity}}шт = {{product.total_price}}

{% endfor %}
<b>🛍️ Всього товарів:</b> {{cart.total_quantity}}
<b>💸 Сумма:</b> <u>{{cart.total}}</u>

<b>Адреса доставки: </b>
<b>Імя:</b> {{shipping.first_name}} {{shipping.last_name}}
<b>Телефон:</b> {{shipping.phone_number}}
<b>Область:</b> {{shipping.region}}
<b>Наслелений пункт:</b> {{shipping.city}}
<b>омер відділення:</b> {{shipping.office_number}}
"""