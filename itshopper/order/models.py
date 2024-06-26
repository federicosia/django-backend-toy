from django.db import models


# Create your models here.
class Order(models.Model):
    OrderGenre = {"IT": "information technology", "EL": "electronics", "TM": "temp"}
    name = models.CharField(max_length=30)
    genre = models.CharField(max_length=30, choices=OrderGenre, default="TM")
    price = models.FloatField(default=1000)
