from django.urls import path

from garage.views import GarageView


app_name = 'garage'

urlpatterns = [
    path("", GarageView.as_view(), name="garage"),
]