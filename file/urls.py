from django.urls import path
from . import views

app_name = "file"
urlpatterns = [
    path('upload', views.FileUpload.as_view(), name="upload"),
]