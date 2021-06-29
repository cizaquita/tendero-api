# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_order_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shopkeeper',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_detail',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
