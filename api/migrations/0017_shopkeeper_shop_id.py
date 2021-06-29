# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20160120_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='shop_id',
            field=models.IntegerField(default=0),
        ),
    ]
