from django.urls import path
from . import views

urlpatterns = [
    path('',views.create_list_moderators, name="create_list_mods"),
    path('<int:id>',views.pickone_modify_delete_moderator, name="pick_update_delete_mod"),
]
