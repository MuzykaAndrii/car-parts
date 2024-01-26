from django.urls import path

from .views import (
    IndexPage,
    PartProducerView,
    PartProducersListView,
    ScannerPage,
    PartByScanner,
    CarCatalog,
    PartsCatalog,
    CarProducerCatalog,
)

app_name = 'main'

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('scanner/', ScannerPage.as_view(), name='scanner'),
    path('get_part_by_barcode/', PartByScanner.as_view(), name='part_by_barcode'),

    path('cars/producers/', CarProducerCatalog.as_view(), name='car_producers_catalog'),
    path('cars/<str:car_producer>/', CarCatalog.as_view(), name="car_catalog"),
    path('cars/<str:car_vin>/parts/', PartsCatalog.as_view(), name="parts_catalog"),

    path('parts/producers/', PartProducersListView.as_view(), name='part_producers_catalog'),
    path('parts/producers/<int:pk>', PartProducerView.as_view(), name='part_producer'),
]