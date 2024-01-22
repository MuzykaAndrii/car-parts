from django.urls import path

from user.views import SettingsView


app_name = "user"

urlpatterns = [
    path("settings/", SettingsView.as_view(), name="settings"),
]
