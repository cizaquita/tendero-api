# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_shopkeeper_delivery_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='open',
            field=models.BooleanField(default=False),
        ),
    ]
