# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20160421_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moteros',
            name='duty',
        ),
    ]
