# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_order_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='image',
            field=models.ImageField(null=True, upload_to=b'shopkeepers', blank=True),
        ),
    ]
