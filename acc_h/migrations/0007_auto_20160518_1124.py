# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc_h', '0006_auto_20160511_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand_nm_m',
            name='PFZ_MKT',
            field=models.ForeignKey(to='acc_h.PFZ_MKT_M', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account_info',
            name='CURR_DOL_SLS',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='CURR_DOL_SLS_MKT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='CURR_NEW_PTNT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='CURR_TOTAL_PTNT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='CURR_TRX_SLS',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='CURR_TRX_SLS_MKT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='CURR_UNIT_SLS',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='CURR_UNIT_SLS_MKT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='NUM_DTL',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='NUM_DTL_TCL',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='NUM_HCP',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='NUM_HCP_TCL',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='NUM_HCP_TCL_WITH_DTL',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='NUM_HCP_TCL_WITH_SLS',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='NUM_HCP_WITH_DTL',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='NUM_HCP_WITH_SLS',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='PREV_DOL_SLS',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='PREV_DOL_SLS_MKT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='PREV_NEW_PTNT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='PREV_TOTAL_PTNT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='PREV_TRX_SLS',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='PREV_TRX_SLS_MKT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='PREV_UNIT_SLS',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='PREV_UNIT_SLS_MKT',
            field=models.DecimalField(decimal_places=0, max_digits=19, blank=True, null=True),
        ),
    ]
