# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20160129_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='store_code',
            field=models.BigIntegerField(default=0),
        ),
    ]
