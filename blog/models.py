from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from tinymce import HTMLField

from django.contrib.auth import get_user_model
from accounts.models import Profile


User = get_user_model()

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:list_by_category', args=[self.slug])


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(
        max_length=100, db_index=True, blank=True)
    image = models.ImageField(blank=False, default='post.jpg')
    text = models.TextField()
    content = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    like = models.ManyToManyField(User, related_name='like', blank=True)

    categories = models.ManyToManyField(Category)
    special = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{ self.title } توسط { self.author.user }'

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save()

    def approve_comments(self):
        self.comments.filter(approved_comment=True)

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id, self.slug])

    def get_like_url(self):
        return reverse('blog:post_like', args=[self.id, self.slug])

    def get_update_url(self):
        return reverse('blog:post_update', args=[self.id, self.slug])

    def get_delete_url(self):
        return reverse('blog:post_delete', args=[self.id, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
    is_good = models.PositiveIntegerField(default=0)
    is_bad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{ self.user.username }---{ self.post.title }'

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')
