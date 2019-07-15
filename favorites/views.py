from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Favorite, FavoriteItem
from products.models import Product
from cart.models import CartItem, Cart

# Create your views here.


@login_required
def favorite_view(request):
    cart = Cart.objects.filter(user=request.user.id, active=True)
    items = CartItem.objects.filter(cart=cart.first())
    try:
        favorite = Favorite.objects.filter(user=request.user.id)
        fav = FavoriteItem.objects.filter(favorite=favorite.first())
    except ObjectDoesNotExist:
        favorite = Favorite.objects.create(user=request.user)
        fav = FavoriteItem.objects.filter(favorite=favorite.first())

    context = {
        'favorite': fav,
        'cart': items,
    }

    return render(request, 'favorites/favorite.html', context)


def add_favorite(request, product_id):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                favorite = Favorite.objects.get(user=request.user)
            except ObjectDoesNotExist:
                favorite = Favorite.objects.create(user=request.user)
                favorite.save()
            favorite.add_favorite(product_id)
            messages.success(
                request, f"محصول  ' {product.title} '  به لیست علاقه مندیها اضافه شد")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('login-view')


def clear_from_favorite(request, product_id):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            pass

        else:
            favorite = Favorite.objects.get(user=request.user.id)

            favorite.save()
        favorite.clear_from_favorite(product_id)

    else:
        return redirect('pages:home-page')

    return redirect('favorites:favorite_view')
