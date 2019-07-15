from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Cart, CartItem
from products.models import Product
from accounts.forms import UserUpdateForm, ProfileUpdateForm
from accounts.models import Profile


# @login_required
# def maketotal(request):
#     cart = Cart.objects.filter(user=request.user.id, active=True)
#     items = CartItem.objects.filter(cart=cart.first())

#     total = 0
#     count = 0
#     for item in items:
#         total += (item.product.price * item.quantity)
#         count += item.quantity

#     context = {
#         'cart': items,
#         'total': total,
#         'count': count,
#     }
#     return (context['total'])


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:  # id i ke vojod nadashte bashe vase ye product
            pass

        else:
            try:
                cart = Cart.objects.get(user=request.user, active=True)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(user=request.user)
                cart.save()
            if product.stock == 0:
                product.save()
                messages.success(
                    request, f"محصول  '{product.title}'  به تعدادکافی موجود نیست")
                return redirect('cart:cart')
            else:
                product.stock -= 1
                product.save()
            cart.add_to_cart(product_id)

        return redirect('cart:cart')

    else:
        return redirect('login-view')


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            pass

        else:
            cart = Cart.objects.get(user=request.user, active=True)
            cart.remove_from_cart(product_id)
            product.stock += 1
            product.save()

        return redirect('cart:cart')
    else:
        return redirect('pages:home-page')


def clear_from_cart(request, product_id):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            pass

        else:
            cart = Cart.objects.get(user=request.user.id, active=True)
            cart.clear_from_cart(product_id)

        return redirect('cart:cart')
    else:
        return redirect('pages:home-page')


def clear_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user, active=True)
        items = CartItem.objects.filter(cart=cart)
        for item in items:
            item.clear_cart(request)

        return redirect('cart:cart')
    else:
        return redirect('pages:home-page')


def get_total_price(request):
    cart = Cart.objects.get(user=request.user.id, active=True)
    return cart.total


@login_required
def cart(request):
    message = messages.get_messages(request)
    # cart, new_obj = Cart.objects.new_or_get(request)
    # items = cart.product.all()
    # ---------------[asli]--------------------------------
    try:
        cart = Cart.objects.get(user=request.user.id, active=True)
        items = CartItem.objects.filter(cart=cart)
    except ObjectDoesNotExist:
        cart = Cart.objects.create(user=request.user)
        items = CartItem.objects.filter(cart=cart)
    # -----------------------------------------------------

    total = 0
    count = 0
    for item in items:
        total += (item.product.price * item.quantity)
        count += item.quantity
    cart.total = total
    cart.save()

    context = {
        'cart': items,
        'total': total,
        'count': count,
        'messages': message,

    }

    return render(request, 'cart/detail.html', context)


@login_required
def bank_view(request):
    try:
        cart = Cart.objects.get(user=request.user.id, active=True)
        items = CartItem.objects.filter(cart=cart)
    except ObjectDoesNotExist:
        cart = Cart.objects.create(user=request.user)
        items = CartItem.objects.filter(cart=cart)
    total = cart.total

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('zarinpal:request')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'cart': items,
        'total': total
    }
    return render(request, 'cart/bank.html', context)


def add_to_cart_product_list(request, product_id):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:  # id i ke vojod nadashte bashe vase ye product
            pass

        else:
            try:
                cart = Cart.objects.get(user=request.user, active=True)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(user=request.user)
                cart.save()
            if product.stock == 0:
                product.save()
                messages.success(
                    request, f"محصول  '{product.title}'  به تعدادکافی موجود نیست")
                return redirect('cart:cart')
            else:
                product.stock -= 1
                product.save()
            cart.add_to_cart(product_id)
            messages.success(
                request, f"محصول  '{product.title}' به سبد خرید اضافه شد")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return redirect('login-view')


# @require_POST
# def add_to_cart(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)

#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'], update_quantity=cd['update'])
#     return redirect('cart:cart_detail')

# def remove_from_cart(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')

# def cart_detail(request):
#     cart = Cart(request)
#     for item in cart:
#         item['update_quantity_form'] = CartAddProductForm(
#             initial={'quantity': item['quantity'], 'update': True})

#     return render(request, 'cart/detail.html', {'cart': cart})
