# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rotator', '0009_auto_20151102_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdThematics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='thematics',
            field=models.ManyToManyField(to='rotator.AdThematics', blank=True),
        ),
        migrations.AddField(
            model_name='userpixel',
            name='thematics',
            field=models.ManyToManyField(to='rotator.AdThematics', blank=True),
        ),
    ]
