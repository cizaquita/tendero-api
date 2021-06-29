# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_shopkeeper_store_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='username',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
