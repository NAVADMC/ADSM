"""Form inheritance is for better support of layouts.  All forms have a default layout that it inherits from
ModelForm -> models.py.  This basic layout can be overridden by declaring an __init__ with a self.helper Layout.
See DirectSpread for an example.  More complex widgets and layouts are accessible from there.
All forms now have their "submit" button restored and you can choose custom layouts.  ControlProtocol has tabs."""


from floppyforms.__future__ import ModelForm
from django.conf import settings
from django.forms.models import inlineformset_factory
from crispy_forms.bootstrap import TabHolder, Tab, AppendedText
from crispy_forms.layout import Layout, ButtonHolder, HTML
from ScenarioCreator.models import *
from floppyforms import Select, NumberInput, HiddenInput, SelectMultiple, CheckboxInput
from crispy_forms.helper import FormHelper
import os


class AddOrSelect(Select):
    template_name = 'floppyforms/model_select.html'
    # def get_context(self, name, value, attrs=None, choices=()):
    #     context = super(AddOrSelect, self).get_context(name, value, attrs=None, choices=())
    #     context['attrs']['data-new-item-url'] = '/%s/new/' %


class FixedSelect(Select):
    template_name = 'floppyforms/fixed_select.html'

    def get_context(self, name, value, attrs=None, choices=()):
        context = super(FixedSelect, self).get_context(name, value, attrs)
        context['value'] = value
        context['value_name'] = ([x[1] for x in self.choices if x[0] == value] + [''])[0]  # first match
        return context


def submit_button():
    return ButtonHolder(HTML(open(os.path.join(settings.BASE_DIR, 'ScenarioCreator','templates','ScenarioCreator','EditButtons.html'), 'r').read()))


class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'helper'):  # so as not to override specific layouts
            self.helper = FormHelper()
            fields_and_submit = list(self.base_fields.keys()) + [submit_button()]
            self.helper.layout = Layout(*fields_and_submit)

        super(BaseForm, self).__init__(*args, **kwargs)


class PopulationForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'source_file',
            submit_button()
        )
        super(PopulationForm, self).__init__(*args, **kwargs)

    class Meta(object):
        model = Population
        exclude = []


class UnitForm(BaseForm):
    class Meta(object):
        model = Unit
        exclude = ['_population', ]
        widgets = {'production_type': AddOrSelect(attrs={'data-new-item-url': '/setup/ProductionType/new/'})}


class UnitFormAbbreviated(BaseForm):
    class Meta(object):
        model = Unit
        exclude = ['_population', 'days_in_initial_state', 'days_left_in_initial_state']
        widgets = {}
        #'production_type': AddOrSelect(attrs={'data-new-item-url': '/setup/ProductionType/new/'})


