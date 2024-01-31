from django.urls import path

from selection.views import SelectionRequestView


app_name = "selection"

urlpatterns = [
    path("/request_selection", SelectionRequestView.as_view(), name="request_selection"),
]