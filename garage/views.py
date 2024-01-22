from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages

from main.models import Auto
from auth.mixins import MyLoginRequiredMixin


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
    def get(self, request: HttpRequest):

        return render(request, "garage/history.html")