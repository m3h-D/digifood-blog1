from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash
)
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, RegisterForm, ProfileUpdateForm, UserUpdateForm

from cart.models import CartItem, Cart

# Create your views here.


def login_view(request):
    next = request.GET.get('next')  # rol e redirect o dare
    if request.user.is_authenticated:
        if next:
            return redirect(next)
        return redirect('profile-view')
    else:

        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # user o migire
            password = form.cleaned_data.get('password')  # pass o migire
            # to ye auth mizare user , pass o
            user = authenticate(username=username, password=password)
            # az built-in login estefade mikone ta karbar o login kone
            login(request, user)
            if next:
                return redirect(next)
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('pages:home-page')
    else:
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            # user = form.save(commit=False)
            # password1 = form.cleaned_data.get('password1')
            # password2 = form.cleaned_data.get('password2')
            # user.save()
            form.save()

            # username o mishe to HTML farakhani kard
            username = form.cleaned_data.get('username')
            # password1 o mishe to HTML farakhani kard
            raw_password = form.cleaned_data.get('password1')
            # to inja user o baad az sabte nam login mikone
            new_user = authenticate(username=username, password=raw_password)
            login(request, new_user)

            return redirect('pages:home-page')

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request, *args, **kwargs):
    logout(request, *args, **kwargs)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def profile_edit(request):
    cart = Cart.objects.filter(user=request.user.id, active=True)
    items = CartItem.objects.filter(cart=cart.first())
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'پروفایل شما بروز رسانی شد')
            return redirect('profile-view')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'cart': items
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def profile(request):
    cart = Cart.objects.filter(user=request.user.id, active=True)
    items = CartItem.objects.filter(cart=cart.first())
    message = messages.get_messages(request)

    return render(request, 'accounts/profile.html', {'messages': message, 'cart': items})


@login_required
def change_password_view(request):
    items = CartItem.objects.all()
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'پسورد شما تغییر کرد!')
            update_session_auth_hash(request, form.user)
            return redirect('profile-view')
        else:
            messages.error(request, f'اشتباهی پیش امده')
            return redirect('change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        context = {
            'form': form,
            'cart': items,
        }
        return render(request, 'accounts/change_password.html', context)
