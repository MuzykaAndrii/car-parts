from django.urls import path

from main.api.views import CarListEndpoint, CarProducersListEndpoint, PartListEndpoint, PartEndpoint, SearchPartEndpoint


app_name = "api"

urlpatterns = [
    path('car_producers/', CarProducersListEndpoint.as_view(), name="car_producers_list"),
    path('car_producers/<int:producer_id>/cars', CarListEndpoint.as_view(), name="cars_list"),
    path('car_producers/<int:car_producer_id>/cars/<str:car_vin>/parts', PartListEndpoint.as_view(), name="parts_list"),
    path('car_producers/<int:car_producer_id>/cars/<str:car_vin>/parts/<int:part_id>', PartEndpoint.as_view(), name="part"),
    path('search', SearchPartEndpoint.as_view(), name="search"),
]
