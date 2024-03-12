from django.urls import path

from scanner.api.views import PartByScannerEndpoint


app_name = 'api'


urlpatterns = [
    path('get_part_by_barcode/', PartByScannerEndpoint.as_view(), name='part_by_barcode'),
]
