# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RequestApp', '0003_system_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system_user',
            name='company',
            field=models.ForeignKey(to='RequestApp.Company', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='system_user',
            name='usertype',
            field=models.ForeignKey(to='RequestApp.User_type', null=True),
            preserve_default=True,
        ),
    ]
