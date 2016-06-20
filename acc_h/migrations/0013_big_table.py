# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc_h', '0012_auto_20160519_0019'),
    ]

    operations = [
        migrations.CreateModel(
            name='BIG_TABLE',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('CHNL_ID', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('CHNL_NM', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('CHNL_VAL', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('CHILD_ID', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('CHILD_NM', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('CHILD_FULL_ADDR', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('PARENT_ID', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('PARENT_NM', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('PARENT_FULL_ADDR', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('PFZ_MKT_NM', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('BRAND_NM', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('TIME_BCKT', models.CharField(max_length=250, blank=True, db_index=True, null=True)),
                ('CURR_TRX_SLS', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('CURR_DOL_SLS', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('CURR_UNIT_SLS', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('CURR_NEW_PTNT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('CURR_TOTAL_PTNT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('CURR_TRX_SLS_MKT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('CURR_DOL_SLS_MKT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('CURR_UNIT_SLS_MKT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('PREV_TRX_SLS', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('PREV_DOL_SLS', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('PREV_UNIT_SLS', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('PREV_NEW_PTNT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('PREV_TOTAL_PTNT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('PREV_TRX_SLS_MKT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('PREV_DOL_SLS_MKT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('PREV_UNIT_SLS_MKT', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('NUM_DTL', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('NUM_DTL_TCL', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('NUM_HCP', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('NUM_HCP_TCL', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('NUM_HCP_WITH_DTL', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('NUM_HCP_TCL_WITH_DTL', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('NUM_HCP_WITH_SLS', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
                ('NUM_HCP_TCL_WITH_SLS', models.DecimalField(decimal_places=0, blank=True, null=True, max_digits=19)),
            ],
        ),
    ]