class ProbabilityFunctionForm(BaseForm):
    class Meta(object):
        model = ProbabilityFunction
        exclude = []
        widgets = {'graph': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'})}


class RelationalPointForm(BaseForm):
    class Meta(object):
        model = RelationalPoint
        fields = ['relational_function', 'x', 'y']  # just to make the deprecation warnings happy
        widgets = {'relational_function': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'})}


PointFormSet = inlineformset_factory(RelationalFunction, RelationalPoint, fields=['relational_function', 'x', 'y'], extra=4)


class RelationalFunctionForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'name',
            'x_axis_units',
            'y_axis_units',
            'notes'
        )
        super(RelationalFunctionForm, self).__init__(*args, **kwargs)

    class Meta(object):
        model = RelationalFunction
        exclude = []


class ControlMasterPlanForm(BaseForm):
    class Meta(object):
        model = ControlMasterPlan
        exclude = ['disable_all_controls']
        widgets = {
                 # 'disable_all_controls': CheckboxInput(attrs={'hidden':'hidden'}),
                   'destruction_capacity': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'vaccination_capacity': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'restart_vaccination_capacity': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   }


class ProtocolAssignmentForm(BaseForm):
    class Meta(object):
        model = ProtocolAssignment
        exclude = ['_master_plan', ]
        widgets = {'production_type': FixedSelect(),}


class DiseaseProgressionAssignmentForm(BaseForm):
    class Meta(object):
        model = DiseaseProgressionAssignment
        exclude = []
        widgets = {'production_type': FixedSelect(),
                   'progression': AddOrSelect(attrs={'data-new-item-url': '/setup/DiseaseProgression/new/'})}


class ControlProtocolForm(BaseForm):
    """https://speakerdeck.com/maraujop/advanced-django-forms-usage slide 47
    http://stackoverflow.com/questions/19625211/bootstrap-linking-to-a-tab-with-an-url"""
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'name',
            HTML('<script src="{{ STATIC_URL }}js/control-protocol.js"></script>'),
            TabHolder(
                Tab('Detection',
                    'use_detection',
                    'detection_probability_for_observed_time_in_clinical',
                    'detection_probability_report_vs_first_detection',
                    'detection_is_a_zone_trigger',
                    ),
                Tab('Tracing',
                    'use_tracing',
                    'trace_direct_forward',
                    'trace_direct_back',
                    AppendedText('direct_trace_success_rate', 'example: 0.37 = 37%'),
                    'direct_trace_period',
                    'trace_indirect_forward',
                    'trace_indirect_back',
                    AppendedText('indirect_trace_success', 'example: 0.37 = 37%'),
                    'indirect_trace_period',
                    'trace_result_delay',
                    'direct_trace_is_a_zone_trigger',
                    'indirect_trace_is_a_zone_trigger',
                    ),
                Tab('Testing',
                    'use_testing',
                    'test_direct_forward_traces',
                    'test_indirect_forward_traces',
                    'test_direct_back_traces',
                    'test_indirect_back_traces',
                    'test_specificity',
                    'test_sensitivity',
                    'test_delay',
                    ),
                Tab('Exams',
                    'use_exams',
                    'examine_direct_forward_traces',
                    'exam_direct_forward_success_multiplier',
                    'examine_indirect_forward_traces',
                    'exam_indirect_forward_success_multiplier',
                    'examine_direct_back_traces',
                    'exam_direct_back_success_multiplier',
                    'examine_indirect_back_traces',
                    'examine_indirect_back_success_multiplier',
                    ),
                Tab('Destruction',
                    'use_destruction',
                    'destruction_is_a_ring_trigger',
                    'destruction_ring_radius',
                    'destruction_is_a_ring_target',
                    'destroy_direct_forward_traces',
                    'destroy_indirect_forward_traces',
                    'destroy_direct_back_traces',
                    'destroy_indirect_back_traces',
                    'destruction_priority',
                    ),
                Tab('Vaccination',
                    'use_vaccination',
                    'vaccinate_detected_units',
                    'minimum_time_between_vaccinations',
                    'days_to_immunity',
                    'vaccine_immune_period',
                    'trigger_vaccination_ring',
                    'vaccination_ring_radius',
                    'vaccination_priority',
                    ),
                Tab('Cost Accounting',
                    'use_cost_accounting',
                    'cost_of_destruction_appraisal_per_unit',
                    'cost_of_destruction_cleaning_per_unit',
                    'cost_of_euthanasia_per_animal',
                    'cost_of_indemnification_per_animal',
                    'cost_of_carcass_disposal_per_animal',
                    'cost_of_vaccination_setup_per_unit',
                    'cost_of_vaccination_baseline_per_animal',
                    'vaccination_demand_threshold',
                    'cost_of_vaccination_additional_per_animal',
                    )
            ),
            submit_button()
        )
        super(ControlProtocolForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super(ControlProtocolForm, self).clean()
        #TODO: remove this duplication (above) by building both behaviors off the same list
        sections = {'use_detection': ['detection_probability_for_observed_time_in_clinical',
                                      'detection_probability_report_vs_first_detection',
                                      'detection_is_a_zone_trigger',
                                      ],
                    'use_tracing': ['trace_direct_forward',
                                    'trace_direct_back',
                                    'direct_trace_success_rate',
                                    'direct_trace_period',
                                    'trace_indirect_forward',
                                    'trace_indirect_back',
                                    'indirect_trace_success',
                                    'indirect_trace_period',
                                    'trace_result_delay',
                                    'direct_trace_is_a_zone_trigger',
                                    'indirect_trace_is_a_zone_trigger',
                                    ],
                    'use_testing': ['test_direct_forward_traces',
                                    'test_indirect_forward_traces',
                                    'test_direct_back_traces',
                                    'test_indirect_back_traces',
                                    'test_specificity',
                                    'test_sensitivity',
                                    'test_delay',
                                    ],
                    'use_exams': ['examine_direct_forward_traces',
                                  'exam_direct_forward_success_multiplier',
                                  'examine_indirect_forward_traces',
                                  'exam_indirect_forward_success_multiplier',
                                  'examine_direct_back_traces',
                                  'exam_direct_back_success_multiplier',
                                  'examine_indirect_back_traces',
                                  'examine_indirect_back_success_multiplier',
                                  ],
                    'use_destruction': ['destruction_is_a_ring_trigger',
                                        'destruction_ring_radius',
                                        'destruction_is_a_ring_target',
                                        'destroy_direct_forward_traces',
                                        'destroy_indirect_forward_traces',
                                        'destroy_direct_back_traces',
                                        'destroy_indirect_back_traces',
                                        'destruction_priority',
                                        ],
                    'use_vaccination': ['vaccinate_detected_units',
                                        'minimum_time_between_vaccinations',
                                        'days_to_immunity',
                                        'vaccine_immune_period',
                                        'trigger_vaccination_ring',
                                        'vaccination_ring_radius',
                                        'vaccination_priority',
                                        ],
                    'use_cost_accounting': ['cost_of_destruction_appraisal_per_unit',
                                            'cost_of_destruction_cleaning_per_unit',
                                            'cost_of_euthanasia_per_animal',
                                            'cost_of_indemnification_per_animal',
                                            'cost_of_carcass_disposal_per_animal',
                                            'cost_of_vaccination_setup_per_unit',
                                            'cost_of_vaccination_baseline_per_animal',
                                            'vaccination_demand_threshold',
                                            'cost_of_vaccination_additional_per_animal',
                                            ],
                    'use_': [],
                    }
        for trigger_switch, fields in sections.items():
            if cleaned_data.get(trigger_switch):
                for field in fields:
                    if cleaned_data.get(field) is None:
                        self.add_error(field, ValidationError(field + " must not be blank!"))
        
    class Meta(object):
        model = ControlProtocol
        exclude = []
        widgets = {'detection_probability_for_observed_time_in_clinical': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'detection_probability_report_vs_first_detection': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'trace_result_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'vaccine_immune_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'test_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'})}


