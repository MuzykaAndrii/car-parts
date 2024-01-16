from django.urls import path

from .views import (
    IndexPage,
    ScannerPage,
    PartByScanner
)

app_name = 'main'

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('scanner/', ScannerPage.as_view(), name='scanner'),
    path('get_part_by_barcode/', PartByScanner.as_view(), name='part_by_barcode'),
]