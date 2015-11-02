# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rotator', '0003_auto_20151017_0945'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPixel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('unique_code', models.CharField(unique=True, max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='campaign',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 17, 10, 30, 1, 803685), blank=True),
        ),
        migrations.AlterField(
            model_name='usersite',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 17, 10, 30, 1, 806055)),
        ),
        migrations.AddField(
            model_name='userpixel',
            name='site',
            field=models.ForeignKey(to='rotator.UserSite'),
        ),
    ]
