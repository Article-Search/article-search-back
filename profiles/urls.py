from django.urls import path
from .views import update_user , add_to_favorites , delete_from_favorites , get_favorites

urlpatterns = [
    path('update/', update_user, name='user_update'),
    path('addToFavorites/', add_to_favorites , name='add_to_favorites'),
    path('deletefromfavorites/<str:article_id>', delete_from_favorites , name='delete_from_favorites'),
    path('getFavorites/', get_favorites , name='get_favorites'),

]