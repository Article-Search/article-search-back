from django.db import models
from user_auth.models import User
from articles.models import Article
# Create your models here.

# This app manages the profile information of the user. like their favorites
# Here you can import the users models from the user_auth app and operate on them

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    articles = models.ManyToManyField(Article)
    
    class Meta:
        #managed = False
        db_table = 'favorite'
