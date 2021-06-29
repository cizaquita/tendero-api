# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_order_delivery_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='last_active',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
