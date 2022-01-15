from django.contrib import admin
from vendor.models import Product

from vendor.models import Category, Color, Product, ProductDetail, Shop, Size, Type

# Register your models here.






admin.site.register(Shop)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(Category)
admin.site.register(Type)

