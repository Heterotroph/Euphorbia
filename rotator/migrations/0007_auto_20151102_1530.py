# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import rotator.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rotator', '0006_auto_20151102_0714'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdSpot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('unique_code', models.CharField(default=rotator.models.generate_unique_code, unique=True, max_length=300)),
                ('format', django.contrib.postgres.fields.ArrayField(base_field=models.SmallIntegerField(blank=True), size=8)),
            ],
        ),
        migrations.AlterField(
            model_name='userpixel',
            name='unique_code',
            field=models.CharField(default=rotator.models.generate_unique_code, unique=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='usersite',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 2, 15, 30, 35, 745294)),
        ),
        migrations.AddField(
            model_name='adspot',
            name='site',
            field=models.ForeignKey(to='rotator.UserSite'),
        ),
    ]
