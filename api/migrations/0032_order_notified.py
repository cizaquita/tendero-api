# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_shopkeeper_last_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notified',
            field=models.BooleanField(default=False),
        ),
    ]
