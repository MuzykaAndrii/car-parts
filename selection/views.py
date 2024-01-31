from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class SelectionRequestView(View):
    def get(self, request: HttpRequest):
        return render(request, "selection/request.html")