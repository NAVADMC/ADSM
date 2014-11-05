# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Population'
        db.create_table('ScenarioCreator_population', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_file', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
        ))
        db.send_create_signal('ScenarioCreator', ['Population'])

        # Adding model 'Unit'
        db.create_table('ScenarioCreator_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_population', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Population'])),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('latitude', self.gf('django_extras.db.models.fields.LatitudeField')()),
            ('longitude', self.gf('django_extras.db.models.fields.LongitudeField')()),
            ('initial_state', self.gf('django.db.models.fields.CharField')(max_length=255, default='S')),
            ('days_in_initial_state', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('days_left_in_initial_state', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('initial_size', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['Unit'])

        # Adding model 'ProbabilityFunction'
        db.create_table('ScenarioCreator_probabilityfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('x_axis_units', self.gf('django.db.models.fields.CharField')(max_length=255, default='Days')),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('equation_type', self.gf('django.db.models.fields.CharField')(max_length=255, default='Triangular')),
            ('mean', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('std_dev', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('min', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('mode', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('max', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('alpha', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('alpha2', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('beta', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('location', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('scale', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('shape', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('n', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('p', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('m', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('d', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('theta', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('a', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('s', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.RelationalFunction'])),
        ))
        db.send_create_signal('ScenarioCreator', ['ProbabilityFunction'])

        # Adding model 'RelationalFunction'
        db.create_table('ScenarioCreator_relationalfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('x_axis_units', self.gf('django.db.models.fields.CharField')(max_length=255, default='Days')),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('y_axis_units', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
        ))
        db.send_create_signal('ScenarioCreator', ['RelationalFunction'])

        # Adding model 'RelationalPoint'
        db.create_table('ScenarioCreator_relationalpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relational_function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'])),
            ('x', self.gf('django.db.models.fields.FloatField')()),
            ('y', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('ScenarioCreator', ['RelationalPoint'])

        # Adding model 'ControlMasterPlan'
        db.create_table('ScenarioCreator_controlmasterplan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, default='Control Master Plan')),
            ('disable_all_controls', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destruction_program_delay', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('destruction_capacity', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
            ('destruction_priority_order', self.gf('django.db.models.fields.CharField')(max_length=255, default='reason, time waiting, production type')),
            ('destruction_reason_order', self.gf('django.db.models.fields.CharField')(max_length=255, default='Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring')),
            ('units_detected_before_triggering_vaccination', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('vaccination_capacity', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
            ('vaccination_priority_order', self.gf('django.db.models.fields.CharField')(max_length=255, default='reason, time waiting, production type')),
        ))
        db.send_create_signal('ScenarioCreator', ['ControlMasterPlan'])

        # Adding model 'ControlProtocol'
        db.create_table('ScenarioCreator_controlprotocol', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('use_detection', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('detection_probability_for_observed_time_in_clinical', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
            ('detection_probability_report_vs_first_detection', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
            ('detection_is_a_zone_trigger', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_tracing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trace_direct_forward', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trace_direct_back', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('direct_trace_success_rate', self.gf('ScenarioCreator.custom_fields.PercentField')(blank=True, null=True)),
            ('direct_trace_period', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('trace_indirect_forward', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trace_indirect_back', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('indirect_trace_success', self.gf('ScenarioCreator.custom_fields.PercentField')(blank=True, null=True)),
            ('indirect_trace_period', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('trace_result_delay', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('direct_trace_is_a_zone_trigger', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('indirect_trace_is_a_zone_trigger', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_destruction', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destruction_is_a_ring_trigger', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destruction_ring_radius', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('destruction_is_a_ring_target', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destroy_direct_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destroy_indirect_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destroy_direct_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destroy_indirect_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destruction_priority', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True, default=5)),
            ('use_vaccination', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vaccinate_detected_units', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('days_to_immunity', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('minimum_time_between_vaccinations', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('vaccine_immune_period', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('trigger_vaccination_ring', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vaccination_ring_radius', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('vaccination_priority', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True, default=5)),
            ('vaccination_demand_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('cost_of_vaccination_additional_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(decimal_places=4, max_digits=20, default=0.0)),
            ('use_exams', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('examine_direct_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exam_direct_forward_success_multiplier', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('examine_indirect_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exam_indirect_forward_success_multiplier', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('examine_direct_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exam_direct_back_success_multiplier', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('examine_indirect_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('examine_indirect_back_success_multiplier', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('use_testing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_direct_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_indirect_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_direct_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_indirect_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_specificity', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('test_sensitivity', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('test_delay', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('use_cost_accounting', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost_of_destruction_appraisal_per_unit', self.gf('django_extras.db.models.fields.MoneyField')(decimal_places=4, max_digits=20, default=0.0)),
            ('cost_of_destruction_cleaning_per_unit', self.gf('django_extras.db.models.fields.MoneyField')(decimal_places=4, max_digits=20, default=0.0)),
            ('cost_of_euthanasia_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(decimal_places=4, max_digits=20, default=0.0)),
            ('cost_of_indemnification_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(decimal_places=4, max_digits=20, default=0.0)),
            ('cost_of_carcass_disposal_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(decimal_places=4, max_digits=20, default=0.0)),
            ('cost_of_vaccination_setup_per_unit', self.gf('django_extras.db.models.fields.MoneyField')(decimal_places=4, max_digits=20, default=0.0)),
            ('cost_of_vaccination_baseline_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(decimal_places=4, max_digits=20, default=0.0)),
        ))
        db.send_create_signal('ScenarioCreator', ['ControlProtocol'])

        # Adding model 'ProtocolAssignment'
        db.create_table('ScenarioCreator_protocolassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_master_plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ControlMasterPlan'])),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'], unique=True)),
            ('control_protocol', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.ControlProtocol'])),
            ('notes', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=255)),
        ))
        db.send_create_signal('ScenarioCreator', ['ProtocolAssignment'])

        # Adding model 'Disease'
        db.create_table('ScenarioCreator_disease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('disease_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('include_direct_contact_spread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('include_indirect_contact_spread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('include_airborne_spread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('use_airborne_exponential_decay', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_within_unit_prevalence', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ScenarioCreator', ['Disease'])

        # Adding model 'DiseaseProgression'
        db.create_table('ScenarioCreator_diseaseprogression', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_disease', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Disease'])),
            ('disease_latent_period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('disease_subclinical_period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('disease_clinical_period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('disease_immune_period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('disease_prevalence', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
        ))
        db.send_create_signal('ScenarioCreator', ['DiseaseProgression'])

        # Adding model 'DiseaseProgressionAssignment'
        db.create_table('ScenarioCreator_diseaseprogressionassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'], unique=True)),
            ('progression', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.DiseaseProgression'])),
        ))
        db.send_create_signal('ScenarioCreator', ['DiseaseProgressionAssignment'])

        # Adding model 'IndirectSpread'
        db.create_table('ScenarioCreator_indirectspread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_disease', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Disease'])),
            ('transport_delay', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('subclinical_animals_can_infect_others', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_rate', self.gf('django.db.models.fields.FloatField')()),
            ('use_fixed_contact_rate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('distance_distribution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('movement_control', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
            ('infection_probability', self.gf('ScenarioCreator.custom_fields.PercentField')()),
        ))
        db.send_create_signal('ScenarioCreator', ['IndirectSpread'])

        # Adding model 'DirectSpread'
        db.create_table('ScenarioCreator_directspread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_disease', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Disease'])),
            ('transport_delay', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('subclinical_animals_can_infect_others', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_rate', self.gf('django.db.models.fields.FloatField')()),
            ('use_fixed_contact_rate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('distance_distribution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('movement_control', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
            ('infection_probability', self.gf('ScenarioCreator.custom_fields.PercentField')(blank=True, null=True)),
            ('latent_animals_can_infect_others', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ScenarioCreator', ['DirectSpread'])

        # Adding model 'AirborneSpread'
        db.create_table('ScenarioCreator_airbornespread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_disease', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Disease'])),
            ('transport_delay', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('spread_1km_probability', self.gf('ScenarioCreator.custom_fields.PercentField')()),
            ('max_distance', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('exposure_direction_start', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('exposure_direction_end', self.gf('django.db.models.fields.PositiveIntegerField')(default=360)),
        ))
        db.send_create_signal('ScenarioCreator', ['AirborneSpread'])

        # Adding model 'Scenario'
        db.create_table('ScenarioCreator_scenario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255, default='en')),
            ('random_seed', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['Scenario'])

        # Adding model 'OutputSettings'
        db.create_table('ScenarioCreator_outputsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iterations', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('stop_criteria', self.gf('django.db.models.fields.CharField')(max_length=255, default='disease-end')),
            ('days', self.gf('django.db.models.fields.PositiveIntegerField')(default=1825)),
            ('cost_track_destruction', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('cost_track_vaccination', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('cost_track_zone_surveillance', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('save_daily_unit_states', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('save_daily_events', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('save_daily_exposures', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('save_iteration_outputs_for_units', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('save_map_output', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ScenarioCreator', ['OutputSettings'])

        # Adding model 'ProductionType'
        db.create_table('ScenarioCreator_productiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['ProductionType'])

        # Adding model 'DiseaseSpreadAssignment'
        db.create_table('ScenarioCreator_diseasespreadassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'], related_name='used_as_sources')),
            ('destination_production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'], related_name='used_as_destinations')),
            ('direct_contact_spread', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.DirectSpread'], related_name='direct_spread_pair')),
            ('indirect_contact_spread', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.IndirectSpread'], related_name='indirect_spread_pair')),
            ('airborne_spread', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.AirborneSpread'], related_name='airborne_spread_pair')),
        ))
        db.send_create_signal('ScenarioCreator', ['DiseaseSpreadAssignment'])

        # Adding unique constraint on 'DiseaseSpreadAssignment', fields ['source_production_type', 'destination_production_type']
        db.create_unique('ScenarioCreator_diseasespreadassignment', ['source_production_type_id', 'destination_production_type_id'])

        # Adding model 'Zone'
        db.create_table('ScenarioCreator_zone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('radius', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('ScenarioCreator', ['Zone'])

        # Adding model 'ZoneEffect'
        db.create_table('ScenarioCreator_zoneeffect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=255)),
            ('zone_direct_movement', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
            ('zone_indirect_movement', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
            ('zone_detection_multiplier', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('cost_of_surveillance_per_animal_day', self.gf('django_extras.db.models.fields.MoneyField')(decimal_places=4, max_digits=20, default=0.0)),
        ))
        db.send_create_signal('ScenarioCreator', ['ZoneEffect'])

        # Adding model 'ZoneEffectAssignment'
        db.create_table('ScenarioCreator_zoneeffectassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone'])),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('effect', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['ScenarioCreator.ZoneEffect'])),
        ))
        db.send_create_signal('ScenarioCreator', ['ZoneEffectAssignment'])


    def backwards(self, orm):
        # Removing unique constraint on 'DiseaseSpreadAssignment', fields ['source_production_type', 'destination_production_type']
        db.delete_unique('ScenarioCreator_diseasespreadassignment', ['source_production_type_id', 'destination_production_type_id'])

        # Deleting model 'Population'
        db.delete_table('ScenarioCreator_population')

        # Deleting model 'Unit'
        db.delete_table('ScenarioCreator_unit')

        # Deleting model 'ProbabilityFunction'
        db.delete_table('ScenarioCreator_probabilityfunction')

        # Deleting model 'RelationalFunction'
        db.delete_table('ScenarioCreator_relationalfunction')

        # Deleting model 'RelationalPoint'
        db.delete_table('ScenarioCreator_relationalpoint')

        # Deleting model 'ControlMasterPlan'
        db.delete_table('ScenarioCreator_controlmasterplan')

        # Deleting model 'ControlProtocol'
        db.delete_table('ScenarioCreator_controlprotocol')

        # Deleting model 'ProtocolAssignment'
        db.delete_table('ScenarioCreator_protocolassignment')

        # Deleting model 'Disease'
        db.delete_table('ScenarioCreator_disease')

        # Deleting model 'DiseaseProgression'
        db.delete_table('ScenarioCreator_diseaseprogression')

        # Deleting model 'DiseaseProgressionAssignment'
        db.delete_table('ScenarioCreator_diseaseprogressionassignment')

        # Deleting model 'IndirectSpread'
        db.delete_table('ScenarioCreator_indirectspread')

        # Deleting model 'DirectSpread'
        db.delete_table('ScenarioCreator_directspread')

        # Deleting model 'AirborneSpread'
        db.delete_table('ScenarioCreator_airbornespread')

        # Deleting model 'Scenario'
        db.delete_table('ScenarioCreator_scenario')

        # Deleting model 'OutputSettings'
        db.delete_table('ScenarioCreator_outputsettings')

        # Deleting model 'ProductionType'
        db.delete_table('ScenarioCreator_productiontype')

        # Deleting model 'DiseaseSpreadAssignment'
        db.delete_table('ScenarioCreator_diseasespreadassignment')

        # Deleting model 'Zone'
        db.delete_table('ScenarioCreator_zone')

        # Deleting model 'ZoneEffect'
        db.delete_table('ScenarioCreator_zoneeffect')

        # Deleting model 'ZoneEffectAssignment'
        db.delete_table('ScenarioCreator_zoneeffectassignment')


    models = {
        'ScenarioCreator.airbornespread': {
            'Meta': {'object_name': 'AirborneSpread'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            'exposure_direction_end': ('django.db.models.fields.PositiveIntegerField', [], {'default': '360'}),
            'exposure_direction_start': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_distance': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spread_1km_probability': ('ScenarioCreator.custom_fields.PercentField', [], {}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"})
        },
        'ScenarioCreator.controlmasterplan': {
            'Meta': {'object_name': 'ControlMasterPlan'},
            'destruction_capacity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'destruction_priority_order': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'reason, time waiting, production type'"}),
            'destruction_program_delay': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destruction_reason_order': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring'"}),
            'disable_all_controls': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'Control Master Plan'"}),
            'units_detected_before_triggering_vaccination': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccination_capacity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'vaccination_priority_order': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'reason, time waiting, production type'"})
        },
        'ScenarioCreator.controlprotocol': {
            'Meta': {'object_name': 'ControlProtocol'},
            'cost_of_carcass_disposal_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'decimal_places': '4', 'max_digits': '20', 'default': '0.0'}),
            'cost_of_destruction_appraisal_per_unit': ('django_extras.db.models.fields.MoneyField', [], {'decimal_places': '4', 'max_digits': '20', 'default': '0.0'}),
            'cost_of_destruction_cleaning_per_unit': ('django_extras.db.models.fields.MoneyField', [], {'decimal_places': '4', 'max_digits': '20', 'default': '0.0'}),
            'cost_of_euthanasia_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'decimal_places': '4', 'max_digits': '20', 'default': '0.0'}),
            'cost_of_indemnification_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'decimal_places': '4', 'max_digits': '20', 'default': '0.0'}),
            'cost_of_vaccination_additional_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'decimal_places': '4', 'max_digits': '20', 'default': '0.0'}),
            'cost_of_vaccination_baseline_per_animal': ('django_extras.db.models.fields.MoneyField', [], {'decimal_places': '4', 'max_digits': '20', 'default': '0.0'}),
            'cost_of_vaccination_setup_per_unit': ('django_extras.db.models.fields.MoneyField', [], {'decimal_places': '4', 'max_digits': '20', 'default': '0.0'}),
            'days_to_immunity': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destroy_direct_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destroy_direct_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destroy_indirect_back_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destroy_indirect_forward_traces': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_is_a_ring_target': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_is_a_ring_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destruction_priority': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True', 'default': '5'}),
            'destruction_ring_radius': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'detection_is_a_zone_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'detection_probability_for_observed_time_in_clinical': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'detection_probability_report_vs_first_detection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'direct_trace_is_a_zone_trigger': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'direct_trace_period': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'direct_trace_success_rate': ('ScenarioCreator.custom_fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
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
            'indirect_trace_period': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'indirect_trace_success': ('ScenarioCreator.custom_fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'minimum_time_between_vaccinations': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'test_delay': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
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
            'trace_result_delay': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'trigger_vaccination_ring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_cost_accounting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_destruction': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_detection': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'use_exams': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_testing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_tracing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_vaccination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vaccinate_detected_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vaccination_demand_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccination_priority': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True', 'default': '5'}),
            'vaccination_ring_radius': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'vaccine_immune_period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"})
        },
        'ScenarioCreator.directspread': {
            'Meta': {'object_name': 'DirectSpread'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            'contact_rate': ('django.db.models.fields.FloatField', [], {}),
            'distance_distribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('ScenarioCreator.custom_fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'latent_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'movement_control': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'use_fixed_contact_rate': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.disease': {
            'Meta': {'object_name': 'Disease'},
            'disease_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_airborne_spread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'include_direct_contact_spread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'include_indirect_contact_spread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'disease_prevalence': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'disease_subclinical_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ScenarioCreator.diseaseprogressionassignment': {
            'Meta': {'object_name': 'DiseaseProgressionAssignment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'unique': 'True'}),
            'progression': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.DiseaseProgression']"})
        },
        'ScenarioCreator.diseasespreadassignment': {
            'Meta': {'object_name': 'DiseaseSpreadAssignment', 'unique_together': "(('source_production_type', 'destination_production_type'),)"},
            'airborne_spread': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.AirborneSpread']", 'related_name': "'airborne_spread_pair'"}),
            'destination_production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'related_name': "'used_as_destinations'"}),
            'direct_contact_spread': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.DirectSpread']", 'related_name': "'direct_spread_pair'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirect_contact_spread': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.IndirectSpread']", 'related_name': "'indirect_spread_pair'"}),
            'source_production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'related_name': "'used_as_sources'"})
        },
        'ScenarioCreator.indirectspread': {
            'Meta': {'object_name': 'IndirectSpread'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            'contact_rate': ('django.db.models.fields.FloatField', [], {}),
            'distance_distribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('ScenarioCreator.custom_fields.PercentField', [], {}),
            'movement_control': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'use_fixed_contact_rate': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ScenarioCreator.outputsettings': {
            'Meta': {'object_name': 'OutputSettings'},
            'cost_track_destruction': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cost_track_vaccination': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cost_track_zone_surveillance': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'days': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1825'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iterations': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'save_daily_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_daily_exposures': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_daily_unit_states': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_iteration_outputs_for_units': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'save_map_output': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stop_criteria': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'disease-end'"})
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
            'd': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'equation_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'Triangular'"}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'm': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'max': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'mean': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'min': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'mode': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'n': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'p': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            's': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'scale': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'shape': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'std_dev': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'theta': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'x_axis_units': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'Days'"})
        },
        'ScenarioCreator.productiontype': {
            'Meta': {'object_name': 'ProductionType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'ScenarioCreator.protocolassignment': {
            'Meta': {'object_name': 'ProtocolAssignment'},
            '_master_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ControlMasterPlan']"}),
            'control_protocol': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.ControlProtocol']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'unique': 'True'})
        },
        'ScenarioCreator.relationalfunction': {
            'Meta': {'object_name': 'RelationalFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'x_axis_units': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'Days'"}),
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
            'language': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "'en'"}),
            'random_seed': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'ScenarioCreator.unit': {
            'Meta': {'object_name': 'Unit'},
            '_population': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Population']"}),
            'days_in_initial_state': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'days_left_in_initial_state': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'initial_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'S'"}),
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
            'cost_of_surveillance_per_animal_day': ('django_extras.db.models.fields.MoneyField', [], {'decimal_places': '4', 'max_digits': '20', 'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'zone_detection_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'zone_direct_movement': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'zone_indirect_movement': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"})
        },
        'ScenarioCreator.zoneeffectassignment': {
            'Meta': {'object_name': 'ZoneEffectAssignment'},
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['ScenarioCreator.ZoneEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Zone']"})
        }
    }

    complete_apps = ['ScenarioCreator']