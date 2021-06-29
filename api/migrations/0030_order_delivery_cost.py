# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_cost',
            field=models.IntegerField(default=0),
        ),
    ]
