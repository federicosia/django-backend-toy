from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    type_genres = {"IT": "information technology", "EL": "electronics", "TM": "temp"}
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    genre = models.CharField(max_length=30, choices=type_genres, default="TM")
    price = models.FloatField(default=0)
    sold = models.BooleanField(default=False)


class Cart(models.Model):
    is_snapshot = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)


class Order(models.Model):
    cart_snapshot = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
