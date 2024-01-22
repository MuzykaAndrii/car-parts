from typing import Any

from django.views.generic import TemplateView

from main.models import PartUnit
from auth.mixins import AdminRequiredMixin

class IndexPage(TemplateView, AdminRequiredMixin):
    template_name = 'statistic/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        queryset = PartUnit.objects.all()
        
        sales = {date: 0 for date in set(map(lambda item: str(item.sale_date.date()), queryset))}
        for el in queryset:
            sales[str(el.sale_date.date())] += el.sell_price
        margin = sum(map(lambda item: item.sell_price - item.buy_price, queryset))

        context['sale_date'] = list(sales.keys())
        context['sale_values'] = list(sales.values())
        context['margin'] = margin
        return context