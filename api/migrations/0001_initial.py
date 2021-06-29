# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=100)),
                ('address_verification', models.CharField(max_length=100)),
                ('neighborhood', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=15)),
                ('type', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(default=0)),
                ('client', models.ForeignKey(to='api.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('modified', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='api.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ShopKeeper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('lat', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('lon', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('password', models.CharField(max_length=100, null=True, blank=True)),
                ('shop_name', models.CharField(max_length=100, null=True, blank=True)),
                ('delivery_time', models.IntegerField(default=10)),
                ('point', django.contrib.gis.db.models.fields.PointField(default=b'POINT(0.0 0.0)', srid=32140)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='grocer',
            field=models.ForeignKey(to='api.ShopKeeper'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='api.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='shopkeeper',
            field=models.ForeignKey(blank=True, to='api.ShopKeeper', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='client',
            field=models.ForeignKey(to='api.Client'),
        ),
    ]
