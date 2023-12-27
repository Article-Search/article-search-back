from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from .manager import CustomUserManager

class User(AbstractUser,PermissionsMixin):
    username = models.CharField(max_length=30, blank=True, null=True, unique=False)
    #above we made the username nullable and unique false so we can use the email as the username
    ROLE_CHOICES = (
        (1, 'admin'),
        (2, 'moderator'),
        (3, 'user'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    USERNAME_FIELD = 'email'#so we can catch the error if the email is not unique 
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
