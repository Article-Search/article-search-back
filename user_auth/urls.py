from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('test_admin/',views.test_admin,name='test_admin'),
    path('test_user/',views.test_user,name='test_user'),
    path('test_moderator/',views.test_moderator,name='test_moderator'),
    path('test_moderator_admin/',views.test_moderator_admin,name='test_moderator_admin'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('refresh_token/', views.custom_token_refresh, name='token_refresh'),

    # Add more paths for your views here
]