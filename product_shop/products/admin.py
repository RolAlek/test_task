from django.contrib import admin

from .models import Category, Product, SubCategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'price', 'category', 'subcategory', 'image')

admin.site.register(Category)
admin.site.register(SubCategory)