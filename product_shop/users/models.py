from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product


class CustomUser(AbstractUser):
    pass


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Корзина пользователя",
        related_name="cart",
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name="item",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар в корзине",
        related_name="cart",
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