class DiseaseForm(BaseForm):
    class Meta(object):
        model = Disease
        exclude = ['include_direct_contact_spread', 'include_indirect_contact_spread', 'include_airborne_spread']


class DiseaseProgressionForm(BaseForm):
    class Meta(object):
        model = DiseaseProgression
        exclude = ['_disease']
        widgets = {'_disease': AddOrSelect(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'disease_latent_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'disease_subclinical_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'disease_clinical_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'disease_immune_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'disease_prevalence': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/',
                                                            'data-visibility-context': 'use_within_unit_prevalence'})
        }


class IndirectSpreadForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            # 'latent_animals_can_infect_others',  # Indirect doesn't have this field
            'subclinical_animals_can_infect_others',
            'use_fixed_contact_rate',
            'contact_rate',
            AppendedText('infection_probability', 'example: 0.37 = 37%'),
            'distance_distribution',
            'transport_delay',
            'movement_control',
            submit_button()
        )
        super(IndirectSpreadForm, self).__init__(*args, **kwargs)

    class Meta(object):
        model = IndirectSpread
        exclude = ['_disease']
        widgets = {'distance_distribution': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   '_disease': AddOrSelect(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'movement_control': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'transport_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/',
                                                         'data-visibility-controller': 'transport_delay',
                                                         'data-disabled-value': ''})}  # should lock itself invisible if null


class DirectSpreadForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'latent_animals_can_infect_others',
            'subclinical_animals_can_infect_others',
            'use_fixed_contact_rate',
            'contact_rate',
            AppendedText('infection_probability', 'example: 0.37 = 37%'),
            'distance_distribution',
            'transport_delay',
            'movement_control',
            submit_button()
        )
        super(DirectSpreadForm, self).__init__(*args, **kwargs)
        
    class Meta(object):
        model = DirectSpread
        exclude = ['_disease']
        widgets = {'infection_probability': NumberInput(attrs={'data-visibility-context': 'use_within_unit_prevalence',
                                                               'data-visibility-flipped': 'true',
                                                               'step': 'any'}),
                   'distance_distribution': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   '_disease': AddOrSelect(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'movement_control': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'transport_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/',
                                                         'data-visibility-controller': 'transport_delay',
                                                         'data-disabled-value': ''})}  # should lock itself invisible if null


class AirborneSpreadForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            AppendedText('spread_1km_probability', 'example: 0.37 = 37%'),
            'max_distance',
            'exposure_direction_start',
            'exposure_direction_end',
            'transport_delay',
            submit_button()
        )
        super(AirborneSpreadForm, self).__init__(*args, **kwargs)
        
    class Meta(object):
        model = AirborneSpread
        exclude = ['_disease']
        widgets = {'_disease': AddOrSelect(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'max_distance': NumberInput(attrs={'data-visibility-context': 'use_airborne_exponential_decay',
                                                      'data-visibility-flipped': 'true',
                                                      'step': 'any'}),  # only visible when exponential is false
                   'movement_control': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'transport_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/',
                                                         'data-visibility-controller': 'transport_delay',
                                                         'data-disabled-value': ''})}  # should lock itself invisible if null


class ScenarioForm(BaseForm):
    class Meta(object):
        model = Scenario
        exclude = ['language', 'use_fixed_random_seed', 'random_seed']


class OutputSettingsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'iterations',
            'stop_criteria',
            'days',
            HTML(r"<h4>Cost Tracking</h4>"),
            'cost_track_destruction',
            'cost_track_vaccination',
            'cost_track_zone_surveillance',
            HTML(r"<h4>Supplemental Outputs</h4>"),
            'save_daily_unit_states',
            'save_daily_events',
            'save_daily_exposures',
            'save_map_output',
            submit_button()
        )
        super(OutputSettingsForm, self).__init__(*args, **kwargs)

    class Meta(object):
        model = OutputSettings
        exclude = ['save_iteration_outputs_for_units']
        widgets = {
            'days': NumberInput(
                attrs={'data-visibility-controller': 'stop_criteria',
                       'data-required-value': 'stop-days',
                       'step': '1'})
        }


class ProductionTypeForm(BaseForm):
    class Meta(object):
        model = ProductionType
        exclude = []


class DiseaseSpreadAssignmentForm(BaseForm):
    class Meta(object):
        model = DiseaseSpreadAssignment
        exclude = []
        widgets = {  # Production types are not given edit buttons because the user is only allowed to add Production types from a Population XML
                   'source_production_type': FixedSelect(),
                   'destination_production_type': FixedSelect(),}


class DiseaseIncludeSpreadForm(BaseForm):
    class Meta(object):
        model = Disease
        fields = ['include_direct_contact_spread', 'include_indirect_contact_spread', 'include_airborne_spread']
        widgets = {'include_direct_contact_spread': HiddenInput(),
                   'include_indirect_contact_spread': HiddenInput(),
                   'include_airborne_spread': HiddenInput()}


class ZoneForm(BaseForm):
    class Meta(object):
        model = Zone
        exclude = []


