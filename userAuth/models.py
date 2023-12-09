from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from .manager import CustomUserManager

class User(AbstractUser,PermissionsMixin):
    ROLE_CHOICES = (
        (1, 'admin'),
        (2, 'moderator'),
        (3, 'user'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
