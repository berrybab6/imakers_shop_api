from rest_framework import serializers
from . import models


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "_all_"
