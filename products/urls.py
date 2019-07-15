from django.urls import path
from .views import(
    product_list_view,
    search_view,
    product_detail_view,
    product_ordering,
    comment_approve,
    comment_remove,

    # ProductDetailSlugView,
)


urlpatterns = [
    path('list/', product_list_view, name='product_list'),
    path('results/', search_view, name='search'),
    path('order/', product_ordering, name='ordering'),

    path('category/<slug:cat_slug>/', product_list_view,
         name='product_list_by_category'),
    path('<pk>/<slug>/',
         product_detail_view, name='product_detail'),
    path('comment/<int:id>/approve',
         comment_approve, name='comment_approve'),
    path('comment/<int:id>/remove',
         comment_remove, name='comment_remove'),

]
