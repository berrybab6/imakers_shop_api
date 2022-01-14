"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))

]
# CREATE function get_full_name(_first_name character varying, _last_name character varying)
#     returns character varying 
#     LANGUAGE plpgsql
# AS 
# $$
# declare
#     fullname character varying;
# Begin
#     select concat(us.first_name, ' ', us.last_name) into fullname
#     from users us
#     where us.first_name=_first_name and us.last_name=_last_name;


#     return fullname;
# end;
# $$;
  