from django.urls import path

from telegram.api.views import CreateAccountEndpoint, GetAccountEndpoint


app_name = "api"


urlpatterns = [
    path("account/", CreateAccountEndpoint.as_view(), name="create_account"),
    path("account/<int:account_id>", GetAccountEndpoint.as_view(), name="get_account"),
]
