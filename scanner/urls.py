from django.urls import include, path

from scanner.views import ScannerPage


app_name = 'scanner'


urlpatterns = [
    path('', ScannerPage.as_view(), name='scan'),
    path('api/', include('scanner.api.urls', namespace='api')),
]