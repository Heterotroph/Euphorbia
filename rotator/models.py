from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
__author__ = 'igorzygin'



class Campaign(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(blank=True, default=datetime.now())
    name = models.CharField(max_length=30)


class Banner(models.Model):
    campaign = models.ForeignKey(Campaign)
    banner_url = models.CharField(max_length=1000)


class ImageBanner(Banner):
    image_format = models.PositiveSmallIntegerField(blank=True, default=0)
    image = models.ImageField(blank=False)


class UserSite(models.Model):
    user = models.ForeignKey(User, unique=False)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.now())

