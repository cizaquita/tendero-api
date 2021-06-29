# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_order_notified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('client', models.ForeignKey(to='api.Client')),
                ('order', models.ForeignKey(to='api.Order')),
                ('shopkeeper', models.ForeignKey(to='api.ShopKeeper')),
            ],
        ),
    ]
