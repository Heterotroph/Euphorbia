from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models

__author__ = 'igorzygin'

class ClientManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        # if not username:
        # raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.email

    objects = ClientManager()

    phone = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=100, blank=True, unique=True)
    roles = ArrayField(models.SmallIntegerField(blank=True),size=3, default=[])

    date_joined = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user can log into this admin '
                                               'site.')

    USERNAME_FIELD = 'email'

