from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
     pass

class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    initial_price = models.IntegerField()
    price = models.IntegerField()
    image = models.CharField(max_length=64)
    image_url = models.CharField(max_length=300)
    category = models.CharField(max_length=64)
    #date = models.DateTimeField()
    creator = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, default="")
    users = models.ManyToManyField(User, blank=True, related_name="products")

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    new_price = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    #product_id = models.IntegerField()

    def __str__(self):
        return f"{self.new_price}  {self.bidder}"

class Comment(models.Model):
    comment = models.CharField(max_length=128)
    creator = models.CharField(max_length=64)
    product_id = models.IntegerField()     
    #date = models.DateField()

    def __str__(self):
        return f"{self.comment} | {self.creator}" 


class BidForm(forms.Form):
    new_price = forms.IntegerField(help_text="Bid")

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()