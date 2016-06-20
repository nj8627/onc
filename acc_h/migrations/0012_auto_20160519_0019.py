# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc_h', '0011_auto_20160519_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chnl_val_m',
            name='CHNL_VAL',
            field=models.CharField(max_length=250, db_index=True, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pfz_mkt_m',
            name='PFZ_MKT_NM',
            field=models.CharField(max_length=250, db_index=True, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time_bckt_m',
            name='TIME_BCKT',
            field=models.CharField(max_length=250, db_index=True, blank=True, null=True),
        ),
    ]
