# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_shopkeeper_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='delivery_time',
            field=models.IntegerField(default=10),
        ),
    ]
