# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopkeeper',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(default=b'POINT(0.0 0.0)', srid=4326),
        ),
    ]
