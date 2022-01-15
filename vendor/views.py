from django.shortcuts import render
from rest_framework import serializers, viewsets
from . import seriliazer
from . import models


# Create your views here.

class ProductListView(viewsets.ModelViewSet):
    serializer_class = seriliazer.ProductListSerializer
    queryset = models.Product.objects.all()

    def get_queryset(self):
        return super().get_queryset()
