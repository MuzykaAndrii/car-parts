from typing import Any

from django.views.generic import TemplateView

from auth.mixins import AdminRequiredMixin
from statistic.services import DateRange, StoreStatistic, parse_date


class IndexPage(TemplateView, AdminRequiredMixin):
    template_name = 'statistic/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        date_range = self.get_date_range()        
        stats = StoreStatistic(date_range).get_stats()

        total_margin = sum((stat_item.margin for stat_item in stats.values()))

        context['stats'] = stats
        context['total_margin'] = total_margin

        stat_ranges = (
            DateRange(label="Увесь час").as_dict(),
            DateRange.last_year(label="Останній рік").as_dict(),
            DateRange.last_month(label="Останній місяць").as_dict(),
            DateRange.last_week(label="Останній тиждень").as_dict(),
        )

        context["stat_ranges"] = stat_ranges
        
        return context
    
    def _get_date_ranges_from_request(self) -> tuple[str, str]:
        date_from = self.request.GET.get('from', None)
        date_to = self.request.GET.get('to', None)
        
        return date_from, date_to
    
    def get_date_range(self) -> DateRange:
        date_from, date_to = self._get_date_ranges_from_request()

        date_from_as_obj = parse_date(date_from) if date_from else None
        date_to_as_obj = parse_date(date_to) if date_to else None

        return DateRange(date_from=date_from_as_obj, date_to=date_to_as_obj)