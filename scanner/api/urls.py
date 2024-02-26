from django.urls import path

from scanner.api.views import PartByScanner


app_name = 'api'


urlpatterns = [
    path('get_part_by_barcode/', PartByScanner.as_view(), name='part_by_barcode'),
]
