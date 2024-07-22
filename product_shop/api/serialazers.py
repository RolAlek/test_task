from products.models import Category, Product, SubCategory
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import ShoppingCart

user = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("name", "slug", "image", "sub_categories")


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SubCategory
        fields = ("name", "slug", "image", "category")


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "price",
            "category",
            "subcategory",
            "thumb_image",
            "small_image",
            "large_image",
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        new_user = user.objects.create_user(**validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'product', 'quantity')