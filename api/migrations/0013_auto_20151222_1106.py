# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_order_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_verification',
            new_name='address_detail',
        ),
        migrations.RemoveField(
            model_name='address',
            name='neighborhood',
        ),
        migrations.RemoveField(
            model_name='address',
            name='telephone',
        ),
        migrations.AddField(
            model_name='client',
            name='telephone',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
    ]
