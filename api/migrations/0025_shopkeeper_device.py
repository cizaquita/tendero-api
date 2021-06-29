# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_shopkeeper_telephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='device',
            field=models.TextField(null=True, blank=True),
        ),
    ]
