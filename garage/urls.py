from django.urls import path

from garage.views import AddCarToGarageView, GarageView


app_name = 'garage'

urlpatterns = [
    path("", GarageView.as_view(), name="garage"),
    path("add/<str:car_vin>", AddCarToGarageView.as_view(), name="add_car"),
]