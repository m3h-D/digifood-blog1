from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(blank=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'کتگوری'
        verbose_name_plural = 'کتگوری ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class ProductManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)  # Product.objects. ...
        if qs.count() == 1:
            return qs.first()
        return None

    # def get_queryset(self):
    #     return ProductQuerySet(self.model, using=self.db)

    # def search(self, query=None):
    #     return self.get_queryset().search(query=query)


class Product(models.Model):
    # ye many to one relationship e(ke mige ye product moteallegh be ye category e , ye category shamele chand product e)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    # baraye sakhte URL ha estefade mishe
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=100000, decimal_places=0)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    special = models.BooleanField(default=False)
    special2 = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    image = models.ImageField(blank=False, default='product.jpg')
    image2 = models.ImageField(blank=True, null=True, default='product.jpg')
    image3 = models.ImageField(blank=True, null=True, default='product.jpg')

    objects = ProductManager()

    class Meta:
        ordering = ('-created',)
        # chun ma mikhaym bar asas e id o slug to query biarim
        index_together = (('id', 'slug'),)
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

    def approve_comments(self):
        self.comment.filter(approved_comment=True)

    @property
    def get_comments(self):
        return self.comment.all().order_by('-timestamp')


class ProductComment(models.Model):
    product = models.ForeignKey(
        Product, related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
    is_good = models.BooleanField(default=False)
    is_bad = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'کامنت محصوت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'{ self.user.username }---{ self.product.title }'

    def approve(self):
        self.approved_comment = True
        self.save()

    def good(self):
        self.is_good = True
        self.save()

    def bad(self):
        self.is_bad = True
        self.save()

    def get_absolute_url(self):
        return reverse('product_list')
