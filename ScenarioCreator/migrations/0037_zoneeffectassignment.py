# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ZoneEffectOnProductionType'
        db.delete_table('ScenarioCreator_zoneeffectonproductiontype')

        # Adding model 'ZoneEffectAssignment'
        db.create_table('ScenarioCreator_zoneeffectassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone'])),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('effect', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ZoneEffect'])),
        ))
        db.send_create_signal('ScenarioCreator', ['ZoneEffectAssignment'])

        # Adding model 'ZoneEffect'
        db.create_table('ScenarioCreator_zoneeffect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255)),
            ('zone_direct_movement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], null=True, blank=True, related_name='+')),
            ('zone_indirect_movement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], null=True, blank=True, related_name='+')),
            ('zone_detection_multiplier', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('cost_of_surveillance_per_animal_day', self.gf('django_extras.db.models.fields.MoneyField')(default=0.0, max_digits=20, decimal_places=4)),
        ))
        db.send_create_signal('ScenarioCreator', ['ZoneEffect'])


    def backwards(self, orm):
        # Adding model 'ZoneEffectOnProductionType'
        db.create_table('ScenarioCreator_zoneeffectonproductiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone_indirect_movement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], blank=True, null=True, related_name='+')),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone'])),
            ('zone_direct_movement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], blank=True, null=True, related_name='+')),
            ('zone_detection_multiplier', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('cost_of_surveillance_per_animal_day', self.gf('django_extras.db.models.fields.MoneyField')(default=0.0, max_digits=20, decimal_places=4)),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
        ))
        db.send_create_signal('ScenarioCreator', ['ZoneEffectOnProductionType'])

        # Deleting model 'ZoneEffectAssignment'
        db.delete_table('ScenarioCreator_zoneeffectassignment')

        # Deleting model 'ZoneEffect'
        db.delete_table('ScenarioCreator_zoneeffect')


    models = {
        'ScenarioCreator.airbornespread': {
            'Meta': {'object_name': 'AirborneSpread'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spread_1km_probability': ('ScenarioCreator.custom_fields.PercentField', [], {}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'wind_direction_end': ('django.db.models.fields.PositiveIntegerField', [], {'default': '360'}),
            'wind_direction_start': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'ScenarioCreator.controlmasterplan': {
            'Meta': {'object_name': 'ControlMasterPlan'},
            'destruction_capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'destruction_priority_order': ('django.db.models.fields.CharField', [], {'default': "'reason, time waiting, production type'", 'max_length': '255'}),
            'destruction_program_delay': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destruction_reason_order': ('django.db.models.fields.CharField', [], {'default': "'Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring'", 'max_length': '255'}),
            'disable_all_controls': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Control Master Plan'", 'max_length': '255'}),
            'units_detected_before_triggering_vaccination': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccination_capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'vaccination_priority_order': ('django.db.models.fields.CharField', [], {'default': "'reason, time waiting, production type'", 'max_length': '255'})
        },
        'ScenarioCreator.controlprotocol': {
            'Meta': {'object_name': 'ControlProtocol'},
            'cost_of_carcass_disposal_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '4'}),
            'cost_of_destruction_appraisal_per_unit': ('django_extras.db.models.fields.MoneyField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '4'}),
            'cost_of_destruction_cleaning_per_unit': ('django_extras.db.models.fields.MoneyField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '4'}),
            'cost_of_euthanasia_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '4'}),
            'cost_of_indemnification_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '4'}),
            'cost_of_vaccination_additional_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '4'}),
            'cost_of_vaccination_baseline_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '4'}),
            'cost_of_vaccination_setup_per_unit': ('django_extras.db.models.fields.MoneyField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '4'}),
            'days_to_immunity': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destroy_direct_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destroy_direct_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destroy_indirect_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destroy_indirect_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_is_a_ring_target': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_is_a_ring_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_priority': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True', 'default': '5'}),
            'destruction_ring_radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'detection_is_a_zone_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'detection_probability_for_observed_time_in_clinical': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'detection_probability_report_vs_first_detection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'direct_trace_is_a_zone_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'direct_trace_period': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'direct_trace_success_rate': ('ScenarioCreator.custom_fields.PercentField', [], {'null': 'True', 'blank': 'True'}),
            'exam_direct_back_success_multiplier': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'exam_direct_forward_success_multiplier': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'exam_indirect_forward_success_multiplier': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'examine_direct_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'examine_direct_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'examine_indirect_back_success_multiplier': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'examine_indirect_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'examine_indirect_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirect_trace_is_a_zone_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'indirect_trace_period': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'indirect_trace_success': ('ScenarioCreator.custom_fields.PercentField', [], {'null': 'True', 'blank': 'True'}),
            'minimum_time_between_vaccinations': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'test_delay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'test_direct_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test_direct_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test_indirect_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test_indirect_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test_sensitivity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'test_specificity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'trace_direct_back': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trace_direct_forward': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trace_indirect_back': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trace_indirect_forward': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trace_result_delay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'trigger_vaccination_ring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_cost_accounting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_destruction': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_detection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_testing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_tracing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_vaccination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vaccinate_detected_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vaccination_demand_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccination_priority': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True', 'default': '5'}),
            'vaccination_ring_radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vaccine_immune_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"})
        },
        'ScenarioCreator.directspread': {
            'Meta': {'object_name': 'DirectSpread'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'indirect'", 'max_length': '255'}),
            'contact_rate': ('django.db.models.fields.FloatField', [], {}),
            'distance_distribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('ScenarioCreator.custom_fields.PercentField', [], {}),
            'latent_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'movement_control': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'use_fixed_contact_rate': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.disease': {
            'Meta': {'object_name': 'Disease'},
            'disease_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_airborne_spread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'include_contact_spread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'use_airborne_exponential_decay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_within_unit_prevalence': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.diseaseprogression': {
            'Meta': {'object_name': 'DiseaseProgression'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            'disease_clinical_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'disease_immune_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'disease_latent_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'disease_prevalence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'disease_subclinical_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ScenarioCreator.diseaseprogressionassignment': {
            'Meta': {'object_name': 'DiseaseProgressionAssignment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'unique': 'True'}),
            'progression': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.DiseaseProgression']", 'null': 'True', 'blank': 'True'})
        },
        'ScenarioCreator.dynamicblob': {
            'Meta': {'object_name': 'DynamicBlob'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone_perimeters': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'ScenarioCreator.indirectspread': {
            'Meta': {'object_name': 'IndirectSpread'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'indirect'", 'max_length': '255'}),
            'contact_rate': ('django.db.models.fields.FloatField', [], {}),
            'distance_distribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('ScenarioCreator.custom_fields.PercentField', [], {}),
            'movement_control': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'use_fixed_contact_rate': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.outputsettings': {
            'Meta': {'object_name': 'OutputSettings'},
            '_scenario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Scenario']"}),
            'cost_track_destruction': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cost_track_vaccination': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cost_track_zone_surveillance': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'days': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1825'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iterations': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'save_daily_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_daily_exposures': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_daily_unit_states': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_iteration_outputs_for_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_map_output': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stop_criteria': ('django.db.models.fields.CharField', [], {'default': "'disease-end'", 'max_length': '255'})
        },
        'ScenarioCreator.population': {
            'Meta': {'object_name': 'Population'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_file': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'ScenarioCreator.probabilityfunction': {
            'Meta': {'object_name': 'ProbabilityFunction'},
            'a': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'alpha': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'alpha2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'd': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'equation_type': ('django.db.models.fields.CharField', [], {'default': "'Triangular'", 'max_length': '255'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mean': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mode': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'n': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            's': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'scale': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'shape': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'std_dev': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'theta': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_axis_units': ('django.db.models.fields.CharField', [], {'default': "'Days'", 'max_length': '255'})
        },
        'ScenarioCreator.productiontype': {
            'Meta': {'object_name': 'ProductionType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'ScenarioCreator.productiontypepairtransmission': {
            'Meta': {'unique_together': "(('source_production_type', 'destination_production_type'),)", 'object_name': 'ProductionTypePairTransmission'},
            'airborne_spread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.AirborneSpread']", 'null': 'True', 'blank': 'True', 'related_name': "'airborne_spread_pair'"}),
            'destination_production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'related_name': "'used_as_destinations'"}),
            'direct_contact_spread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.DirectSpread']", 'null': 'True', 'blank': 'True', 'related_name': "'direct_spread_pair'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirect_contact_spread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.IndirectSpread']", 'null': 'True', 'blank': 'True', 'related_name': "'indirect_spread_pair'"}),
            'source_production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'related_name': "'used_as_sources'"})
        },
        'ScenarioCreator.protocolassignment': {
            'Meta': {'object_name': 'ProtocolAssignment'},
            '_master_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ControlMasterPlan']"}),
            'control_protocol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ControlProtocol']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'unique': 'True'})
        },
        'ScenarioCreator.readallcodes': {
            'Meta': {'object_name': 'ReadAllCodes'},
            '_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            '_code_description': ('django.db.models.fields.TextField', [], {}),
            '_code_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ScenarioCreator.readallcodetypes': {
            'Meta': {'object_name': 'ReadAllCodeTypes'},
            '_code_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            '_code_type_description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ScenarioCreator.relationalfunction': {
            'Meta': {'object_name': 'RelationalFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'x_axis_units': ('django.db.models.fields.CharField', [], {'default': "'Days'", 'max_length': '255'}),
            'y_axis_units': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'ScenarioCreator.relationalpoint': {
            'Meta': {'object_name': 'RelationalPoint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relational_function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {})
        },
        'ScenarioCreator.scenario': {
            'Meta': {'object_name': 'Scenario'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'en'", 'max_length': '255'}),
            'random_seed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ScenarioCreator.unit': {
            'Meta': {'object_name': 'Unit'},
            '_population': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Population']"}),
            'days_in_initial_state': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'days_left_in_initial_state': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'initial_state': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '255'}),
            'latitude': ('django_extras.db.models.fields.LatitudeField', [], {}),
            'longitude': ('django_extras.db.models.fields.LongitudeField', [], {}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'user_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'ScenarioCreator.zone': {
            'Meta': {'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'radius': ('django.db.models.fields.FloatField', [], {})
        },
        'ScenarioCreator.zoneeffect': {
            'Meta': {'object_name': 'ZoneEffect'},
            'cost_of_surveillance_per_animal_day': ('django_extras.db.models.fields.MoneyField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'zone_detection_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'zone_direct_movement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"}),
            'zone_indirect_movement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'blank': 'True', 'related_name': "'+'"})
        },
        'ScenarioCreator.zoneeffectassignment': {
            'Meta': {'object_name': 'ZoneEffectAssignment'},
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ZoneEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Zone']"})
        }
    }

    complete_apps = ['ScenarioCreator']