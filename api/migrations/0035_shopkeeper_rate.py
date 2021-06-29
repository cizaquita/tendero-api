# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20160229_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='rate',
            field=models.FloatField(default=0),
        ),
    ]
