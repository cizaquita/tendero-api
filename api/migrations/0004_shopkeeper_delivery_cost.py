# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151201_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='delivery_cost',
            field=models.FloatField(default=2000),
        ),
    ]
