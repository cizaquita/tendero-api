# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_shopkeeper_shop_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.IntegerField(default=0),
        ),
    ]
