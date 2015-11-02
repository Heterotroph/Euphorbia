# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adboxweb', '0003_auto_20150518_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='user',
        ),
    ]
