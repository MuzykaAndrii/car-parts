from django.urls import path

from .views import IndexPage,SalesView,MarginView


app_name = 'stats'

urlpatterns = [
    path('sales/', SalesView.as_view(), name='sales'),
    path('', IndexPage.as_view(), name='index'),
    path('margin/', MarginView.as_view(), name='margin'),
]