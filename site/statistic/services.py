from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any

from django.db.models import QuerySet

from store.models import Order


def parse_date(input_date: str, format: str = "%Y-%m-%d") -> date:
    return datetime.strptime(input_date, format).date()


@dataclass(slots=True)
class StatisticItem:
    margin: float = 0
    sales: float = 0


class StatisticScale(Enum):
    DAILY = lambda date_: date_
    MONTHLY = lambda date_: date_.month
    YEARLY = lambda date_: date_.year


class DateRange:
    def __init__(
        self,
        date_from: date = None,
        date_to: date = None,
        label = None,
        format="%Y-%m-%d",
    ) -> None:
        self.date_from = date_from if date_from else date.min
        self.date_to = date_to if date_to else date.today()
        self._label = label
        self.format=format
    
    @property
    def date_from_str(self):
        return self.date_from.strftime(self.format)
    
    @property
    def date_to_str(self):
        return self.date_to.strftime(self.format)
    
    @property
    def label(self) -> str:
        if not self._label:
            return f"Статистика за {self.date_from} - {self.date_to}"
        return self._label
    
    def as_dict(self) -> dict:
        return {"from": self.date_from_str, "to": self.date_to_str, "label": self.label}
    
    @classmethod
    def last_week(cls, **kwargs):
        today = date.today()
        last_monday = today - timedelta(days=today.weekday())

        return cls(date_from=last_monday, date_to=today, **kwargs)
    
    @classmethod
    def last_month(cls, **kwargs):
        today = date.today()
        first_day_of_month = today.replace(day=1)

        return cls(date_from=first_day_of_month, date_to=today, **kwargs)
    
    @classmethod
    def last_year(cls, **kwargs):
        today = date.today()
        first_day_of_year = today.replace(month=1, day=1)

        return cls(date_from=first_day_of_year, date_to=today, **kwargs)


class AbstractStatistic(ABC):
    def __init__(self, date_range: DateRange, scale: StatisticScale = StatisticScale.DAILY) -> None:
        self.date_range = date_range
        self.scale = scale

    @abstractmethod
    def get_queryset(self) -> QuerySet:
        pass

    @abstractmethod
    def get_stats(self) -> dict[Any, StatisticItem]:
        pass


class StoreStatistic(AbstractStatistic):
    def get_queryset(self) -> QuerySet[Order]:
        return Order.objects.filter(
            status=Order.STATUSES.RECEIVED,
            sold_at__date__gte=self.date_range.date_from,
            sold_at__date__lte=self.date_range.date_to,
        ).order_by("sold_at")
    
    def get_stats(self) -> dict[Any, StatisticItem]:
        sold_products = self.get_queryset()
        stats = defaultdict(StatisticItem)

        for order in sold_products: 
            key = self.scale(order.sold_at.date())

            stats[key].sales += order.total
            stats[key].margin += order.margin
        
        return dict(stats)