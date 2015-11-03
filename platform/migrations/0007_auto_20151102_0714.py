# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platform', '0006_campaignrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='site',
        ),
        migrations.DeleteModel(
            name='BannerRequest',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='campaign_list',
        ),
        migrations.RemoveField(
            model_name='campaignlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='CampaignRequest',
        ),
        migrations.RemoveField(
            model_name='site',
            name='user',
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
        migrations.DeleteModel(
            name='Campaign',
        ),
        migrations.DeleteModel(
            name='CampaignList',
        ),
        migrations.DeleteModel(
            name='Site',
        ),
    ]
