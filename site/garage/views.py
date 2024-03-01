from collections import defaultdict
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages

from main.models import Auto, PartUnit
from auth.mixins import MyLoginRequiredMixin
from store.models import Order


class GarageView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        user_cars = request.user.cars.all()

        return render(request, "garage/index.html", {"cars": user_cars})


class AddCarToGarageView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest, car_vin: str):
        car_to_add = get_object_or_404(Auto, vin=car_vin)
        request.user.cars.add(car_to_add)

        messages.success(request, "Машину успішно додана у ваш гараж!")
        return redirect("main:car_catalog", car_producer=car_to_add.producer.name)


class DeleteCarFromGarageView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest, car_vin: str):
        car_to_delete = get_object_or_404(Auto, vin=car_vin)
        request.user.cars.remove(car_to_delete)

        messages.success(request, "Машина успішно видалена з вашого гаражу!")
        return redirect("garage:garage")


class CarHistoryView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest, car_vin: str):
        # TODO: optimize db queries
        car = get_object_or_404(Auto, vin=car_vin)
        purchased_part_units = PartUnit.objects.filter(
            order__customer=request.user,
            part__belongs_to=car,
            order__status=Order.STATUSES.RECEIVED,
        ).order_by("-order__sold_at")

        purchased_part_units_by_date = defaultdict(list)
        for part_unit in purchased_part_units:
            date_purchased = str(part_unit.order.sold_at.date())
            purchased_part_units_by_date[date_purchased].append(part_unit)

        return render(request, "garage/history.html", {"parts": dict(purchased_part_units_by_date), "car": car})