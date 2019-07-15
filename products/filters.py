from django.contrib.auth.models import User
import django_filters

from django import forms
from .models import Product


class ProductFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'جدید ترین'),
        ('descending', 'قدیمی ترین')
    )

    CHOICES2 = (
        ('ascending', 'بیشترین'),
        ('descending', 'کمترین'),
    )

    CHOICES3 = (
        ('ascending', 'آ-ی'),
        ('descending', 'ی-آ'),
    )

    ordering = django_filters.ChoiceFilter(
        label='زمان تولید', choices=CHOICES, method='filter_by_order_created')

    ordering2 = django_filters.ChoiceFilter(
        label='قیمت', choices=CHOICES2, method='filter_by_order_price'
    )

    ordering3 = django_filters.ChoiceFilter(
        label='حروف الفبا', choices=CHOICES3, method='filter_by_order_title'
    )

    class Meta:
        model = Product
        fields = [
            'special',
        ]

    def filter_by_order_created(self, queryset, name, value):
        exp = '-created' if value == 'ascending' else 'created'
        return queryset.order_by(exp)

    def filter_by_order_price(self, queryset, name, value):
        exp = '-price' if value == 'ascending' else 'price'
        return queryset.order_by(exp)

    def filter_by_order_title(self, queryset, name, value):
        exp = 'title' if value == 'ascending' else '-title'
        return queryset.order_by(exp)
