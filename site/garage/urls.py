from django.urls import path

from garage.views import AddCarToGarageView, CarHistoryView, GarageView, DeleteCarFromGarageView


app_name = 'garage'

urlpatterns = [
    path("", GarageView.as_view(), name="garage"),
    path("add/<str:car_vin>", AddCarToGarageView.as_view(), name="add_car"),
    path("delete/<str:car_vin>", DeleteCarFromGarageView.as_view(), name="delete_car"),
    path("history/<str:car_vin>", CarHistoryView.as_view(), name="history"),
]