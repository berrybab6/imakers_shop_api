from rest_framework import serializers
from .models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email","password","phone_number","full_name","customer","profile_url","business_id","gender","admin","staff","shop_owner","is_validated"]

