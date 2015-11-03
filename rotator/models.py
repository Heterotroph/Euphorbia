from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from  django.contrib.postgres.fields import ArrayField
__author__ = 'igorzygin'

def generate_unique_code():
    return uuid.uuid4().hex[:15].upper()


class AdThematics(models.Model):
    def __unicode__(self):
        return self.name
    created = models.DateTimeField(default=datetime.now)
    name = models.CharField(max_length=100, blank=False)


class UserSite(models.Model):
    def __unicode__(self):
        return self.name+" "+self.url
    user = models.ForeignKey(User, unique=False)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.now)
    thematics = models.ManyToManyField(AdThematics, blank=True)


class UserPixel(models.Model):
    def __unicode__(self):
        return self.name+" "+self.unique_code
    site = models.ForeignKey(UserSite, unique=False)
    name = models.CharField(max_length=100, unique=True)
    unique_code = models.CharField(max_length=300, unique=True, default=generate_unique_code)





class AdSpot(models.Model):
    def __unicode__(self):
        return self.name+" "+self.unique_code
    created = models.DateTimeField(default=datetime.now)
    name = models.CharField(max_length=100, unique=True)
    unique_code = models.CharField(max_length=300, unique=True, default=generate_unique_code)
    site = models.ForeignKey(UserSite)
    format = ArrayField(models.SmallIntegerField(blank=True),size=8,)




class Campaign(models.Model):
    def __unicode__(self):
        return self.name
    created = models.DateTimeField(default=datetime.now)
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, unique=False)
    thematics = models.ManyToManyField(AdThematics, blank=True)

class Banner(models.Model):
    def __unicode__(self):
        return self.campaign.name+" "+str(self.id)+" "+str(self.format)
    created = models.DateTimeField(default=datetime.now)
    campaign = models.ForeignKey(Campaign)
    image = models.ImageField()
    format = models.SmallIntegerField(blank=False)




