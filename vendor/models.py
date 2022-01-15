from ast import Or
from email.mime import image
from itertools import product
from pyexpat import model
from tkinter import CASCADE
from unicodedata import category
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Shop(models.Model):
    name = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)
    location = models.CharField(max_length=200, default=False)
    shopOwner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="User",
                                  default=False, on_delete=models.CASCADE, null=True)

    def clean(self):
        if self.shopOwner.shop_owner != True:
            raise ValidationError('can not add customers')
        return super().clean()


class Color(models.Model):
    c_id = models.PositiveIntegerField()
    name = models.CharField(max_length=50)


class Size(models.Model):
    s_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=50)


class Category(models.Model):
    WOMENS = 1
    MENS = 2
    KIDS = 3

    CATEGORY_CHOICES = ((WOMENS, 'womens'), (MENS, 'mens'), (KIDS, 'kids'))

    id = models.PositiveSmallIntegerField(
        choices=CATEGORY_CHOICES, primary_key=True)

    def __str__(self) -> str:
        return self.get_id_display()


class Type(models.Model):
    AFAR = 1
    AMHARA = 2
    BENSHANGUL_GUMUZ = 3
    GAMBELA = 4
    HARARI = 5
    OROMIA = 6
    SNNPR = 7
    SOMALIA = 8
    TIGRAY = 9

    TYPE_CHOICES = ((AFAR, 'afar'), (AMHARA, 'amhara'), (BENSHANGUL_GUMUZ, 'benshangul_gumuz'), (GAMBELA, 'gambela'),
                    (HARARI, 'harari'), (OROMIA, 'oromia'), (SNNPR, 'snnpr'), (SOMALIA, 'somalia'), (TIGRAY, 'tigray'))

    id = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES, primary_key=True)

    def __str__(self) -> str:
        return self.get_id_display()


class ProductDetail(models.Model):
    color = models.ForeignKey(
        Color, related_name="Color", default=False, on_delete=models.CASCADE, null=True)
    size = models.ForeignKey(Size, related_name="Size",
                             default=False, on_delete=models.CASCADE, null=True)
    amount = models.PositiveIntegerField()


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    product_detail = models.ForeignKey(
        ProductDetail, related_name="ProductDetail", default=False, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        Category, related_name="Category", default=False, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(
        Type, related_name="Category", default=False, on_delete=models.CASCADE, null=True)

    # shop = models.ForeignKey("Shop", default=False, on_delete=models.CASCADE, null=True)


# class ShopOwner(models.Model):
#     shop = models.ForeignKey(
#         Shop, related_name="Shop", default=False, on_delete=models.CASCADE, null=True)
#     seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ShopOwner",
#                                default=False, on_delete=models.CASCADE, null=True)

#     def clean(self):
#         if self.seller.shop_owner != True:
#             raise ValidationError('can not add customers')
#         return super().clean()
