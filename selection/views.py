from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages

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
        messages.success(request, "Запит на підбір успішно відправлено! Ми з вами звяжемось якнайшвидше!")
        return redirect('selection:list')


class SelectionRequestListView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        responded_selections = SelectionRequest.objects.filter(sender=request.user).order_by("-requested_at").prefetch_related("response__proposal")
        form = SelectionRequestForm()

        return render(request, "selection/index.html", {"selections": responded_selections, "form": form})


class RefuseSelectionView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int):
        selection_to_refuse = get_object_or_404(SelectionRequest, pk=pk, sender=request.user)
        selection_to_refuse.status = SelectionRequest.STATUSES.REFUSED
        selection_to_refuse.save()

        messages.success(request, "Ви відмовились від підбору, надіємося що наш наступний підбір вам сподобається!")
        return redirect("selection:list")

class AcceptSelectionView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int):
        ...