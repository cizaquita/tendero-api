# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shopkeeper',
            name='shop_id',
            field=models.BigIntegerField(default=0),
        ),
    ]
