from django.contrib import admin
from .models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'phone', 'address', 'user_info')

    def user_info(self, obj):
        return obj.bio

    def get_queryset(self, request):  # in method baraye sort kardan e list hast
        queryset = super(ProfileAdmin, self).get_queryset(request)
        # ke inja bar asas e phon dare tartib mikone(az 0 ta 9 ke age manfi bezarim bar ax tartib michine)
        queryset = queryset.order_by('-phone', 'user')
        return queryset

    user_info.short_bio = 'Info'


admin.site.register(Profile, ProfileAdmin)
