from django.urls import path

from selection.views import SelectionRequestView


app_name = "selection"

urlpatterns = [
    path("request/", SelectionRequestView.as_view(), name="request"),
]