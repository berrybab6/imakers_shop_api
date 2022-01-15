from importlib.metadata import requires
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
# from rest_framework.decorators import action
from .models import User
from django.contrib.auth.hashers import make_password,check_password

from .serializers import UserSerializers
from rest_framework.authtoken.views import ObtainAuthToken

# , authenticate
from rest_framework.permissions import AllowAny
from rest_framework import generics, status, permissions
# from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# Create your views here.
import random
import string
from rest_framework.authtoken.models import Token


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
        phone_number = request.data.get("phone_number","")
        email = request.data.get("email","")
        business_id = request.data.get("business_id", "")
        if customer and shop_owner:
            return JsonResponse({"error":"User cant be Both Customer and Shop Owner"})
        elif shop_owner:
            if business_id == None:
                return JsonResponse({"error":"Business ID is required for shopowners"})
            else:
                user = User.objects.create_user(username=username,
                                            email = email,
                                            password=password,
                                            full_name=full_name,
                                            business_id=business_id,
                                            is_customer=customer,
                                            phone_number = phone_number,
                                            is_shop_owner=shop_owner)

            ser = UserSerializers(user)
            # return JsonResponse(ser.data, safe=False)

            return JsonResponse(ser.data,safe=False, status=status.HTTP_200_OK)
        elif customer:
            
            user = User.objects.create_user(username=username,
                                        email = email,
                                        password=password,
                                        full_name=full_name,
                                        is_customer=customer,
                                        phone_number = phone_number,
                                        is_shop_owner=shop_owner)

            ser = UserSerializers(user)
            # return JsonResponse(ser.data, safe=False)

            return JsonResponse(ser.data,safe=False, status=status.HTTP_200_OK)
        
        else:
            return JsonResponse({"error":"Please choose one role"})


class GetAllUserView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (permissions.IsAdminUser, )
    def get(self, request,format=None):
        user = User.objects.all()
        serialize = UserSerializers(user,many=True)
        return JsonResponse(serialize.data,safe=False, status=status.HTTP_200_OK)

class LoginUserView(ObtainAuthToken):

    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny, ]
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        if username == "" or password == "":
            return JsonResponse({"msg":"Empty Field"}, status=status.HTTP_404_NOT_FOUND)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)

                ser = UserSerializers(user)
                # return JsonResponse({"message":"user logged in succesfully", "user":ser.data})

                # return JsonResponse(ser.data, safe=False)
                return JsonResponse({"user":ser.data, "token":token.key}, status=status.HTTP_201_CREATED)

            return JsonResponse({"error":"disabled account"}, status=status.HTTP_404_NOT_FOUND)
            #Return a 'disabled account' error message
        else:
            return JsonResponse({"error":"invalid login"}, status=status.HTTP_400_BAD_REQUEST)