from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from django.utils import timezone

# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Post, Comment, Category
from .forms import CommentForm, PostForm

from accounts.models import Profile

# Create your views here.
User = get_user_model()


def get_author(user):
    author = Profile.objects.filter(user=user)
    if author.exists():
        return author.first()
    return None


def cat_count():
    cate = Post.objects.values(
        'categories__title').annotate(Count('categories__title'))
    return cate


def blog_view(request):
    posts = Post.objects.filter(special=True)
    latest = Post.objects.order_by('-timestamp')[:3]
    categories = Category.objects.all().order_by('-id')

    context = {
        'posts': posts,
        'latest': latest,
        'categories': categories,
    }
    return render(request, 'blog/blog-view.html', context)


def post_list(request, cat_slug=None, category=None):
    category_count = cat_count()
    post_list = Post.objects.all().order_by('-timestamp')
    latest = Post.objects.order_by('-timestamp')[:3]

    categories = Category.objects.all().order_by('title')

    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        post_list = post_list.filter(categories=category)

    paginator = Paginator(post_list, 4)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)
    context = {
        'post_list': post_list,
        'posts': post_list,
        'page': page,
        'latest': latest,
        'category_count': category_count,
        'categories': categories,
        'category': category,
    }
    return render(request, 'blog/post.html', context)


def post_detail(request, id, slug):
    category_count = cat_count()
    latest = Post.objects.order_by('-timestamp')[:3]
    categories = Category.objects.all().order_by('title')

    post = get_object_or_404(Post, id=id, slug=slug)
    post.view_count = post.view_count + 1
    post.save()

    is_liked = False
    if post.like.filter(id=request.user.id).exists():
        is_liked = True

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect('blog:post_detail', id=id, slug=slug)

    context = {
        'post': post,
        'latest': latest,
        'category_count': category_count,
        'form': form,
        'is_liked': is_liked,
        'categories': categories,
    }
    return render(request, 'blog/post-detail.html', context)


@staff_member_required
def post_create(request):
    title = 'ساخت پست جدید'
    author = get_author(request.user)
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog:post_detail", kwargs={'id': form.instance.id,
                                                                'slug': form.instance.slug}))
    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'blog/post_form.html', context)


@staff_member_required
def post_update(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    title = f'(ویرایش پست ({post.title}'
    author = get_author(request.user)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog:post_detail", kwargs={'id': form.instance.id,
                                                                'slug': form.instance.slug}))
    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'blog/post_form.html', context)


def post_delete(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    post.delete()
    return redirect(reverse('blog:post_list'))


def post_like(request, id, slug, is_liked=False):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=request.POST.get('post_id'))

        if post.like.filter(id=request.user.id).exists():
            post.like.remove(request.user)
            is_liked = False
        else:
            post.like.add(request.user)
            is_liked = True
        return redirect(post.get_absolute_url())
    else:
        post = get_object_or_404(Post, id=id, slug=slug)
        messages.success(
            request, f"برای لایک کردن پست  ( {post.title} ) باید ثبت نام/وارد شوید")
        return redirect(post.get_absolute_url())


def search(request):
    category_count = cat_count()
    latest = Post.objects.order_by('-timestamp')[:3]

    result = Post.objects.all()
    query = request.GET.get('q')
    if query:
        result = Post.objects.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(content__icontains=query)).distinct()

    paginator = Paginator(result, 4)
    page = request.GET.get('page')
    result = paginator.get_page(page)

    context = {
        'query': query,
        'result': result,
        'page': page,
        'latest': latest,
        'category_count': category_count,

    }
    return render(request, 'blog/search.html', context)


@login_required
def post_publish(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    post.publish
    return redirect('blog:post_detail', id=id, slug=slug)


@staff_member_required
def comment_approve(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.approve()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect('blog:post_detail', id=comment.post.id)


@staff_member_required
def comment_remove(request, id):
    comment = get_object_or_404(Comment, id=id)
    # post_id = comment.post.id
    # post_slug = comment.post.slug
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect('blog:post_detail', id=post_id)