class ZoneEffectForm(BaseForm):
    class Meta(object):
        model = ZoneEffect
        exclude = []
        widgets = {'zone_indirect_movement': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'zone_direct_movement': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'})}


class ZoneEffectAssignmentForm(BaseForm):
    class Meta(object):
        model = ZoneEffectAssignment
        exclude = ['zone', 'production_type']
        widgets = {'zone': HiddenInput(),
                   'production_type': HiddenInput(),
                   'effect': AddOrSelect(attrs={'data-new-item-url': '/setup/ZoneEffect/new/'})}


## V3.3 Vaccination Triggers ##

class ProductionTypeList(SelectMultiple):
    template_name = 'floppyforms/multiselect.html'
    def __init__(self, starting_attrs=None):
        attrs = {'data-new-item-url': '/setup/ProductionType/new/'}
        if starting_attrs is not None:
            attrs.update(starting_attrs)
        super(ProductionTypeList, self).__init__(attrs)

    def get_context(self, name, value, attrs=None, choices=()):
        context = super(SelectMultiple, self).get_context(name, value, attrs)
        context['help_text'] = mark_safe("To add production types to the trigger click on a Type or Group from the <em>Population Panel</em>") 
        return context


class GroupList(SelectMultiple):
    template_name = 'floppyforms/multiselect.html'
    def __init__(self, starting_attrs=None):
        attrs = {'data-new-item-url': '/setup/ProductionGroup/new/'}
        if starting_attrs is not None:
            attrs.update(starting_attrs)
        super(GroupList, self).__init__(attrs)

    def get_context(self, name, value, attrs=None, choices=()):
        context = super(SelectMultiple, self).get_context(name, value, attrs)
        context['help_text'] = mark_safe("Create new Groups in the <em>Population Panel</em>") 
        return context


class ProductionGroupForm(BaseForm):
    class Meta(object):
        model = ProductionGroup
        exclude = []
        widgets = {'group': ProductionTypeList()}


class DiseaseDetectionForm(BaseForm):
    class Meta(object):
        model = DiseaseDetection
        fields = ['trigger_group', 'number_of_units', 'restart_only']
        widgets = {'trigger_group': ProductionTypeList()}


class RateOfNewDetectionsForm(BaseForm):
    class Meta(object):
        model = RateOfNewDetections
        fields = ['trigger_group', 'number_of_units', 'days', 'restart_only']
        widgets = {'trigger_group': ProductionTypeList()}


class DisseminationRateForm(BaseForm):
    class Meta(object):
        model = DisseminationRate
        fields = ['trigger_group', 'ratio', 'days', 'restart_only']
        widgets = {'trigger_group': ProductionTypeList()}


class TimeFromFirstDetectionForm(BaseForm):
    class Meta(object):
        model = TimeFromFirstDetection
        fields = ['trigger_group', 'days', 'restart_only']
        widgets = {'trigger_group': ProductionTypeList()}


class DestructionWaitTimeForm(BaseForm):
    class Meta(object):
        model = DestructionWaitTime
        fields = ['trigger_group', 'days', 'restart_only']
        widgets = {'trigger_group': ProductionTypeList()}


class SpreadBetweenGroupsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'number_of_groups',
            'relevant_groups',
            HTML(r"<a href='/setup/ProductionGroup/new/' load-target='#group-creator'>+ define new group</a>"),
            'restart_only',
            submit_button()
        )
        super(SpreadBetweenGroupsForm, self).__init__(*args, **kwargs)
    class Meta(object):
        model = SpreadBetweenGroups
        exclude = []
        widgets = {'relevant_groups': GroupList()}


class StopVaccinationForm(BaseForm):
    class Meta(object):
        model = StopVaccination
        exclude = ['restart_only']
        widgets = {'trigger_group': ProductionTypeList()}


class VaccinationRingRuleForm(BaseForm):
    class Meta(object):
        model = VaccinationRingRule
        exclude = []
        widgets = {'trigger_group': ProductionTypeList(),
                   'target_group': ProductionTypeList()}


