from datetime import datetime, date, timedelta
from random import choice, randint

from store.models import Order
from main.models import PartUnit, Part


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def fill_db():
    today = date.today()
    year_ago = today - timedelta(days=365)

    parts = Part.objects.all()

    for date_ in date_range(year_ago, today):
        order = Order(
            customer=None,
            status=Order.STATUSES.RECEIVED,
        )
        order.save()

        for _ in range(randint(1, 4)):
            pu = PartUnit(
                order=order,
                quantity=randint(1,3),
                part=choice(parts),
            )
            pu.save()
        
        Order.objects.filter(pk=order.pk).update(sold_at=date_)