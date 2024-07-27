from http import HTTPStatus

from django.http import Http404
from django.shortcuts import get_object_or_404
from products.models import Product
from rest_framework.response import Response
from users.models import ShoppingCart, ShoppingCartItem

from .serialazers import ShoppingCartSerializer


def add_to_cart(request, cart, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
    except Http404:
        return Response(
            {"detail": "Такого продукта нет."},
            status=HTTPStatus.NOT_FOUND,
        )
    except ValueError:
        return Response(
            {"detail": "Некорректный id."},
            status=HTTPStatus.BAD_REQUEST,
        )

    cart_item, created = ShoppingCartItem.objects.get_or_create(
        cart=cart,
        product=product,
        quantity=1,
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    serializer = ShoppingCartSerializer(data=cart_item)
    return Response(serializer.data, status=HTTPStatus.CREATED)


def update_cart(request, cart, product_id, quantity):
    if quantity is None or quantity < 1:
        return Response(
            {"detail": "Некорректное количество товара."},
            status=HTTPStatus.BAD_REQUEST,
        )
    cart_item = get_object_or_404(
        ShoppingCartItem,
        cart=cart,
        product=product_id,
    )
    cart_item.quantity = quantity
    cart_item.save()
    serializer = ShoppingCartSerializer(cart_item)
