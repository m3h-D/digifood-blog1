from django.contrib import admin
from .models import Product, Category, ProductComment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'available', 'special', 'category', 'price',
                    'stock', 'created', 'updated', 'id', ]
    # har field i ke in ja hast bayad to list_displaye ham bashe
    list_filter = ['created', 'category']
    list_editable = ['price', 'stock', 'special', 'available', 'category']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComment)
