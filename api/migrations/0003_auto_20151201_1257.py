# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151127_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField(default=0, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='api.Category')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='grocer',
        ),
        migrations.RemoveField(
            model_name='product',
            name='modified',
        ),
        migrations.AddField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(to='api.Product'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='shopkeeper',
            field=models.ForeignKey(to='api.ShopKeeper'),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, to='api.Subcategory', null=True),
        ),
    ]
