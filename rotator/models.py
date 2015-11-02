from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
__author__ = 'igorzygin'



class UserSite(models.Model):
    user = models.ForeignKey(User, unique=False)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.now())


class UserPixel(models.Model):
    site = models.ForeignKey(UserSite, unique=False)
    name = models.CharField(max_length=100, unique=True)
    unique_code = models.CharField(max_length=300, unique=True)

    def generate_unique_code(self):
        return uuid.uuid4().hex[:15].upper()

