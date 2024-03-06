

car_provider_title = "Оберіть марку авто ⚙️ 🔧"
car_provider_item = "{item.name}"
car_providers_cancel = "Вийти"

cars_list_title = "Оберіть модель авто 🚗 🚕"
cars_list_item = "📃: {item.model} 🗓️: {item.year_of_production} ⚙️: {item.engine_volume} 🛢️: {item.fuel}"
cars_list_back = "↩️ Обрати іншу марку"

parts_list_title = "Оберіть товар 🛞 🔧"
parts_list_item = "{item.name} ®️: {item.producer}"
parts_list_back = "↩️ Обрати іншу модель"

part_item_template = """
🔹 <b>Товар:</b> {{part.name}}
🚗 <b>До авто:</b> {{part.belongs_to}}
🏷️ <b>Артикул:</b> {{part.articul}}
🏭 <b>Виробник:</b> {{part.producer}}
💰 <b>Ціна:</b> {{part.sell_price}}
"""
add_to_cart = "🛒 Додати в корзину"
part_item_back = "↩️ Обрати іншу деталь"
