from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from auth.mixins import MyLoginRequiredMixin

from selection.forms import SelectionRequestForm
from selection.models import SelectionRequest


class SelectionRequestView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        form = SelectionRequestForm()
        return render(request, "selection/request.html", {'form': form})
    
    def post(self, request: HttpRequest):
        form = SelectionRequestForm(request.POST)

        if not form.is_valid():
            return render(request, "selection/request.html", {'form': form})

        selection_request: SelectionRequest = form.save(commit=False)
        selection_request.sender = request.user
        selection_request.save()
        return redirect('main:index')