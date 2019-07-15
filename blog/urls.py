from django.urls import path
from .views import (blog_view,
                    post_list,
                    post_detail,
                    search,

                    post_create,
                    post_update,
                    post_delete,

                    post_like,

                    comment_approve,
                    comment_remove,
                    post_publish,
                    )

urlpatterns = [
    path('', blog_view, name='blog_view'),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:id>/<slug:slug>/detail/', post_detail, name='post_detail'),
    path('posts/<slug:cat_slug>/category/', post_list, name='post_category'),
    path('posts/<int:id>/<slug:slug>/like/', post_like, name='post_like'),

    path('posts/create/', post_create, name='post_create'),
    path('posts/<int:id>/<slug:slug>/update/', post_update, name='post_update'),
    path('posts/<int:id>/<slug:slug>/delete/', post_delete, name='post_delete'),



    # path('posts/add', PostCreate.as_view(), name='post_create'),
    # path('posts/<int:id>/<slug:slug>/update',
    #      PostUpdate.as_view(), name='post_update'),
    # path('posts/<int:id>/<slug:slug>/delete',
    #      PostDelete.as_view(), name='post_delete'),

    path('post/<int:id>/<slug:slug>/publish/',
         post_publish, name='post_publish'),

    path('result/', search, name='search'),

    path('comment/<int:id>/approve',
         comment_approve, name='comment_approve'),
    path('comment/<int:id>/remove',
         comment_remove, name='comment_remove'),

]
