# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rotator', '0010_auto_20151103_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpixel',
            name='thematics',
        ),
        migrations.AddField(
            model_name='usersite',
            name='thematics',
            field=models.ManyToManyField(to='rotator.AdThematics', blank=True),
        ),
    ]
