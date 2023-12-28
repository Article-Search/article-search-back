from django.urls import path
from . import views

urlpatterns = [
    
    path('AdminCrud/',views.Create_List_Mod),
    path('AdminCrud/<int:pk>',views.Pickone_Modify_Delete_Mod),
       
]