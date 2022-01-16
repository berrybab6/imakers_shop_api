from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
# Create your models here.


class Role(models.Model):
    ADMIN = 1
    CUSTOMER = 2

    SHOPOWNER = 3
   
    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (CUSTOMER, 'customer'),
        (SHOPOWNER, 'shopowner'),
      
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()



class UserManager(BaseUserManager):

    def create_user(self, username, email,phone_number=None, full_name=None, gender=None, profile_url=None, is_validated=False,reset_link=None,is_admin=False, is_staff=False,is_customer=False,is_shop_owner=False,business_id=None, password=None, is_active=True,):
        if not username:
            raise ValueError("User Must have an username")
        if not password:
            raise  ValueError("User Must have a Password")
        user = self.model(username=username)
        user.set_password(password)
        user.active = is_active
        
        user.gender = gender
        user.profile_url =profile_url
        user.username = username
        user.business_id = business_id            
        user.reset_link = reset_link
        user.full_name = full_name
        user.phone_number = phone_number
        user.email = email
        user.is_validated = is_validated
        user.shop_owner = is_shop_owner
        user.staff = is_staff
        user.customer = is_customer 
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username,full_name=None,phone_number=None, password=None, profile_url=None):

        user = self.create_user(username, email,full_name=full_name,phone_number=phone_number,profile_url=profile_url, is_staff=True,password=password,is_admin=True)
        return user
    
    def create_staffuser(self, username,email, full_name=None, password=None):
        user = self.create_user(username,email, full_name=full_name, is_staff=True,password=password)
        return user
    def create_shop_owner(self,email, username, phone_number=None, full_name=None, password=None, profile_url=None):
        user = self.create_user(username, email,phone_number=phone_number,full_name=full_name, password=password,profile_url=profile_url, is_shop_owner=True)
        return user
    def create_customer(self, email, username, phone_number=None,full_name=None,profile_url=None,is_validated=False, gender=None, reset_link=None, password=None):
        user = self.create_user(email, username, phone_number=phone_number,full_name=full_name,is_validated=is_validated,gender=gender,profile_url=profile_url, reset_link=reset_link, password=password, is_customer=True)
        return user
class User(AbstractUser):
    # roles = models.OneToOneField(Role, on_delete=models.CASCADE, null=True)
    username = models.CharField(unique=True, max_length=100)
    
    gender = models.CharField(max_length=6,null=True, blank=True)
    profile_url = models.ImageField(upload_to="users")
    business_id = models.ImageField(upload_to="owners")

    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    shop_owner = models.BooleanField(default=False)
    customer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100,unique=True,null=False)
    created_At = models.DateTimeField(auto_now_add=True)
    
    full_name = models.CharField(max_length=255, blank=True, null=True)
    reset_link = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    is_validated = models.BooleanField(default=False)
    

    # comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="user", default=None, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    def __str__(self):
        return self.username
    def get_full_name(self):
        return self.full_name
    def get_short_name(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_customer(self):
        return self.customer
    @property
    def is_shop_owner(self):
        return self.shop_owner
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)