# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_shopkeeper_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
