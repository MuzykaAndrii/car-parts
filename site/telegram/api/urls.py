from django.urls import path

from telegram.api.views import AccountView


app_name = "api"


urlpatterns = [
    path("create_account/", AccountView.as_view(), name="create_account"),
]
