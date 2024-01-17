from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from main.models import Auto


class GarageView(View):
    def get(self, request: HttpRequest):
        user_cars = request.user.cars.all()

        return render(request, "garage/index.html", {"cars": user_cars})


class AddCarToGarageView(View):
    def post(self, request: HttpRequest, car_vin: str):
        car_to_add = get_object_or_404(Auto, vin=car_vin)
        request.user.cars.add(car_to_add)

        return redirect("main:car_catalog", car_vin=car_vin)