from rest_framework import serializers
from .models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
# class ShopSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Shop
#         fields = "__all__"