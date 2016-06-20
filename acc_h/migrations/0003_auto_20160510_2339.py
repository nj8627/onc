# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc_h', '0002_auto_20160502_2325'),
    ]

    operations = [
        migrations.CreateModel(
            name='PFZ_MKT_M',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('PFZ_MKT_NM', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TIME_BCKT_M',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('TIME_BCKT', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='CUST',
        ),
        migrations.AddField(
            model_name='account_info',
            name='NUM_DTL',
            field=models.DecimalField(default=1, decimal_places=1, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account_info',
            name='NUM_DTL_TCL',
            field=models.DecimalField(default=1, decimal_places=1, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account_info',
            name='NUM_HCP',
            field=models.DecimalField(default=1, decimal_places=1, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account_info',
            name='NUM_HCP_TCL',
            field=models.DecimalField(default=1, decimal_places=1, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account_info',
            name='NUM_HCP_TCL_WITH_DTL',
            field=models.DecimalField(default=1, decimal_places=1, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account_info',
            name='NUM_HCP_TCL_WITH_SLS',
            field=models.DecimalField(default=1, decimal_places=1, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account_info',
            name='NUM_HCP_WITH_DTL',
            field=models.DecimalField(default=1, decimal_places=1, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account_info',
            name='NUM_HCP_WITH_SLS',
            field=models.DecimalField(default=1, decimal_places=1, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='child_m',
            name='CHILD_FULL_ADDR',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='parent_m',
            name='PARENT_FULL_ADDR',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.DeleteModel(
            name='CUST_M',
        ),
        migrations.AddField(
            model_name='account_info',
            name='PFZ_MKT',
            field=models.ForeignKey(default=1, to='acc_h.PFZ_MKT_M'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account_info',
            name='TIME_BCKT',
            field=models.ForeignKey(default=1, to='acc_h.TIME_BCKT_M'),
            preserve_default=False,
        ),
    ]
