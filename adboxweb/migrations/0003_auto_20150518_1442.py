# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adboxweb', '0002_auto_20150513_0807'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='user',
        ),
        migrations.AddField(
            model_name='campaign',
            name='campaign_list',
            field=models.ForeignKey(to='adboxweb.CampaignList', null=True),
        ),
    ]
