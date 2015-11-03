# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platform', '0004_remove_banner_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_url', models.CharField(max_length=100)),
                ('banner_format', models.CharField(max_length=500)),
            ],
        ),
    ]
