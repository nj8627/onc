# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc_h', '0010_auto_20160518_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand_nm_m',
            name='BRAND_NM',
            field=models.CharField(db_index=True, null=True, max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='child_m',
            name='CHILD_ID',
            field=models.CharField(db_index=True, null=True, max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='child_m',
            name='CHILD_NM',
            field=models.CharField(db_index=True, null=True, max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='chnl_id_m',
            name='CHNL_ID',
            field=models.CharField(db_index=True, null=True, max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='chnl_nm_m',
            name='CHNL_NM',
            field=models.CharField(db_index=True, null=True, max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='parent_m',
            name='PARENT_ID',
            field=models.CharField(db_index=True, null=True, max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='parent_m',
            name='PARENT_NM',
            field=models.CharField(db_index=True, null=True, max_length=250, blank=True),
        ),
    ]
