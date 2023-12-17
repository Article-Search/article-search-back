from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='articles_home'),
    path('upload/', views.upload_file, name='file_upload'),
]
