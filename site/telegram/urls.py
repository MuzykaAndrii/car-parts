from django.urls import include, path


app_name = "telegram"

urlpatterns = [
    path("api/", include("telegram.api.urls", namespace="api")),
]
