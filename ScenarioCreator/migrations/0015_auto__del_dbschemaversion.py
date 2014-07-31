from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DbSchemaVersion'
        db.delete_table('ScenarioCreator_dbschemaversion')


    def backwards(self, orm):
        # Adding model 'DbSchemaVersion'
        db.create_table('ScenarioCreator_dbschemaversion', (
            ('version_info_url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version_application', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('version_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('version_date', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('ScenarioCreator', ['DbSchemaVersion'])


    models = {
        'ScenarioCreator.airbornespreadmodel': {
            'Meta': {'object_name': 'AirborneSpreadModel'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_distance': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'spread_1km_probability': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'wind_direction_end': ('django.db.models.fields.IntegerField', [], {'default': '360'}),
            'wind_direction_start': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'ScenarioCreator.controlmasterplan': {
            'Meta': {'object_name': 'ControlMasterPlan'},
            '_include_destruction': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_include_detection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_include_tracing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_include_tracing_testing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_include_tracing_unit_exam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_include_vaccination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_include_zones': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_capacity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'destruction_priority_order': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'destruction_program_delay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destruction_reason_order': ('django.db.models.fields.CharField', [], {'default': "'Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'units_detected_before_triggering_vaccination': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccination_capacity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'vaccination_priority_order': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ScenarioCreator.controlprotocol': {
            'Meta': {'object_name': 'ControlProtocol'},
            'cost_of_carcass_disposal_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'max_digits': '20', 'decimal_places': '4', 'default': '0.0'}),
            'cost_of_destruction_appraisal_per_unit': ('django_extras.db.models.fields.MoneyField', [], {'max_digits': '20', 'decimal_places': '4', 'default': '0.0'}),
            'cost_of_destruction_cleaning_per_unit': ('django_extras.db.models.fields.MoneyField', [], {'max_digits': '20', 'decimal_places': '4', 'default': '0.0'}),
            'cost_of_euthanasia_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'max_digits': '20', 'decimal_places': '4', 'default': '0.0'}),
            'cost_of_indemnification_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'max_digits': '20', 'decimal_places': '4', 'default': '0.0'}),
            'cost_of_vaccination_additional_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'max_digits': '20', 'decimal_places': '4', 'default': '0.0'}),
            'cost_of_vaccination_baseline_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'max_digits': '20', 'decimal_places': '4', 'default': '0.0'}),
            'cost_of_vaccination_setup_per_unit': ('django_extras.db.models.fields.MoneyField', [], {'max_digits': '20', 'decimal_places': '4', 'default': '0.0'}),
            'days_to_immunity': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destroy_direct_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destroy_direct_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destroy_indirect_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destroy_indirect_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_is_a_ring_target': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_is_a_ring_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_priority': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '5', 'null': 'True'}),
            'destruction_ring_radius': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'detection_is_a_zone_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'detection_probability_for_observed_time_in_clinical': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'detection_probability_report_vs_first_detection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'direct_trace_is_a_zone_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'direct_trace_period': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'direct_trace_success_rate': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'exam_direct_back_success_multiplier': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'exam_direct_forward_success_multiplier': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'exam_indirect_forward_success_multiplier': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'examine_direct_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'examine_direct_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'examine_indirect_back_success_multiplier': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'examine_indirect_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'examine_indirect_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirect_trace_is_a_zone_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'indirect_trace_period': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'indirect_trace_success': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'minimum_time_between_vaccinations': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'test_delay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'test_direct_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test_direct_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test_indirect_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test_indirect_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test_sensitivity': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'test_specificity': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'trace_direct_back': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trace_direct_forward': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trace_indirect_back': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trace_indirect_forward': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trace_result_delay': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
            'trigger_vaccination_ring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_cost_accounting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_destruction': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_detection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_testing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_tracing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_vaccination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vaccinate_detected_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vaccinate_retrospective_days': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccination_demand_threshold': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccination_priority': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '5', 'null': 'True'}),
            'vaccination_ring_radius': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'vaccine_immune_period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']"})
        },
        'ScenarioCreator.customoutputs': {
            'Meta': {'object_name': 'CustomOutputs', '_ormbases': ['ScenarioCreator.OutputSettings']},
            'all_units_states': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'clock_time': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'disease_duration': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'num_animals_in_each_state': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'num_animals_in_each_state_by_production_type': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'num_units_in_each_state': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'num_units_in_each_state_by_production_type': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'outbreak_duration': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'outputsettings_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ScenarioCreator.OutputSettings']", 'unique': 'True', 'primary_key': 'True'}),
            'tsdA': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'tsdU': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'})
        },
        'ScenarioCreator.directspreadmodel': {
            'Meta': {'object_name': 'DirectSpreadModel'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'indirect'", 'max_length': '255'}),
            'contact_rate': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'distance_distribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'latent_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'movement_control': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
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
        'ScenarioCreator.diseasereaction': {
            'Meta': {'object_name': 'DiseaseReaction'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            'disease_clinical_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'disease_immune_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'disease_latent_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'disease_prevalence': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'disease_subclinical_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ScenarioCreator.diseasereactionassignment': {
            'Meta': {'object_name': 'DiseaseReactionAssignment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'unique': 'True'}),
            'reaction': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.DiseaseReaction']"})
        },
        'ScenarioCreator.dynamicblob': {
            'Meta': {'object_name': 'DynamicBlob'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone_perimeters': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'ScenarioCreator.indirectspreadmodel': {
            'Meta': {'object_name': 'IndirectSpreadModel'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'indirect'", 'max_length': '255'}),
            'contact_rate': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'distance_distribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'movement_control': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'use_fixed_contact_rate': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.outputsettings': {
            'Meta': {'object_name': 'OutputSettings'},
            '_scenario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Scenario']"}),
            'cost_track_destruction': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cost_track_vaccination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cost_track_zone_surveillance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'daily_states_filename': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'days': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'early_stop_criteria': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iterations': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'map_directory': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'maximum_iterations_for_daily_output': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '3', 'null': 'True'}),
            'save_all_daily_outputs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_daily_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_daily_exposures': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_iteration_outputs_for_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'write_map_output': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.population': {
            'Meta': {'object_name': 'Population'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_file': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'ScenarioCreator.probabilityfunction': {
            'Meta': {'object_name': 'ProbabilityFunction'},
            'a': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'alpha': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'alpha2': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'beta': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'equation_type': ('django.db.models.fields.CharField', [], {'default': "'Triangular'", 'max_length': '255'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'm': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'max': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'mean': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'min': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'mode': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'n': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'p': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            's': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'scale': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'shape': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'std_dev': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'theta': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'x_axis_units': ('django.db.models.fields.CharField', [], {'default': "'Days'", 'max_length': '255'})
        },
        'ScenarioCreator.productiontype': {
            'Meta': {'object_name': 'ProductionType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'ScenarioCreator.productiontypepairtransmission': {
            'Meta': {'object_name': 'ProductionTypePairTransmission', 'unique_together': "(('source_production_type', 'destination_production_type'),)"},
            'airborne_contact_spread_model': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'airborne_spread_pair'", 'null': 'True', 'to': "orm['ScenarioCreator.AirborneSpreadModel']"}),
            'destination_production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'related_name': "'used_as_destinations'"}),
            'direct_contact_spread_model': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'direct_spread_pair'", 'null': 'True', 'to': "orm['ScenarioCreator.DirectSpreadModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirect_contact_spread_model': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'indirect_spread_pair'", 'null': 'True', 'to': "orm['ScenarioCreator.IndirectSpreadModel']"}),
            'source_production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'related_name': "'used_as_sources'"})
        },
        'ScenarioCreator.protocolassignment': {
            'Meta': {'object_name': 'ProtocolAssignment'},
            '_master_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ControlMasterPlan']"}),
            'control_protocol': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.ControlProtocol']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
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
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
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
            'random_seed': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'use_fixed_random_seed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.unit': {
            'Meta': {'object_name': 'Unit'},
            '_cum_destroyed': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            '_cum_detected': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            '_cum_infected': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            '_cum_vaccinated': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            '_final_control_state_code': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            '_final_detection_state_code': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            '_final_state_code': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            '_population': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Population']"}),
            'days_in_initial_state': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'days_left_in_initial_state': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_size': ('django.db.models.fields.IntegerField', [], {}),
            'initial_state': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '255'}),
            'latitude': ('django_extras.db.models.fields.LatitudeField', [], {}),
            'longitude': ('django_extras.db.models.fields.LongitudeField', [], {}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'user_defined_1': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_defined_2': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_defined_3': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_defined_4': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'ScenarioCreator.zone': {
            'Meta': {'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone_description': ('django.db.models.fields.TextField', [], {}),
            'zone_radius': ('django.db.models.fields.FloatField', [], {})
        },
        'ScenarioCreator.zoneeffectonproductiontype': {
            'Meta': {'object_name': 'ZoneEffectOnProductionType'},
            'cost_of_surveillance_per_animal_day': ('django_extras.db.models.fields.MoneyField', [], {'max_digits': '20', 'decimal_places': '4', 'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Zone']"}),
            'zone_detection_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'zone_direct_movement': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'zone_indirect_movement': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']"})
        }
    }

    complete_apps = ['ScenarioCreator']