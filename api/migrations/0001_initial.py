# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('limit', models.IntegerField(default=200)),
                ('status', models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe5\xbc\x80\xe5\xa7\x8b'), (1, b'\xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad'), (2, b'\xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f')])),
                ('address', models.CharField(max_length=200)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='guest',
            field=models.ManyToManyField(to='api.Guest'),
        ),
    ]
