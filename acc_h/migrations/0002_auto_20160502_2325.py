# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc_h', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CHILD_M',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('CHILD_ID', models.CharField(null=True, blank=True, max_length=250)),
                ('CHILD_NM', models.CharField(null=True, blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='CUST_M',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('CUST_NM', models.CharField(null=True, blank=True, max_length=250)),
                ('PRES_PRI_SPEC', models.CharField(null=True, blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='PARENT_M',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('PARENT_ID', models.CharField(null=True, blank=True, max_length=250)),
                ('PARENT_NM', models.CharField(null=True, blank=True, max_length=250)),
            ],
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='CHILD_ID',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='CHILD_NM',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='CUST_NM',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='PARENT_ID',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='PARENT_NM',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='PRES_PRI_SPEC',
        ),
        migrations.AddField(
            model_name='account_info',
            name='CHILD',
            field=models.ForeignKey(null=True, blank=True, to='acc_h.CHILD_M'),
        ),
        migrations.AddField(
            model_name='account_info',
            name='CUST',
            field=models.ForeignKey(null=True, blank=True, to='acc_h.CUST_M'),
        ),
        migrations.AddField(
            model_name='account_info',
            name='PARENT',
            field=models.ForeignKey(null=True, blank=True, to='acc_h.PARENT_M'),
        ),
    ]
