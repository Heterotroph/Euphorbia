from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Site(models.Model):
    user = models.ForeignKey(User, unique=False)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    def __str__(self):
        return '('+str(self.id)+') '+self.name

class BannerRequest(models.Model):
    site_url = models.CharField(max_length=100)
    banner_format = models.CharField(max_length=500)

class CampaignRequest(models.Model):
    campaign_name = models.CharField(max_length=100)
    campaign_text = models.CharField(max_length=500)


class Banner(models.Model):
    adriver_id = models.CharField(max_length=100)
    url_snippet = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    site = models.ForeignKey(Site)
    def __str__(self):
        return '('+str(self.id)+') '+self.name

class CampaignList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, unique=False)
    def __str__(self):
        return '('+str(self.id)+') '+self.name


class Campaign(models.Model):
    campaign_list = models.ForeignKey(CampaignList,unique=False, null=True)
    adriver_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    def __str__(self):
        return '('+str(self.id)+') '+self.name
