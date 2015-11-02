# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adboxweb', '0005_bannerrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign_name', models.CharField(max_length=100)),
                ('campaign_text', models.CharField(max_length=500)),
            ],
        ),
    ]
