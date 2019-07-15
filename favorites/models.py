from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from products.models import Product

# Create your models here.


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    favorited = models.BooleanField(default=False)

    def add_favorite(self, product_id):
        product = Product.objects.get(id=product_id)
        try:
            exist = FavoriteItem.objects.get(product=product, favorite=self)
            exist.save()
        except FavoriteItem.DoesNotExist:
            new = FavoriteItem.objects.create(product=product, favorite=self)
            new.save()

    def clear_from_favorite(self, product_id):
        product = Product.objects.get(pk=product_id)
        try:
            exist = FavoriteItem.objects.get(product=product, favorite=self)
            exist.delete()
        except FavoriteItem.DoesNotExist:
            pass

    def __str__(self):
        return self.user.username


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"محصول ' {self.product.title} ' در علاقه مندیهای ({self.favorite.user})"
