# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=250)),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=15)),
                ('begin_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('resume', models.CharField(max_length=200)),
                ('company', models.ForeignKey(to='RequestApp.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('serial', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('contract', models.ForeignKey(to='RequestApp.Contract')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Execution_time',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_exectime', models.TimeField()),
                ('finish_exectime', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Groups_engineer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('info', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Normative_time',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_value', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Replacement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crashed', models.ForeignKey(related_name='crash', to='RequestApp.Equipment')),
                ('replace', models.ForeignKey(related_name='replace', to='RequestApp.Equipment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header', models.CharField(max_length=30)),
                ('info', models.TextField(max_length=200)),
                ('createtime', models.TimeField(auto_now_add=True)),
                ('mark', models.CharField(default=b'OK', max_length=2, choices=[(b'EF', b'Engineer_fault'), (b'DF', b'Disp_fault'), (b'ED', b'Disp_engineer_faults'), (b'OK', b'All in time')])),
                ('approvement', models.BooleanField(default=False)),
                ('solution', models.CharField(max_length=250)),
                ('company', models.ForeignKey(to='RequestApp.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request_priority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
                ('info', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request_status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('info', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request_type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
                ('info', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('income_date', models.DateField(auto_now_add=True)),
                ('outcome_date', models.DateField()),
                ('equipment', models.ForeignKey(related_name='storaged', to='RequestApp.Equipment')),
                ('target_equipment', models.ForeignKey(related_name='replaced', to='RequestApp.Equipment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('info', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='System_User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(default=True, max_length=100, unique=True, null=True, verbose_name='email address')),
                ('username', models.CharField(unique=True, max_length=50, verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('patronymic', models.CharField(max_length=30)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=15)),
                ('place', models.CharField(max_length=30)),
                ('company', models.ForeignKey(to='RequestApp.Company')),
                ('usertype', models.ForeignKey(to='RequestApp.User_type')),
            ],
            options={
                'ordering': ('-date_joined',),
                'verbose_name': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c',
                'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='specialization',
            name='engineer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='specialization',
            name='group',
            field=models.ForeignKey(to='RequestApp.Groups_engineer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='creator',
            field=models.ForeignKey(related_name='creator_of', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='dispatcher',
            field=models.ForeignKey(related_name='dispatcher_of', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='engineer',
            field=models.ForeignKey(related_name='engineer_of', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='equipment',
            field=models.ForeignKey(blank=True, to='RequestApp.Equipment', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='group',
            field=models.ForeignKey(blank=True, to='RequestApp.Groups_engineer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='priority',
            field=models.ForeignKey(to='RequestApp.Request_priority'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='reqtype',
            field=models.ForeignKey(to='RequestApp.Request_type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.ForeignKey(to='RequestApp.Request_status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='normative_time',
            name='priority',
            field=models.ForeignKey(to='RequestApp.Request_priority'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='normative_time',
            name='reqtype',
            field=models.ForeignKey(to='RequestApp.Request_type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='normative_time',
            name='status',
            field=models.ForeignKey(to='RequestApp.Request_status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groups_engineer',
            name='head',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='execution_time',
            name='request',
            field=models.ForeignKey(to='RequestApp.Request'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='execution_time',
            name='rstatus',
            field=models.ForeignKey(to='RequestApp.Request_status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='focus',
            field=models.ForeignKey(related_name='focus_of', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='manager',
            field=models.ForeignKey(related_name='manager_of', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='request',
            field=models.ForeignKey(to='RequestApp.Request'),
            preserve_default=True,
        ),
    ]
