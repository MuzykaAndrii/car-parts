from collections import defaultdict
from functools import reduce
from typing import Any

from django.views.generic import TemplateView
from django.db.models import Q

from main.models import PartUnit
from auth.mixins import AdminRequiredMixin
from store.models import Order

class IndexPage(TemplateView, AdminRequiredMixin):
    template_name = 'statistic/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        # TODO: move sold date to order model instead partunit model and refactor this method appropriately tto new structure
        sold_product_units = PartUnit.objects.filter(
            Q(order__status=Order.OrderStatus.RECEIVED) | Q(order=None),
        ).order_by("sale_date")

        sales = defaultdict(float)
        for sold_product in sold_product_units:
            sold_at = str(sold_product.sale_date.date())
            sales[sold_at] += sold_product.sell_price * sold_product.quantity
        
        margin = reduce(lambda acc, item: acc + (item.sell_price - item.buy_price) * item.quantity, sold_product_units, 0)

        context['sale_date'] = list(sales.keys())
        context['sale_values'] = list(sales.values())
        context['margin'] = margin
        return context