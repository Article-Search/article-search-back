from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.logout,name='logout'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('test_token/',views.test_token,name='test_token'),
    path('test_admin/',views.test_admin,name='test_admin'),
    path('test_user/',views.test_user,name='test_user'),
    path('test_moderator/',views.test_moderator,name='test_moderator'),
    path('test_moderator_admin/',views.test_moderator_admin,name='test_moderator_admin')
]
