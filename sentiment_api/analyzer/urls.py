from django.urls import path
from .views import analyze, history

urlpatterns = [
    path("analyze/", analyze),
    path("history/", history),
]
