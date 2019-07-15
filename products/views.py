from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .models import Product, Category, ProductComment
from favorites.models import FavoriteItem, Favorite
from django.views.generic import View
from cart.models import Cart, CartItem
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .filters import ProductFilter
from .forms import CommentForm
from accounts.models import Profile


# list product ha.


def product_list_view(request, cat_slug=None):
    message = messages.get_messages(request)
    cart = Cart.objects.filter(user=request.user.id, active=True)
    items = CartItem.objects.filter(cart=cart.first())  # baraye counter
    category = None

    categories = Category.objects.all().order_by(
        '-id')  # kolle category ha bedoone slug
    products = Product.objects.filter(available=True)

    paginator = Paginator(products, 6)  # paginator baraye P_list_view
    page = request.GET.get('page')

    # baraye dast resi be product e har page... age ino nazarim to har page faqat 3 post e akha ro neshun mide
    products = paginator.get_page(page)
    filter = ProductFilter(
        request.GET, queryset=Product.objects.all())
    if cat_slug:
        products = Product.objects.filter(available=True)
        # age ino dobare taarif nakonim products o paginator minine o dg produvt.obj bar nemigardoone
        category = get_object_or_404(Category, slug=cat_slug)
        # mire donbale product aei ke category e bala ro daran o peyda mikone
        products = products.filter(category=category)
        paginator = Paginator(products, 6)  # paginator baraye C_list_view
        page = request.GET.get('page')
        products = paginator.get_page(page)

    context = {
        'category': category,
        'categories': categories,
        'products': products,

        'page': page,
        'cart': items,
        'message': message,
        'filter': filter,


    }
    return render(request, 'products/products_list.html', context)

#  ----------------- class detail base view ke nemifahmam------------

# class ProductDetailSlugView(DetailView):
#     model = Product  # beja get_object

#     context_object_name = 'product'
#     template_name = 'products/product_detail.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         cart_obj, new_obj = Cart.objects.new_or_get(self.request)
#         context['cart'] = cart_obj
#         return context

# ----- get_object ham nabashe baz okeye ------------------

    # def get_object(self, *args, **kwargs):
    #     request = self.request
    #     message = messages.get_messages(request)
    #     slug = self.kwargs.get('slug_detail')
    #     try:
    #         instance = Product.objects.get(slug=slug)
    #     except Product.DoesNotExist:
    #         raise Http404('پیدا نشد!')
    #     except Product.MultipleObjects.Returned:
    #         qs = Product.objects.filter(slug=slug)
    #         instance = qs.first()
    #     except:
    #         raise Http404('hmmmm...')
    #     return instance

#  ---------------func e khudam...------------------------


def product_detail_view(request, pk, slug):
    cart = Cart.objects.filter(user=request.user.id, active=True)
    items = CartItem.objects.filter(cart=cart.first())

    product = get_object_or_404(Product, pk=pk, slug=slug)
    fav_counter = FavoriteItem.objects.filter(product=product)
    message = messages.get_messages(request)

    same_cat = Product.objects.filter(
        category=product.category).exclude(pk=product.pk)[:3]

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.product = product
            form.save()
            return redirect('products:product_detail', pk=pk, slug=slug)

    context = {
        'product': product,
        'cart': items,
        'fav_counter': fav_counter,
        'message': message,
        'form': form,
        'same_cat': same_cat,

    }
    return render(request, 'products/product_detail.html', context)
# --------------------------------------------------------------


def search_view(request):
    cart = Cart.objects.filter(user=request.user.id, active=True)
    items = CartItem.objects.filter(cart=cart.first())
    categories = Category.objects.all().order_by(
        '-id')

    query = request.GET.get('q')
    result = Product.objects.filter(available=True)
    # user_filter = UserFilter(request.GET, queryset=result)
    if query:
        result = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(slug__icontains=query)
        ).distinct()

    paginator = Paginator(result, 6)
    page = request.GET.get('page')
    result = paginator.get_page(page)

    context = {
        'query': query,
        'result': result,
        'page': page,
        'item': result,
        'cart': items,
        'categories': categories,
        # 'filter': user_filter,
    }

    return render(request, 'products/search.html', context)


class PaginatedFilterViews(View):
    def get_context_data(self, **kwargs):
        context = super(PaginatedFilterViews, self).get_context_data(**kwargs)
        if self.request.GET:
            querystring = self.request.GET.copy()
            if self.request.GET.get('page'):
                del querystring['page']
            context['querystring'] = querystring.urlencode()
        return context


def product_ordering(request):
    cart = Cart.objects.filter(user=request.user.id, active=True)
    items = CartItem.objects.filter(cart=cart.first())
    categories = Category.objects.all().order_by(
        '-id')

    product = Product.objects.filter(available=True)
    filter = ProductFilter(
        request.GET, queryset=product)

    paginator = Paginator(filter, 6)
    page = request.GET.get('page')
    # funds = paginator.get_page(page)

    context = {
        'filter': filter,
        # 'page': funds,
        'categories': categories,
        'cart': items,
    }
    return render(request, 'products/filter.html', context)


# -----------product comment -----------------
def get_author(user):
    author = Profile.objects.filter(user=user)
    if author.exists():
        return author[0]
    return None


@staff_member_required
def comment_approve(request, id):
    comment = get_object_or_404(ProductComment, id=id)
    comment.approve()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect('blog:post_detail', id=comment.post.id)


@staff_member_required
def comment_remove(request, id):
    comment = get_object_or_404(ProductComment, id=id)
    # post_id = comment.post.id
    # post_slug = comment.post.slug
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect('blog:post_detail', id=post_id)
