from django.contrib import admin
from .models import User
# Register your models here.
admin.site.register(User)

from django.contrib import admin
from .models import User
from django.core.mail import send_mail

# class MyModelAdmin(admin.ModelAdmin):
#     actions = ['send__validation_email']

#     def send_validation_email(self, request, queryset):
#         # the below can be modified according to your application.
#         # queryset will hold the instances of your model
#         for profile in queryset:
#             send_email(subject="Invite", message="Hello", from_eamil='myemail@mydomain.com', recipient_list=[profile.email]) # use your email function here
#    send_invite.short_description = "Send invitation"

# admin.site.register(MyModel, MyModelAdmin)