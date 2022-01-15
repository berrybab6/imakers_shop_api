from email.mime import image
from django.db import models

from shop import settings


class Shop(models.Model):
    name = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)


class ShopOwner(models.Model):
    ShopOwner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ShopOwner",
                                  default=False, on_delete=models.CASCADE, null=True)


class Color(models.Model):
    c_id = models.PositiveIntegerField()
    name = models.CharField(max_length=50)


class Size(models.Model):
    s_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=50)


class ProductDetail(models.Model):
    color = models.ForeignKey(
        Color, related_name="Color", default=False, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
