from django.contrib import admin

# Register your models here.

from .models import Banner
from .models import Campaign

admin.site.register(Banner)
admin.site.register(Campaign)
