# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.postgres.fields
from django.conf import settings
import platform.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('platform', '0007_auto_20151102_0714'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdSpot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('unique_code', models.CharField(default=platform.models.generate_unique_code, unique=True, max_length=300)),
                ('format', django.contrib.postgres.fields.ArrayField(base_field=models.SmallIntegerField(blank=True), size=8)),
            ],
        ),
        migrations.CreateModel(
            name='AdThematics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('image', models.ImageField(upload_to=b'')),
                ('format', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('thematics', models.ManyToManyField(to='platform.AdThematics', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPixel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('unique_code', models.CharField(default=platform.models.generate_unique_code, unique=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='UserSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('thematics', models.ManyToManyField(to='platform.AdThematics', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userpixel',
            name='site',
            field=models.ForeignKey(to='platform.UserSite'),
        ),
        migrations.AddField(
            model_name='banner',
            name='campaign',
            field=models.ForeignKey(to='platform.Campaign'),
        ),
        migrations.AddField(
            model_name='adspot',
            name='site',
            field=models.ForeignKey(to='platform.UserSite'),
        ),
    ]
