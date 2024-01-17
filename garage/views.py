from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class GarageView(View):
    def get(self, request: HttpRequest):
        user_cars = request.user.cars.all()

        return render(request, "garage/index.html", {"cars": user_cars})