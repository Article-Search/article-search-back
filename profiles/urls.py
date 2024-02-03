from django.urls import path
from .views import update_user

urlpatterns = [
    path('update/', update_user, name='user_update'),
]