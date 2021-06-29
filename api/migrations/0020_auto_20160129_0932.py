# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20160128_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopkeeper',
            name='delivery_time',
        ),
        migrations.AddField(
            model_name='shopkeeper',
            name='document',
            field=models.BigIntegerField(default=0),
        ),
    ]
