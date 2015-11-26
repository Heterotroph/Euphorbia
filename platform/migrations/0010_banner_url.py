# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platform', '0009_auto_20151109_0744'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='url',
            field=models.CharField(default='http://yandex.com', max_length=255),
            preserve_default=False,
        ),
    ]
