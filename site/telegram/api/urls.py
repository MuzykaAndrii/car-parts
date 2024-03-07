from django.urls import path

from telegram.api.views import CreateAccountView, GetAccountView


app_name = "api"


urlpatterns = [
    path("create_account/", CreateAccountView.as_view(), name="create_account"),
    path("account/<int:account_id>", GetAccountView.as_view(), name="get_account"),
]
