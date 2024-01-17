from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class GarageView(View):
    def get(self, request: HttpRequest):
        # fetch user cars
        return render(request, "garage/index.html")
