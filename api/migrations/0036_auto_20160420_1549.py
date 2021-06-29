# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_shopkeeper_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='square_range',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='shopkeeper',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(default=b'POINT(4.673498 -74.063333)', srid=4326),
        ),
    ]
