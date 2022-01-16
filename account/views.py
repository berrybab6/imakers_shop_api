from importlib.metadata import requires
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from vendor.models import Shop

from django.conf import settings
from django.core.mail import send_mail

from vendor.seriliazer import ShopSerializer
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


from wsgiref.util import FileWrapper
from .custom_renderer import JPEGRenderer
# , PNGRenderer
from rest_framework import generics

from rest_framework.response import Response
# Create your views here.

class ImageAPIView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    renderer_classes = [JPEGRenderer]

    def get(self, request, pk):
        # renderer_classes = [JPEGRenderer]
        queryset = User.objects.get(username=pk).profile_url
        if queryset !=None:

            data = queryset
            return Response(data, content_type='image/jpg')
        else:
            return JsonResponse({"message":"there is no profile associated with thes username"})
class BusinessImageAPIView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    renderer_classes = [JPEGRenderer]

    def get(self, request, pk):
        # renderer_classes = [JPEGRenderer]
        queryset = User.objects.get(username=pk).business_id
        if queryset !=None:

            data = queryset
            return Response(data, content_type='image/jpg')
        else:
            return JsonResponse({"message":"there is no business_ID Image associated with thes username"})


class ImageRelated(generics.GenericAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]

    def get(self,request):
        user = User.objects.get(id=7)
        if user:
            picture = user.profile_url
            return JsonResponse(picture, safe=False)




class UserCreateView(generics.GenericAPIView):
    serializer_class = [UserSerializers,ShopSerializer]
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]


    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password", "")
        customer = request.data.get("customer", False)
        shop_owner = request.data.get("shop_owner", False)
        full_name = request.data.get("full_name", "")
        phone_number = request.data.get("phone_number","")
        email = request.data.get("email")
        
        profile_url = request.data.get("profile_url",None)
        business_id = request.data.get("business_id", None)

        ####shop attributes
        name = request.data.get("name","")
        location = request.data.get("location", "")
        logo = request.data.get("logo", None)
        if not email or not username or not password:
            return JsonResponse({"error":"User cant be Fields can't be Empty "})
        else:
            if customer:
                if shop_owner:
                    return JsonResponse({"error":"Users can't be both shop owner and Customer"})
                else:
                    user = User.objects.create_user(username=username,
                                        email = email,
                                        password=password,
                                        full_name=full_name,
                                        is_customer=customer,
                                        profile_url=profile_url,
                                        phone_number = phone_number,
                                        is_shop_owner=shop_owner)

                    ser = UserSerializers(user)
                    # return JsonResponse(ser.data, safe=False)
                    subject = 'welcome to Abysinnia world'
                    message = f'Hi {user.username}, thank you for registering in Abysinia Shop.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    return JsonResponse(ser.data,safe=False, status=status.HTTP_200_OK)
            elif shop_owner:
                if business_id ==None:
                    return JsonResponse({"error":"Business ID is required for shopowners"})
                else:
                    print("business_id",business_id)
                    user = User.objects.create_user(username=username,
                                                email = email,
                                                password=password,
                                                full_name=full_name,
                                                business_id=business_id,
                                                profile_url=profile_url,
                                                is_customer=customer,
                                                phone_number = phone_number,
                                                is_shop_owner=shop_owner)
                    user.save()

                    # shop = Shop()
                    # shop.name = name
                    # shop.location = location
                    # shop.logo = logo
                    # shop.shopOwner = user
                
                    ser = UserSerializers(user)

                    return JsonResponse(ser.data, safe=False)
            else: 
                return JsonResponse({"error":"Please role must be either Customer or Shop Owner"})


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
                if user.is_customer:
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)

                    ser = UserSerializers(user)
                
                elif user.is_shop_owner==True and user.is_validated==True:
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)

                    ser = UserSerializers(user)
                else:
                    return JsonResponse({"error":"unverified user account"}, status=status.HTTP_404_NOT_FOUND)

                    
                
                # return JsonResponse({"message":"user logged in succesfully", "user":ser.data})

                # return JsonResponse(ser.data, safe=False)
                return JsonResponse({"user":ser.data, "token":token.key}, status=status.HTTP_201_CREATED)

            return JsonResponse({"error":"disabled account"}, status=status.HTTP_404_NOT_FOUND)
            #Return a 'disabled account' error message
        else:
            return JsonResponse({"error":"invalid login"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated ]
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        if user:
            ser = UserSerializers(user)
            return JsonResponse({"user_detail":ser.data}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error":"User Doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        user = User.objects.get(id=request.user.id)
        if user:
            username = request.data.get('username', user.username)
            userprofile = request.data.get('profile_url', user.profile_url)

            full_name = request.data.get('full_name', user.full_name)
            user.username = username
            user.profile_url = userprofile
            user.full_name = full_name
            try:
                user.save()
                ser = UserSerializers(user)
                return JsonResponse({"updated user":ser.data}, status=status.HTTP_201_CREATED)
            except Exception:
                return JsonResponse({"error":"Update Failed"})
        else:
            return JsonResponse({"error":"User doesnot exist"})
    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        if user:
            user.delete()
            return JsonResponse({"success":"User Deleted Succesfully"}, status=status.HTTP_204_NO_CONTENT)
# Create your views here.
class ChangePassword(generics.GenericAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    """Change Password
    """
    def put(self, request):
        user = User.objects.get(id=request.user.id)
        if user:

                oldpass = request.data.get("password","")
                newpass = request.data.get('newpassword',"")

                if oldpass and newpass:
                    password = user.password
                    if check_password(oldpass, password):
                        user.set_password(newpass)
                        user.save()
                        return JsonResponse({"message":"Password Changed Succesfully"}, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({"message":"password and new password fields required"}, status=status.HTTP_400_BAD_REQUEST)


        else:
            return JsonResponse({"message":"user Doesnot Found"}, status=status.HTTP_404_NOT_FOUND)

class ForgotPasswordView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (AllowAny, )

    def post(self, request):
        email = request.data['email']
        user = User.objects.get(email=email)
        if email and user:
            if user.email == email:
                reset_code = ''.join([random.choice(string.ascii_uppercase + string.digits)for _ in range(6)])
                user.reset_link = reset_code
                user.save()
                return JsonResponse({"reset_code":user.reset_link})
    def put(self,request, format=None):
        message = ''
        reset_code = request.data['reset_link']
        password = request.data['password']
        if reset_code and password:
            user = User.objects.get(reset_link=reset_code)
            if user:
                # ser = UserSerializers(user)
                user.set_password(password)
                user.reset_link = ''
                user.save()
                ser = UserSerializers(user)
                message = 'Password Changed succesfully'
            else:
                message = 'incorrect reset_code'
        else:
            message = 'fields cent be empty'
        return JsonResponse({"message":message, "user":ser.data})
