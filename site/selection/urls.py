from django.urls import path

from selection.views import AcceptSelectionView, RefuseSelectionView, SelectionRequestListView, SelectionRequestView


app_name = "selection"

urlpatterns = [
    path("list/", SelectionRequestListView.as_view(), name="list"),
    path("request/", SelectionRequestView.as_view(), name="request"),
    path("<int:pk>/accept/", AcceptSelectionView.as_view(), name="accept"),
    path("<int:pk>/refuse/", RefuseSelectionView.as_view(), name="refuse"),
]