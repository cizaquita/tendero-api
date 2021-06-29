# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
