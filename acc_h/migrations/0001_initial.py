# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ACCOUNT_INFO',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('PARENT_ID', models.CharField(max_length=250, null=True, blank=True)),
                ('PARENT_NM', models.CharField(max_length=250, null=True, blank=True)),
                ('CHILD_ID', models.CharField(max_length=250, null=True, blank=True)),
                ('CHILD_NM', models.CharField(max_length=250, null=True, blank=True)),
                ('CUST_NM', models.CharField(max_length=250, null=True, blank=True)),
                ('PRES_PRI_SPEC', models.CharField(max_length=250, null=True, blank=True)),
                ('CURR_TRX_SLS', models.DecimalField(decimal_places=1, max_digits=19)),
                ('CURR_DOL_SLS', models.DecimalField(decimal_places=1, max_digits=19)),
                ('CURR_UNIT_SLS', models.DecimalField(decimal_places=1, max_digits=19)),
                ('CURR_NEW_PTNT', models.DecimalField(decimal_places=1, max_digits=19)),
                ('CURR_TOTAL_PTNT', models.DecimalField(decimal_places=1, max_digits=19)),
                ('CURR_TRX_SLS_MKT', models.DecimalField(decimal_places=1, max_digits=19)),
                ('CURR_DOL_SLS_MKT', models.DecimalField(decimal_places=1, max_digits=19)),
                ('CURR_UNIT_SLS_MKT', models.DecimalField(decimal_places=1, max_digits=19)),
                ('PREV_TRX_SLS', models.DecimalField(decimal_places=1, max_digits=19)),
                ('PREV_DOL_SLS', models.DecimalField(decimal_places=1, max_digits=19)),
                ('PREV_UNIT_SLS', models.DecimalField(decimal_places=1, max_digits=19)),
                ('PREV_NEW_PTNT', models.DecimalField(decimal_places=1, max_digits=19)),
                ('PREV_TOTAL_PTNT', models.DecimalField(decimal_places=1, max_digits=19)),
                ('PREV_TRX_SLS_MKT', models.DecimalField(decimal_places=1, max_digits=19)),
                ('PREV_DOL_SLS_MKT', models.DecimalField(decimal_places=1, max_digits=19)),
                ('PREV_UNIT_SLS_MKT', models.DecimalField(decimal_places=1, max_digits=19)),
            ],
        ),
        migrations.CreateModel(
            name='BRAND_NM_M',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('BRAND_NM', models.CharField(max_length=250, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CHNL_NM_M',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('CHNL_NM', models.CharField(max_length=250, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CHNL_VAL_M',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('CHNL_VAL', models.CharField(max_length=250, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='account_info',
            name='BRAND_NM',
            field=models.ForeignKey(to='acc_h.BRAND_NM_M'),
        ),
        migrations.AddField(
            model_name='account_info',
            name='CHNL_NM',
            field=models.ForeignKey(to='acc_h.CHNL_NM_M'),
        ),
        migrations.AddField(
            model_name='account_info',
            name='CHNL_VAL',
            field=models.ForeignKey(to='acc_h.CHNL_VAL_M'),
        ),
    ]
