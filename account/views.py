from django.shortcuts import render

from rest_framework import generics, permissions, status
from django.http import JsonResponse
from .models import User
from django.contrib.auth.hashers import make_password,check_password

from .serializers import UserSerializers
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response
# Create your views here.

class UserCreateView(generics.GenericAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]


    def post(self, request):
        
        username = request.data.get("username")
        password = request.data.get("password", "")
        customer = request.data.get("customer", False)
        shop_owner = request.data.get("shop_owner", False)
        full_name = request.data.get("full_name", "")
        
        bussiness_id = request.data.get("bussines", "")
        if customer and shop_owner:
            return JsonResponse({"error":"User cant be Both Customer and Shop Owner"})
        elif customer or shop_owner:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            full_name=full_name,
                                            bussiness_id=bussiness_id,
                                            is_customer=customer,
                                            is_shop_owner=shop_owner)

            ser = UserSerializers(user)
            # return JsonResponse(ser.data, safe=False)

            return JsonResponse({"user":ser.data, "is_customer":user.is_customer})
        else:
            return JsonResponse({"error":"Please choose one role"})
        # else:
        #     return JsonResponse(
        #                         {"error":"you are not authorized to add user"},
        #                         status=status.HTTP_401_UNAUTHORIZED)

    # def get(self, request):
    #     if request.user.admin:
    #         user = User.objects.all()
    #         if user:
    #             ser = UserSerializers(user, many=True)
    #             return JsonResponse({"users":ser.data})
    #         else:
    #             return JsonResponse({"error":"User doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return JsonResponse({"error":"User UnAuthorized to view users"}, status=status.HTTP_401_UNAUTHORIZED)