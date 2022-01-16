from rest_framework import serializers
from . import models


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "_all_"
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = "_all_"