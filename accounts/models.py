from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    # age User delete shud profile o ham delete kon
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(
        max_length=120, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    city = models.CharField(default='تهران',
                            max_length=30, blank=True)
    address = models.CharField(max_length=1000, blank=True)
    phone = models.IntegerField(blank=True, null=True, validators=[
                                MinValueValidator(11)])
    post_code = models.CharField(max_length=20, blank=True)
    image = models.ImageField(default='default.jpg',
                              upload_to='profile_image', blank=True)

    def __str__(self):
        return f'پروفایل : {self.user.username}'
