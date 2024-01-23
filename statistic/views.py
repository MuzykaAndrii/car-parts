from collections import defaultdict
from functools import reduce
from typing import Any

from django.views.generic import TemplateView

from auth.mixins import AdminRequiredMixin
from store.models import Order

class IndexPage(TemplateView, AdminRequiredMixin):
    template_name = 'statistic/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        received_orders = Order.objects.filter(status=Order.STATUSES.RECEIVED).order_by("sold_at")
        total_margin = reduce(lambda acc, order: acc + order.margin, received_orders, 0)

        sales = defaultdict(float)
        for order in received_orders:
            order_date = str(order.sold_at.date())
            sales[order_date] += order.total

        context['sale_date'] = list(sales.keys())
        context['sale_values'] = list(sales.values())
        context['margin'] = total_margin
        return context