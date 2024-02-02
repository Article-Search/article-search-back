from django.urls import path
from . import views

urlpatterns = [
    path('',views.add_list_favorites, name="add_list_favs"),
    path('<int:id>',views.pickone_delete_favorite, name="pick_delete_favs"),
]