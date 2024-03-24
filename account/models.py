from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    city = models.CharField(max_length=300)
    phone_number = models.CharField(unique=True, max_length=15)
    confirmed_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

