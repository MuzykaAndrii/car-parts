from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import Any

from django.views.generic import TemplateView

from main.models import PartUnit
from auth.mixins import AdminRequiredMixin
from store.models import Order

class IndexPage(TemplateView, AdminRequiredMixin):
    template_name = 'statistic/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # TODO: calculate sell price according to quantity filed
        context = super().get_context_data(**kwargs)
        
        sold_with_orders = PartUnit.objects.filter(order__status=Order.OrderStatus.RECEIVED)
        sold_without_orders = PartUnit.objects.filter(order=None)
        sold_total = tuple(chain(sold_with_orders, sold_without_orders))

        sales = defaultdict(float)
        for sold_product in sold_total:
            sold_at = str(sold_product.sale_date.date())
            sales[sold_at] += sold_product.sell_price
        
        margin = reduce(lambda acc, item: acc + item.sell_price - item.buy_price, sold_total, 0)

        context['sale_date'] = list(sales.keys())
        context['sale_values'] = list(sales.values())
        context['margin'] = margin
        return context