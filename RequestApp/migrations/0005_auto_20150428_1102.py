# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RequestApp', '0004_auto_20150428_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system_user',
            name='email',
            field=models.EmailField(unique=True, max_length=100, verbose_name='email address'),
            preserve_default=True,
        ),
    ]
