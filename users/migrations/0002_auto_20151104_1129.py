# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=django.contrib.postgres.fields.ArrayField(default=[], base_field=models.SmallIntegerField(blank=True), size=3),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
