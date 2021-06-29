# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_order_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.IntegerField(default=0),
        ),
    ]
