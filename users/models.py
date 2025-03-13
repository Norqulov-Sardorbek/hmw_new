from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField()
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'