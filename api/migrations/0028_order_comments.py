# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_shopkeeper_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
    ]
