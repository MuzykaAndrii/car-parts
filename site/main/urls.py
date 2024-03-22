from django.urls import include, path

from .views import (
    IndexPage,
    PartDetail,
    PartProducerView,
    PartProducersListView,
    CarCatalog,
    PartsCatalog,
    CarProducerCatalog,
)

app_name = 'main'

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),

    path('cars/producers/', CarProducerCatalog.as_view(), name='car_producers_catalog'),
    path('cars/<str:car_producer>/', CarCatalog.as_view(), name="car_catalog"),
    path('cars/<str:car_vin>/parts/', PartsCatalog.as_view(), name="parts_catalog"),
    path('cars/<str:car_vin>/parts/<int:part_id>', PartDetail.as_view(), name="part_detail"),

    path('parts/producers/', PartProducersListView.as_view(), name='part_producers_catalog'),
    path('parts/producers/<int:pk>', PartProducerView.as_view(), name='part_producer'),

    path('api/', include('main.api.urls', namespace='api')),
]