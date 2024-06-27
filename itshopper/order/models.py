from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Order(models.Model):
    price = models.FloatField(default=0)
    items = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Item(models.Model):
    type_genres = {"IT": "information technology", "EL": "electronics", "TM": "temp"}
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    genre = models.CharField(max_length=30, choices=type_genres, default="TM")
    price = models.FloatField(default=0)
