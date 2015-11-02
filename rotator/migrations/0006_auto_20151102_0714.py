# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rotator', '0005_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='user',
        ),
        migrations.RemoveField(
            model_name='imagebanner',
            name='banner_ptr',
        ),
        migrations.AlterField(
            model_name='usersite',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 2, 7, 14, 37, 517462)),
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
        migrations.DeleteModel(
            name='Campaign',
        ),
        migrations.DeleteModel(
            name='ImageBanner',
        ),
    ]
