# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='phone',
        ),
        migrations.AddField(
            model_name='guest',
            name='phone_number',
            field=models.CharField(default=1, unique=True, max_length=12),
            preserve_default=False,
        ),
    ]
