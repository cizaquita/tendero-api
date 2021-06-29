# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20151207_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='Order',
            field=models.ForeignKey(to='api.Order'),
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='Product',
            field=models.ForeignKey(to='api.Product'),
        ),
    ]
