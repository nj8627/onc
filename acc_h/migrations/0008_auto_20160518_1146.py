# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc_h', '0007_auto_20160518_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='CHNL_ID_M',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('CHNL_ID', models.CharField(max_length=250, blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='account_info',
            name='CHNL_ID',
            field=models.ForeignKey(to='acc_h.CHNL_ID_M', default=1),
            preserve_default=False,
        ),
    ]
