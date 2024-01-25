from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any

from django.views.generic import TemplateView

from auth.mixins import AdminRequiredMixin
from store.models import Order


def parse_date(input_date: str | date | datetime, format: str = "%Y-%m-%d") -> date:
    match input_date:
        case str():
            return datetime.strptime(input_date, format).date()
        case date():
            return input_date
        case datetime():
            return input_date.date()
        case _:
            raise TypeError


class IndexPage(TemplateView, AdminRequiredMixin):
    template_name = 'statistic/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        date_from, date_to = self.get_date_range()

        date_from = parse_date(date_from)
        date_to = parse_date(date_to)

        received_orders = Order.objects.filter(
            status=Order.STATUSES.RECEIVED,
            sold_at__date__gte=date_from,
            sold_at__date__lte=date_to,
        ).order_by("sold_at")

        total_margin = sum((order.margin for order in received_orders))

        sales = defaultdict(float)
        margins = defaultdict(float)

        for order in received_orders:
            order_date = order.sold_at.date()
            sales[order_date] += order.total
            margins[order_date] += order.margin

        context['sale_date'] = list(sales.keys())
        context['sale_values'] = list(sales.values())
        context['margins'] = list(margins.values())
        context['total_margin'] = total_margin

        today = date.today()
        last_monday = today - timedelta(days=today.weekday())

        context['weekly'] = {"from": last_monday.strftime("%Y-%m-%d"), "to": today.strftime("%Y-%m-%d")}

        first_day_of_month = today.replace(day=1)
        context['monthly'] = {"from": first_day_of_month.strftime("%Y-%m-%d"), "to": today.strftime("%Y-%m-%d")}

        first_day_of_year = today.replace(month=1, day=1)
        context['yearly'] = {"from": first_day_of_year.strftime("%Y-%m-%d"), "to": today.strftime("%Y-%m-%d")}
        
        return context
    
    def get_date_range(self) -> tuple[date, date]:
        date_from = self.request.GET.get('from', None)
        date_to = self.request.GET.get('to', None)

        if not date_from:
            date_from = date.min
        
        if not date_to:
            date_to = date.today()
        
        return date_from, date_to