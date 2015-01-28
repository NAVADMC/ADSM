# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import ScenarioCreator.models


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0002_contact_rate__help_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airbornespread',
            name='max_distance',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(1.1)], help_text='The maximum distance in KM of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#airborne-transmission" class="wiki">airborne spread</a>.  Only used in Linear Airborne Decay.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='destruction_ring_radius',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Radius in kilometers of the destruction ring.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='exam_direct_back_success_multiplier',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki">clinical signs</a> in units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct contact</a>.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='exam_direct_forward_success_multiplier',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki">clinical signs</a> in units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct contact</a>.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='exam_indirect_forward_success_multiplier',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki">clinical signs</a> in units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> .'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='examine_indirect_back_success_multiplier',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki">clinical signs</a> in units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a>.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_sensitivity',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='<a href="http://en.wikipedia.org/wiki/Sensitivity_and_specificity" class="wiki">Test Sensitivity</a> for units of this production type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_specificity',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='<a href="http://en.wikipedia.org/wiki/Sensitivity_and_specificity" class="wiki">Test Specificity</a> for units of this production type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='vaccination_ring_radius',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Radius in kilometers of the vaccination ring.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='directspread',
            name='contact_rate',
            field=ScenarioCreator.models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], help_text='<div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="true">\n                                    Fixed baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>\n                                <div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="false">\n                                    Mean baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='contact_rate',
            field=ScenarioCreator.models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], help_text='<div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="true">\n                                    Fixed baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>\n                                <div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="false">\n                                    Mean baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='a',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Functions:Pareto.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='alpha',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, help_text='Functions: Gamma, Weibull, Pearson 5, Beta.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='alpha2',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, help_text='Functions: Beta.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='beta',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, help_text='Functions: Gamma, Weibull, Pearson 5.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='location',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, help_text='Functions: Logistic, LogLogistic.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='max',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Functions: Discrete Uniform, Uniform, Triangular, Beta, BetaPERT.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='mean',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Functions: Inverse Gaussian, Gaussian, Lognormal, Poisson, Exponential.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='min',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Functions: Discrete Uniform, Uniform, Triangular, Beta, BetaPERT.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='mode',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Functions: Fixed Value, Triangular, BetaPERT.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='p',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], help_text='Functions: Binomial, Negative Binomial, Bernoulli.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='scale',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, help_text='Functions: Logistic, LogLogistic.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='shape',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, help_text='Functions: LogLogistic, Inverse Gaussian.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='std_dev',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Functions: Gaussian, Lognormal.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='probabilityfunction',
            name='theta',
            field=ScenarioCreator.models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Functions: Pareto.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relationalpoint',
            name='x',
            field=ScenarioCreator.models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relationalpoint',
            name='y',
            field=ScenarioCreator.models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zone',
            name='radius',
            field=ScenarioCreator.models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], help_text='Radius in kilometers of the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki">Zone</a>'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zoneeffect',
            name='zone_detection_multiplier',
            field=ScenarioCreator.models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki">clinical signs</a> in units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a> in this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki">Zone</a>.'),
            preserve_default=True,
        ),
    ]
