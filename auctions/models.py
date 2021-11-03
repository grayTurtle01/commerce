from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
     pass

class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.CharField(max_length=64)
    image_url = models.CharField(max_length=300)
    category = models.CharField(max_length=64)
    #date = models.DateTimeField()
    creator = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, default="admin")
    users = models.ManyToManyField(User, blank=True, related_name="products")

    def __str__(self):
        return f"{self.name}"

     
     


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()