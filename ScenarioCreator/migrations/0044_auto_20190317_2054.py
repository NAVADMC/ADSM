# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0043_auto_20190111_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoneeffect',
            name='zone_direct_movement',
            field=models.ForeignKey(null=True, related_name='+', help_text='Function that describes direct movement rate.', blank=True, to='ScenarioCreator.RelationalFunction'),
        ),
        migrations.AlterField(
            model_name='zoneeffect',
            name='zone_indirect_movement',
            field=models.ForeignKey(null=True, related_name='+', help_text='Function that describes indirect movement rate.', blank=True, to='ScenarioCreator.RelationalFunction'),
        ),
    ]
