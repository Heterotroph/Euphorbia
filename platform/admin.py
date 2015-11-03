from django.contrib import admin

# Register your models here.

from .models import UserPixel, UserSite, AdSpot, Campaign, Banner, AdThematics

admin.site.register(UserPixel)
admin.site.register(UserSite)
admin.site.register(AdSpot)
admin.site.register(Campaign)
admin.site.register(Banner)
admin.site.register(AdThematics)
