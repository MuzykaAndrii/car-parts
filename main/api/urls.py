from django.urls import path

from main.api.views import CarListView, CarProducersListView, PartListView, PartView


app_name = "api"

urlpatterns = [
    path('car_producers/', CarProducersListView.as_view(), name="car_producers_list"),
    path('car_producers/<int:producer_id>/cars', CarListView.as_view(), name="cars_list"),
    path('car_producers/<int:car_producer_id>/cars/<str:car_vin>/parts', PartListView.as_view(), name="parts_list"),
    path('car_producers/<int:car_producer_id>/cars/<str:car_vin>/parts/<int:part_id>', PartView.as_view(), name="part"),
]
