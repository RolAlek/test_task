from products.models import Category, Product, SubCategory
from rest_framework import serializers


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
