# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rotator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 9, 58, 8, 564526), blank=True),
        ),
    ]
