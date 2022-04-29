from django.urls import path
from . import views

app_name = "infra"
urlpatterns = [
    path('health', views.health, name="health"),
]