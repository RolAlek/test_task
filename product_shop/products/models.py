from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image

IMG_VERSIONS = {
    "thumb_image": (500, 500),
    "small_image": (800, 800),
    "large_image": (1200, 1200),
}


class BaseModel(models.Model):
    name = models.CharField(max_length=128, verbose_name="Наименование")
    slug = models.SlugField(unique=True, verbose_name="Идентификатор")

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        abstract = True


class Category(BaseModel):
    image = models.ImageField(upload_to="category/images/")


class SubCategory(BaseModel):
    image = models.ImageField(upload_to="category/subcategory/images/")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="sub_categories",
    )


class Product(BaseModel):
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        verbose_name="Подкатегория",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name="Цена",
    )
    image = models.ImageField(upload_to="products/original/")
    thumb_image = models.ImageField(upload_to="products/images/")
    small_image = models.ImageField(upload_to="products/images/")
    large_image = models.ImageField(upload_to="products/images/")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if self.image:
            img = Image.open(self.image)

            for version_name, size in IMG_VERSIONS.items():
                resized_img = img.resize(
                    size,
                    Image.Resampling.LANCZOS,
                )
                buffer = BytesIO()
                resized_img.save(buffer, format=img.format)

                getattr(self, version_name).save(
                    f"{version_name}_{self.image.name}",
                    ContentFile(buffer.getvalue()),
                    save=False,
                )
        super(Product, self).save(*args, **kwargs)
