# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rotator', '0002_auto_20151017_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersite',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 17, 9, 45, 5, 680972)),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 17, 9, 45, 5, 678641), blank=True),
        ),
    ]
