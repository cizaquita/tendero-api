# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20151222_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
