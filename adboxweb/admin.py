from django.contrib import admin

# Register your models here.

from .models import Banner
from .models import Campaign
from .models import CampaignList, Site, CampaignRequest, BannerRequest

admin.site.register(Banner)
admin.site.register(Campaign)
admin.site.register(CampaignList)
admin.site.register(Site)
admin.site.register(CampaignRequest)
admin.site.register(BannerRequest)