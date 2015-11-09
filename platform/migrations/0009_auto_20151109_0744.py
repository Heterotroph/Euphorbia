# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platform', '0008_auto_20151103_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='user',
            field=models.ForeignKey(to='users.User'),
        ),
        migrations.AlterField(
            model_name='usersite',
            name='user',
            field=models.ForeignKey(to='users.User'),
        ),
    ]
