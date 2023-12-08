from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.logout,name='logout'),
    path('test_token/',views.test_token,name='test_token'),
    # Add more paths for your views here
]