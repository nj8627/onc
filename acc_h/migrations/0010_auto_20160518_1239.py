# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc_h', '0009_chnl_nm_m_chnl_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CHNL_ID_NM_M',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('CHNL_ID', models.ForeignKey(to='acc_h.CHNL_ID_M')),
            ],
        ),
        migrations.RemoveField(
            model_name='chnl_nm_m',
            name='CHNL_ID',
        ),
        migrations.AddField(
            model_name='chnl_id_nm_m',
            name='CHNL_NM',
            field=models.ForeignKey(to='acc_h.CHNL_NM_M'),
        ),
    ]
