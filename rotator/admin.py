from django.contrib import admin

# Register your models here.

from .models import UserPixel, UserSite

admin.site.register(UserPixel)
admin.site.register(UserSite)
