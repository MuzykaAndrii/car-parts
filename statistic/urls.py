from django.urls import path

from .views import IndexPage


app_name = 'stats'

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
]