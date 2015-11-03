# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner_url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 9, 18, 8, 19, 26, 836057), blank=True)),
                ('name', models.CharField(max_length=30)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImageBanner',
            fields=[
                ('banner_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rotator.Banner')),
                ('image_format', models.PositiveSmallIntegerField(default=0, blank=True)),
                ('image', models.ImageField(upload_to=b'')),
            ],
            bases=('rotator.banner',),
        ),
        migrations.AddField(
            model_name='banner',
            name='campaign',
            field=models.ForeignKey(to='rotator.Campaign'),
        ),
    ]
