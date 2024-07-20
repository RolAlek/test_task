from django.db import models


class BaseCategoryModel(models.Model):
    name = models.CharField(max_length=128, verbose_name='Категория')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор')
    image = models.ImageField(upload_to='products/images/')

    class Meta:
        abstract = True


class Category(BaseCategoryModel):
    pass


class SubCategory(BaseCategoryModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
