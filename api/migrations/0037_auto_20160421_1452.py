# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20160420_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moteros',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('plate', models.CharField(max_length=16)),
                ('duty', models.BooleanField(default=False)),
                ('type', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='motero',
            field=models.ForeignKey(blank=True, to='api.Moteros', null=True),
        ),
    ]
