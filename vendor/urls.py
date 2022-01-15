from django.urls.conf import path, include
from rest_framework import routers
from . import views

app_name = 'product'
router = routers.DefaultRouter()
router.register('product_list', views.ProductListView)

urlpatterns = [
    path('', include(router.urls))
]
