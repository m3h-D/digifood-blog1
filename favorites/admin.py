from django.contrib import admin
from .models import Favorite, FavoriteItem

admin.site.register(FavoriteItem)

admin.site.register(Favorite)

# Register your models here.
