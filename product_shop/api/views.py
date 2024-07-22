from django.contrib.auth import get_user_model
from products.models import Category, Product
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .serialazers import (
    CategorySerializer,
    ProductSerializer,
    UserReadSerializer,
    UserRegisterSerializer,
)

user = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer
        return UserReadSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    pass
