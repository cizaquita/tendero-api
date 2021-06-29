# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151202_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, to='api.Address', null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to=b'categories', blank=True),
        ),
    ]
