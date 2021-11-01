from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.CharField(max_length=64)
    image_url = models.CharField(max_length=64)
    category = models.CharField(max_length=64)


    def __str__(self):
        return f"{self.name}"
