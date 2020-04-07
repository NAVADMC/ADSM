# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0045_auto_20190317_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outputsettings',
            name='save_daily_unit_states',
            field=models.BooleanField(help_text='Save all daily non-susceptible states for each unit in a supplemental file.', default=False),
        ),
    ]
