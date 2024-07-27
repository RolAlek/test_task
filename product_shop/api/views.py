from django.contrib.auth import get_user_model
from products.models import Category, Product
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import ShoppingCart

from .serialazers import (
    CategorySerializer,
    ProductSerializer,
    ShoppingCartSerializer,
    UserReadSerializer,
    UserRegisterSerializer,
)
from .utils import add_to_cart, update_cart

user = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    @action(
        methods=["post", "delete", "patch"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, *args, **kwargs):
        user_cart = request.user.cart
        product_id = self.kwargs.get("pk")
        if request.method == "POST":
            return add_to_cart(request, user_cart, product_id)
        elif request.method == "PATCH":
            return update_cart(
                request,
                user_cart,
                product_id,
                self.kwargs.get("quantity"),
            )

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def user_cart(self, request, *args, **kwargs):
        cart = self.get_cart(request.user)
        cart_products = cart.products.all()
        serializer = ShoppingCartSerializer(cart_products, many=True)
        total_price = sum(item.product.price * item.quantity for item in cart_products)
        return Response(
            data={"items": serializer.data, "total_price": total_price},
        )

    def get_cart(self, user):
        cart, _ = ShoppingCart.objects.get_or_create(user=user)
        return cart


class UserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer
        return UserReadSerializer
