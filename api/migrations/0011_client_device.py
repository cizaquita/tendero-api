# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_shopkeeper_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='device',
            field=models.TextField(null=True, blank=True),
        ),
    ]
