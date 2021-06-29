# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='rating',
            field=models.OneToOneField(null=True, blank=True, to='api.Rating'),
        ),
    ]
