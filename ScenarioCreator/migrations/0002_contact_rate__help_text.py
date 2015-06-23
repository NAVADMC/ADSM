# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directspread',
            name='contact_rate',
            field=models.FloatField(help_text='<div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="true">\n                                    Fixed baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>\n                                <div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="false">\n                                    Mean baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='contact_rate',
            field=models.FloatField(help_text='<div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="true">\n                                    Fixed baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>\n                                <div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="false">\n                                    Mean baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
    ]
