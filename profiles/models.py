from django.db import models
from articles.models import Article
# Create your models here.

# This app manages the profile information of the user. like their favorites
# Here you can import the users models from the user_auth app and operate on them

class Favorite(models.Model):
    articles = models.ManyToManyField(Article, related_name='favorites')
    
    class Meta:
        #managed = False
        db_table = 'favorite'
