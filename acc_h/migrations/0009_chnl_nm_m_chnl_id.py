# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc_h', '0008_auto_20160518_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='chnl_nm_m',
            name='CHNL_ID',
            field=models.ForeignKey(default=1, to='acc_h.CHNL_ID_M'),
            preserve_default=False,
        ),
    ]
