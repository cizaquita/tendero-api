# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20151207_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='api.Product', through='api.OrderProducts'),
        ),
    ]
