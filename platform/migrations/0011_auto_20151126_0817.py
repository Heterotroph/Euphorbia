# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('platform', '0010_banner_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='banner',
            name='format',
        ),
        migrations.RemoveField(
            model_name='adspot',
            name='format',
        ),
        migrations.AddField(
            model_name='adspot',
            name='format',
            field=models.ManyToManyField(to='platform.AdFormat', max_length=3),
        ),
    ]
