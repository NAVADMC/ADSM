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
        db.rename_column('ScenarioCreator_indirectspreadmodel', 'transport_delay_pdf_id', 'transport_delay_id')
        db.rename_column('ScenarioCreator_indirectspreadmodel', 'distance_pdf_id', 'distance_id')
        db.rename_column('ScenarioCreator_diseasereaction', 'disease_latent_period_pdf_id', 'disease_latent_period_id')
        db.rename_column('ScenarioCreator_diseasereaction', 'disease_clinical_period_pdf_id', 'disease_clinical_period_id')
        db.rename_column('ScenarioCreator_diseasereaction', 'disease_subclinical_period_pdf_id', 'disease_subclinical_period_id')
        db.rename_column('ScenarioCreator_diseasereaction', 'disease_immune_period_pdf_id', 'disease_immune_period_id')
        db.rename_column('ScenarioCreator_airbornespreadmodel', 'transport_delay_pdf_id', 'transport_delay_id')
        db.rename_column('ScenarioCreator_directspreadmodel', 'transport_delay_pdf_id', 'transport_delay_id')
        db.rename_column('ScenarioCreator_directspreadmodel', 'distance_pdf_id', 'distance_id')
        db.rename_column('ScenarioCreator_controlprotocol', 'test_delay_pdf_id', 'test_delay_id')
        db.rename_column('ScenarioCreator_controlprotocol', 'vaccine_immune_period_pdf_id', 'vaccine_immune_period_id')


    def backwards(self, orm):
        # User chose to not deal with backwards NULL issues for 'IndirectSpreadModel.transport_delay_pdf'
        raise RuntimeError("Cannot reverse this migration. 'IndirectSpreadModel.transport_delay_pdf' and its values cannot be restored.")

    models = {
        'ScenarioCreator.airbornespreadmodel': {
            'Meta': {'object_name': 'AirborneSpreadModel'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_distance': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'spread_1km_probability': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
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
            'destrucion_reason_order': ('django.db.models.fields.CharField', [], {'default': "'Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring'", 'max_length': '255'}),
            'destruction_capacity_relid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True'}),
            'destruction_priority_order': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'destruction_program_delay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'units_detected_before_triggering_vaccincation': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccination_capacity_relid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True'}),
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
            'detection_probability_for_observed_time_in_clinical_relid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True'}),
            'detection_probability_report_vs_first_detection_relid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True'}),
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
            'test_delay': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
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
            'trace_result_delay': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True'}),
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
            'vaccine_immune_period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True'})
        },
        'ScenarioCreator.customoutputs': {
            'Meta': {'_ormbases': ['ScenarioCreator.OutputSettings'], 'object_name': 'CustomOutputs'},
            'all_units_states': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'clock_time': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'disease_duration': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'num_animals_in_each_state': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'num_animals_in_each_state_by_production_type': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'num_units_in_each_state': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'num_units_in_each_state_by_production_type': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'outbreak_duration': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'outputsettings_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['ScenarioCreator.OutputSettings']", 'unique': 'True'}),
            'tsdA': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'}),
            'tsdU': ('django.db.models.fields.CharField', [], {'default': "'never'", 'max_length': '50'})
        },
        'ScenarioCreator.dbschemaversion': {
            'Meta': {'object_name': 'DbSchemaVersion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version_application': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version_date': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'version_info_url': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'ScenarioCreator.directspreadmodel': {
            'Meta': {'object_name': 'DirectSpreadModel'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'indirect'", 'max_length': '255'}),
            'contact_rate': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'distance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'latent_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'movement_control_relid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
            'use_fixed_contact_rate': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.disease': {
            'Meta': {'object_name': 'Disease'},
            'disease_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ScenarioCreator.diseasereaction': {
            'Meta': {'object_name': 'DiseaseReaction'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            'disease_clinical_period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
            'disease_immune_period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
            'disease_latent_period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
            'disease_prevalence_relid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True'}),
            'disease_subclinical_period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ScenarioCreator.diseasereactionassignment': {
            'Meta': {'object_name': 'DiseaseReactionAssignment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'reaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.DiseaseReaction']"})
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
            'distance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'movement_control_relid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['ScenarioCreator.ProbabilityFunction']"}),
            'use_fixed_contact_rate': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.outputsettings': {
            'Meta': {'object_name': 'OutputSettings'},
            '_scenario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Scenario']"}),
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
            'source_file': ('django.db.models.fields.CharField', [], {'default': "'SampleScenario.sqlite3'", 'max_length': '255'})
        },
        'ScenarioCreator.probabilityfunction': {
            'Meta': {'object_name': 'ProbabilityFunction'},
            'a': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'alpha': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'alpha2': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'beta': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'equation_type': ('django.db.models.fields.CharField', [], {'default': "'Triangular'", 'max_length': '255'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ScenarioCreator.productiontypepairtransmission': {
            'Meta': {'object_name': 'ProductionTypePairTransmission'},
            'airborne_contact_spread_model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'airborne_spread_pair'", 'blank': 'True', 'to': "orm['ScenarioCreator.AirborneSpreadModel']", 'null': 'True'}),
            'destination_production_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'used_as_destinations'", 'to': "orm['ScenarioCreator.ProductionType']"}),
            'direct_contact_spread_model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'direct_spread_pair'", 'blank': 'True', 'to': "orm['ScenarioCreator.DirectSpreadModel']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirect_contact_spread_model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indirect_spread_pair'", 'blank': 'True', 'to': "orm['ScenarioCreator.IndirectSpreadModel']", 'null': 'True'}),
            'source_production_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'used_as_sources'", 'to': "orm['ScenarioCreator.ProductionType']"})
        },
        'ScenarioCreator.protocolassignment': {
            'Meta': {'object_name': 'ProtocolAssignment'},
            '_master_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ControlMasterPlan']"}),
            'control_protocol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ControlProtocol']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"})
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
            '_point_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relational_function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {})
        },
        'ScenarioCreator.scenario': {
            'Meta': {'object_name': 'Scenario'},
            'cost_track_destruction': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cost_track_vaccination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cost_track_zone_surveillance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_airborne_spread': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'include_contact_spread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'random_seed': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'use_airborne_exponential_decay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_fixed_random_seed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_within_unit_prevalence': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'zone_direct_movement_relid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True'}),
            'zone_indirect_movement_relid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True'})
        }
    }

    complete_apps = ['ScenarioCreator']