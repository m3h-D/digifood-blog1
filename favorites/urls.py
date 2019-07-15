from django.urls import path
from .views import favorite_view, add_favorite, clear_from_favorite

urlpatterns = [
    path('', favorite_view, name='favorite_view'),
    path('add/<product_id>/', add_favorite,
         name='favorite_update_view'),
    path('clear/<product_id>/', clear_from_favorite, name='clear_from_favorite'),
]
