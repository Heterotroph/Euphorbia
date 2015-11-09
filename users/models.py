from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

__author__ = 'igorzygin'


class User(AbstractBaseUser):
    def __unicode__(self):
        return self.name

    phone = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    roles = ArrayField(models.SmallIntegerField(blank=True),size=3, default=[])
