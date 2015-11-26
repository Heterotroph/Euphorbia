# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platform', '0011_auto_20151126_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='format',
            field=models.ForeignKey(default=1, to='platform.AdFormat'),
            preserve_default=False,
        ),
    ]
