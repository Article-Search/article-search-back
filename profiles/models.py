from django.db import models
from articles.models import Article
from user_auth.models import User

# Create your models here.

# This app manages the profile information of the user. like their favorites
# Here you can import the users models from the user_auth app and operate on them

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return f'Favorite of user {self.user.email}'
