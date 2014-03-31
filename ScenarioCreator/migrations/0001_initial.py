# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DbSchemaVersion'
        db.create_table('ScenarioCreator_dbschemaversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version_number', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('version_application', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version_date', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version_info_url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('version_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['DbSchemaVersion'])

        # Adding model 'DynamicBlob'
        db.create_table('ScenarioCreator_dynamicblob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone_perimeters', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
        ))
        db.send_create_signal('ScenarioCreator', ['DynamicBlob'])

        # Adding model 'Population'
        db.create_table('ScenarioCreator_population', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_file', self.gf('django.db.models.fields.CharField')(default='SampleScenario.sqlite3', max_length=255)),
        ))
        db.send_create_signal('ScenarioCreator', ['Population'])

        # Adding model 'Unit'
        db.create_table('ScenarioCreator_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_population', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Population'])),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('latitude', self.gf('django_extras.db.models.fields.LatitudeField')()),
            ('longitude', self.gf('django_extras.db.models.fields.LongitudeField')()),
            ('initial_state', self.gf('django.db.models.fields.CharField')(default='S', max_length=255)),
            ('days_in_initial_state', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('days_left_in_initial_state', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('initial_size', self.gf('django.db.models.fields.IntegerField')()),
            ('_final_state_code', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('_final_control_state_code', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('_final_detection_state_code', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('_cum_infected', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('_cum_detected', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('_cum_destroyed', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('_cum_vaccinated', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('user_defined_1', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user_defined_2', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user_defined_3', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user_defined_4', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['Unit'])

        # Adding model 'ProbabilityFunction'
        db.create_table('ScenarioCreator_probabilityfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('x_axis_units', self.gf('django.db.models.fields.CharField')(default='Days', max_length=255)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('equation_type', self.gf('django.db.models.fields.CharField')(default='Triangular', max_length=255)),
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
            ('n', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('p', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('m', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('d', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('theta', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('a', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('s', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['ProbabilityFunction'])

        # Adding model 'RelationalFunction'
        db.create_table('ScenarioCreator_relationalfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('x_axis_units', self.gf('django.db.models.fields.CharField')(default='Days', max_length=255)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('y_axis_units', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
        ))
        db.send_create_signal('ScenarioCreator', ['RelationalFunction'])

        # Adding model 'RelationalPoint'
        db.create_table('ScenarioCreator_relationalpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relational_function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'])),
            ('_point_order', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('x', self.gf('django.db.models.fields.FloatField')()),
            ('y', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('ScenarioCreator', ['RelationalPoint'])

        # Adding model 'ControlMasterPlan'
        db.create_table('ScenarioCreator_controlmasterplan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_include_detection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_include_tracing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_include_tracing_unit_exam', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_include_tracing_testing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_include_destruction', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_include_vaccination', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_include_zones', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destruction_program_delay', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('destruction_capacity_relid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], null=True, related_name='+', blank=True)),
            ('destruction_priority_order', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('destrucion_reason_order', self.gf('django.db.models.fields.CharField')(default='Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring', max_length=255)),
            ('units_detected_before_triggering_vaccincation', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vaccination_capacity_relid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], null=True, related_name='+', blank=True)),
            ('vaccination_priority_order', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('ScenarioCreator', ['ControlMasterPlan'])

        # Adding model 'ControlProtocol'
        db.create_table('ScenarioCreator_controlprotocol', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('use_detection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('detection_probability_for_observed_time_in_clinical_relid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], null=True, related_name='+', blank=True)),
            ('detection_probability_report_vs_first_detection_relid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], null=True, related_name='+', blank=True)),
            ('detection_is_a_zone_trigger', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_tracing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trace_direct_forward', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trace_direct_back', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('direct_trace_success_rate', self.gf('django_extras.db.models.fields.PercentField')(blank=True, null=True)),
            ('direct_trace_period', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('trace_indirect_forward', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trace_indirect_back', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('indirect_trace_success', self.gf('django_extras.db.models.fields.PercentField')(blank=True, null=True)),
            ('indirect_trace_period', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('trace_result_delay_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], null=True, related_name='+', blank=True)),
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
            ('destruction_priority', self.gf('django.db.models.fields.IntegerField')(blank=True, default=5, null=True)),
            ('use_vaccination', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vaccinate_detected_units', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('days_to_immunity', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('minimum_time_between_vaccinations', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vaccine_immune_period_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], null=True, related_name='+', blank=True)),
            ('trigger_vaccination_ring', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vaccination_ring_radius', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('vaccination_priority', self.gf('django.db.models.fields.IntegerField')(blank=True, default=5, null=True)),
            ('vaccination_demand_threshold', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('cost_of_vaccination_additional_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(max_digits=20, decimal_places=4, default=0.0)),
            ('use_testing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('examine_direct_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exam_direct_forward_success_multiplier', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('examine_indirect_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exam_indirect_forward_success_multiplier', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('examine_direct_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exam_direct_back_success_multiplier', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('examine_indirect_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('examine_indirect_back_success_multiplier', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('test_direct_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_indirect_forward_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_direct_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_indirect_back_traces', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_specificity', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('test_sensitivity', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('test_delay_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('vaccinate_retrospective_days', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('use_cost_accounting', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost_of_destruction_appraisal_per_unit', self.gf('django_extras.db.models.fields.MoneyField')(max_digits=20, decimal_places=4, default=0.0)),
            ('cost_of_destruction_cleaning_per_unit', self.gf('django_extras.db.models.fields.MoneyField')(max_digits=20, decimal_places=4, default=0.0)),
            ('cost_of_euthanasia_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(max_digits=20, decimal_places=4, default=0.0)),
            ('cost_of_indemnification_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(max_digits=20, decimal_places=4, default=0.0)),
            ('cost_of_carcass_disposal_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(max_digits=20, decimal_places=4, default=0.0)),
            ('cost_of_vaccination_setup_per_unit', self.gf('django_extras.db.models.fields.MoneyField')(max_digits=20, decimal_places=4, default=0.0)),
            ('cost_of_vaccination_baseline_per_animal', self.gf('django_extras.db.models.fields.MoneyField')(max_digits=20, decimal_places=4, default=0.0)),
        ))
        db.send_create_signal('ScenarioCreator', ['ControlProtocol'])

        # Adding model 'ProtocolAssignment'
        db.create_table('ScenarioCreator_protocolassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_master_plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ControlMasterPlan'])),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('control_protocol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ControlProtocol'])),
            ('notes', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255, null=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['ProtocolAssignment'])

        # Adding model 'Disease'
        db.create_table('ScenarioCreator_disease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('disease_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['Disease'])

        # Adding model 'DiseaseReaction'
        db.create_table('ScenarioCreator_diseasereaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_disease', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Disease'])),
            ('disease_latent_period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('disease_subclinical_period_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('disease_clinical_period_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('disease_immune_period_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('disease_prevalence_relid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], null=True, related_name='+', blank=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['DiseaseReaction'])

        # Adding model 'DiseaseReactionAssignment'
        db.create_table('ScenarioCreator_diseasereactionassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('reaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.DiseaseReaction'])),
        ))
        db.send_create_signal('ScenarioCreator', ['DiseaseReactionAssignment'])

        # Adding model 'IndirectSpreadModel'
        db.create_table('ScenarioCreator_indirectspreadmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255, null=True)),
            ('_disease', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Disease'])),
            ('transport_delay_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('_spread_method_code', self.gf('django.db.models.fields.CharField')(default='indirect', max_length=255)),
            ('subclinical_animals_can_infect_others', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_rate', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('use_fixed_contact_rate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('infection_probability', self.gf('django_extras.db.models.fields.PercentField')(blank=True, null=True)),
            ('distance_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('movement_control_relid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
        ))
        db.send_create_signal('ScenarioCreator', ['IndirectSpreadModel'])

        # Adding model 'DirectSpreadModel'
        db.create_table('ScenarioCreator_directspreadmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255, null=True)),
            ('_disease', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Disease'])),
            ('transport_delay_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('_spread_method_code', self.gf('django.db.models.fields.CharField')(default='indirect', max_length=255)),
            ('subclinical_animals_can_infect_others', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_rate', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('use_fixed_contact_rate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('infection_probability', self.gf('django_extras.db.models.fields.PercentField')(blank=True, null=True)),
            ('distance_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('movement_control_relid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], related_name='+')),
            ('latent_animals_can_infect_others', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ScenarioCreator', ['DirectSpreadModel'])

        # Adding model 'AirborneSpreadModel'
        db.create_table('ScenarioCreator_airbornespreadmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255, null=True)),
            ('_disease', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Disease'])),
            ('transport_delay_pdf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProbabilityFunction'], related_name='+')),
            ('_spread_method_code', self.gf('django.db.models.fields.CharField')(default='other', max_length=255)),
            ('spread_1km_probability', self.gf('django_extras.db.models.fields.PercentField')(blank=True, null=True)),
            ('max_distance', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('wind_direction_start', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('wind_direction_end', self.gf('django.db.models.fields.IntegerField')(default=360)),
        ))
        db.send_create_signal('ScenarioCreator', ['AirborneSpreadModel'])

        # Adding model 'Scenario'
        db.create_table('ScenarioCreator_scenario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('use_fixed_random_seed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('random_seed', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('include_contact_spread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('include_airborne_spread', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_airborne_exponential_decay', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_within_unit_prevalence', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost_track_destruction', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost_track_vaccination', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost_track_zone_surveillance', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ScenarioCreator', ['Scenario'])

        # Adding model 'OutputSettings'
        db.create_table('ScenarioCreator_outputsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_scenario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Scenario'])),
            ('iterations', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('days', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('early_stop_criteria', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('save_all_daily_outputs', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('maximum_iterations_for_daily_output', self.gf('django.db.models.fields.IntegerField')(blank=True, default=3, null=True)),
            ('daily_states_filename', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255, null=True)),
            ('save_daily_events', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('save_daily_exposures', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('save_iteration_outputs_for_units', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('write_map_output', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('map_directory', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255, null=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['OutputSettings'])

        # Adding model 'CustomOutputs'
        db.create_table('ScenarioCreator_customoutputs', (
            ('outputsettings_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ScenarioCreator.OutputSettings'], primary_key=True, unique=True)),
            ('all_units_states', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
            ('num_units_in_each_state', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
            ('num_units_in_each_state_by_production_type', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
            ('num_animals_in_each_state', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
            ('num_animals_in_each_state_by_production_type', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
            ('disease_duration', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
            ('outbreak_duration', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
            ('clock_time', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
            ('tsdU', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
            ('tsdA', self.gf('django.db.models.fields.CharField')(default='never', max_length=50)),
        ))
        db.send_create_signal('ScenarioCreator', ['CustomOutputs'])

        # Adding model 'ProductionType'
        db.create_table('ScenarioCreator_productiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['ProductionType'])

        # Adding model 'ProductionTypePairTransmission'
        db.create_table('ScenarioCreator_productiontypepairtransmission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'], related_name='used_as_sources')),
            ('destination_production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'], related_name='used_as_destinations')),
            ('direct_contact_spread_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.DirectSpreadModel'], null=True, related_name='direct_spread_pair', blank=True)),
            ('indirect_contact_spread_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.IndirectSpreadModel'], null=True, related_name='indirect_spread_pair', blank=True)),
            ('airborne_contact_spread_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.AirborneSpreadModel'], null=True, related_name='airborne_spread_pair', blank=True)),
        ))
        db.send_create_signal('ScenarioCreator', ['ProductionTypePairTransmission'])

        # Adding model 'Zone'
        db.create_table('ScenarioCreator_zone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone_description', self.gf('django.db.models.fields.TextField')()),
            ('zone_radius', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('ScenarioCreator', ['Zone'])

        # Adding model 'ZoneEffectOnProductionType'
        db.create_table('ScenarioCreator_zoneeffectonproductiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone'])),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('zone_indirect_movement_relid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], null=True, related_name='+', blank=True)),
            ('zone_direct_movement_relid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.RelationalFunction'], null=True, related_name='+', blank=True)),
            ('zone_detection_multiplier', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('cost_of_surveillance_per_animal_day', self.gf('django_extras.db.models.fields.MoneyField')(max_digits=20, decimal_places=4, default=0.0)),
        ))
        db.send_create_signal('ScenarioCreator', ['ZoneEffectOnProductionType'])

        # Adding model 'ReadAllCodes'
        db.create_table('ScenarioCreator_readallcodes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_code_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_code_description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('ScenarioCreator', ['ReadAllCodes'])

        # Adding model 'ReadAllCodeTypes'
        db.create_table('ScenarioCreator_readallcodetypes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_code_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_code_type_description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('ScenarioCreator', ['ReadAllCodeTypes'])


    def backwards(self, orm):
        # Deleting model 'DbSchemaVersion'
        db.delete_table('ScenarioCreator_dbschemaversion')

        # Deleting model 'DynamicBlob'
        db.delete_table('ScenarioCreator_dynamicblob')

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

        # Deleting model 'DiseaseReaction'
        db.delete_table('ScenarioCreator_diseasereaction')

        # Deleting model 'DiseaseReactionAssignment'
        db.delete_table('ScenarioCreator_diseasereactionassignment')

        # Deleting model 'IndirectSpreadModel'
        db.delete_table('ScenarioCreator_indirectspreadmodel')

        # Deleting model 'DirectSpreadModel'
        db.delete_table('ScenarioCreator_directspreadmodel')

        # Deleting model 'AirborneSpreadModel'
        db.delete_table('ScenarioCreator_airbornespreadmodel')

        # Deleting model 'Scenario'
        db.delete_table('ScenarioCreator_scenario')

        # Deleting model 'OutputSettings'
        db.delete_table('ScenarioCreator_outputsettings')

        # Deleting model 'CustomOutputs'
        db.delete_table('ScenarioCreator_customoutputs')

        # Deleting model 'ProductionType'
        db.delete_table('ScenarioCreator_productiontype')

        # Deleting model 'ProductionTypePairTransmission'
        db.delete_table('ScenarioCreator_productiontypepairtransmission')

        # Deleting model 'Zone'
        db.delete_table('ScenarioCreator_zone')

        # Deleting model 'ZoneEffectOnProductionType'
        db.delete_table('ScenarioCreator_zoneeffectonproductiontype')

        # Deleting model 'ReadAllCodes'
        db.delete_table('ScenarioCreator_readallcodes')

        # Deleting model 'ReadAllCodeTypes'
        db.delete_table('ScenarioCreator_readallcodetypes')


    models = {
        'ScenarioCreator.airbornespreadmodel': {
            'Meta': {'object_name': 'AirborneSpreadModel'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_distance': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'spread_1km_probability': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'transport_delay_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
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
            'destruction_capacity_relid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'related_name': "'+'", 'blank': 'True'}),
            'destruction_priority_order': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'destruction_program_delay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'units_detected_before_triggering_vaccincation': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccination_capacity_relid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'related_name': "'+'", 'blank': 'True'}),
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
            'detection_probability_for_observed_time_in_clinical_relid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'related_name': "'+'", 'blank': 'True'}),
            'detection_probability_report_vs_first_detection_relid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'related_name': "'+'", 'blank': 'True'}),
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
            'test_delay_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
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
            'trace_result_delay_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True', 'related_name': "'+'", 'blank': 'True'}),
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
            'vaccine_immune_period_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'null': 'True', 'related_name': "'+'", 'blank': 'True'})
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
            'outputsettings_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ScenarioCreator.OutputSettings']", 'primary_key': 'True', 'unique': 'True'}),
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
            'version_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'ScenarioCreator.directspreadmodel': {
            'Meta': {'object_name': 'DirectSpreadModel'},
            '_disease': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Disease']"}),
            '_spread_method_code': ('django.db.models.fields.CharField', [], {'default': "'indirect'", 'max_length': '255'}),
            'contact_rate': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'distance_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'latent_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'movement_control_relid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
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
            'disease_clinical_period_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'disease_immune_period_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'disease_latent_period_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'disease_prevalence_relid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'related_name': "'+'", 'blank': 'True'}),
            'disease_subclinical_period_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
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
            'distance_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_probability': ('django_extras.db.models.fields.PercentField', [], {'blank': 'True', 'null': 'True'}),
            'movement_control_relid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'subclinical_animals_can_infect_others': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transport_delay_pdf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProbabilityFunction']", 'related_name': "'+'"}),
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
            'airborne_contact_spread_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.AirborneSpreadModel']", 'null': 'True', 'related_name': "'airborne_spread_pair'", 'blank': 'True'}),
            'destination_production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'related_name': "'used_as_destinations'"}),
            'direct_contact_spread_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.DirectSpreadModel']", 'null': 'True', 'related_name': "'direct_spread_pair'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirect_contact_spread_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.IndirectSpreadModel']", 'null': 'True', 'related_name': "'indirect_spread_pair'", 'blank': 'True'}),
            'source_production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'related_name': "'used_as_sources'"})
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
            'zone_direct_movement_relid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'related_name': "'+'", 'blank': 'True'}),
            'zone_indirect_movement_relid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.RelationalFunction']", 'null': 'True', 'related_name': "'+'", 'blank': 'True'})
        }
    }

    complete_apps = ['ScenarioCreator']