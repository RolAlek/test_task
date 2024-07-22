from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product


class CustomUser(AbstractUser):
    pass


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Корзина пользователя",
        related_name="cart",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товары в корзине",
        related_name="cart",
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
