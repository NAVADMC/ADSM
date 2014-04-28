"""Form inheritance is for better support of layouts.  All forms have a default layout that it inherits from
ModelForm -> models.py.  This basic layout can be overridden by declaring an __init__ with a self.helper Layout.
See DirectSpread for an example.  More complex widgets and layouts are accessible from there.
All forms now have their "submit" button restored and you can choose custom layouts.  ControlProtocol has tabs."""


from crispy_forms.bootstrap import TabHolder, Tab
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML, Field, Hidden
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import OperationalError  # OperationalError is for initial manage.py syncdb
from ScenarioCreator.models import *
from floppyforms import ModelForm, Select, NumberInput, RadioSelect, HiddenInput, TextInput
from crispy_forms.helper import FormHelper


class AddOrSelect(Select):
    template_name = 'floppyforms/model_select.html'
    # def get_context(self, name, value, attrs=None, choices=()):
    #     context = super(AddOrSelect, self).get_context(name, value, attrs=None, choices=())
    #     context['attrs']['data-new-item-url'] = '/%s/new/' %


class FixedSelect(Select):
    template_name = 'floppyforms/fixed_select.html'

    def get_context(self, name, value, attrs=None, choices=()):
        context = super(FixedSelect, self).get_context(name, value, attrs)
        print([x for x in self.choices])
        context['value'] = value
        context['value_name'] = [x[1] for x in self.choices if x[0] == value][0]  # first match
        return context


def submit_button():
    return ButtonHolder(Submit('submit', 'Submit', css_class='button white'),
                        HTML(open('ScenarioCreator/templates/ScenarioCreator/EditButtons.html', 'r').read()))


class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'helper'):  # so as not to override specific layouts
            self.helper = FormHelper()
            fields_and_submit = list(self.base_fields.keys()) + [submit_button()]
            self.helper.layout = Layout(*fields_and_submit)
        return super().__init__(*args, **kwargs)


class DynamicBlobForm(BaseForm):
    class Meta:
        model = DynamicBlob


class PopulationForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'source_file',
            submit_button()
        )
        return super().__init__(*args, **kwargs)
    class Meta:
        model = Population


class UnitForm(BaseForm):
    class Meta:
        model = Unit
        exclude = ['_population', '_final_state_code', '_final_control_state_code', '_final_detection_state_code', '_cum_infected', '_cum_detected', '_cum_destroyed', '_cum_vaccinated']
        widgets = {'production_type': AddOrSelect(attrs={'data-new-item-url': '/setup/ProductionType/new/'})}


class FunctionForm(BaseForm):
    class Meta:
        model = Function


class ProbabilityFunctionForm(BaseForm):
    class Meta:
        model = ProbabilityFunction


class RelationalFunctionForm(BaseForm):
    class Meta:
        model = RelationalFunction


class RelationalPointForm(BaseForm):
    class Meta:
        model = RelationalPoint
        exclude = []
        widgets = {'relational_function': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'})}


class ControlMasterPlanForm(BaseForm):
    class Meta:
        model = ControlMasterPlan
        exclude = []
        widgets = {'destruction_capacity': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'vaccination_capacity': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'})}


class ProtocolAssignmentForm(BaseForm):
    class Meta:
        model = ProtocolAssignment
        exclude = ['_master_plan', ]
        widgets = {'_master_plan': AddOrSelect(attrs={'data-new-item-url': '/setup/ControlMasterPlan/new/'}),
                   'production_type': FixedSelect(),
                   'control_protocol': AddOrSelect(attrs={'data-new-item-url': '/setup/ControlProtocol/new/'})}


class DiseaseProgressionAssignmentForm(BaseForm):
    class Meta:
        model = DiseaseProgressionAssignment
        # widgets = {'production_type': AddOrSelect(attrs={'data-new-item-url': '/setup/ProductionType/new/'}),
        #            'progression': AddOrSelect(attrs={'data-new-item-url': '/setup/DiseaseProgression/new/'})}


class ControlProtocolForm(BaseForm):
    """https://speakerdeck.com/maraujop/advanced-django-forms-usage slide 47
    http://stackoverflow.com/questions/19625211/bootstrap-linking-to-a-tab-with-an-url"""
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'name',
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
                    'direct_trace_success_rate',
                    'direct_trace_period',
                    'trace_indirect_forward',
                    'trace_indirect_back',
                    'indirect_trace_success',
                    'indirect_trace_period',
                    'trace_result_delay',
                    'direct_trace_is_a_zone_trigger',
                    'indirect_trace_is_a_zone_trigger',
                    ),
                Tab('Testing',
                    'use_testing',
                    'examine_direct_forward_traces',
                    'exam_direct_forward_success_multiplier',
                    'examine_indirect_forward_traces',
                    'exam_indirect_forward_success_multiplier',
                    'examine_direct_back_traces',
                    'exam_direct_back_success_multiplier',
                    'examine_indirect_back_traces',
                    'examine_indirect_back_success_multiplier',
                    'test_direct_forward_traces',
                    'test_indirect_forward_traces',
                    'test_direct_back_traces',
                    'test_indirect_back_traces',
                    'test_specificity',
                    'test_sensitivity',
                    'test_delay',
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
                    'vaccinate_retrospective_days',
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
        return super().__init__(*args, **kwargs)
    class Meta:
        model = ControlProtocol
        widgets = {'detection_probability_for_observed_time_in_clinical': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'detection_probability_report_vs_first_detection': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'trace_result_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'vaccine_immune_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'test_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'})}


class DiseaseForm(BaseForm):
    class Meta:
        model = Disease


class DiseaseProgressionForm(BaseForm):
    class Meta:
        model = DiseaseProgression
        exclude = ['_disease']
        try:
            if not Disease.objects.get(id=1).use_within_unit_prevalence:
                exclude.append('disease_prevalence')
        except (ObjectDoesNotExist, OperationalError):
            pass  # If someone hasn't created a Scenario yet, the field will show
        widgets = {'_disease': AddOrSelect(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'disease_latent_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'disease_subclinical_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'disease_clinical_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'disease_immune_period': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   'disease_prevalence': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'})}


class IndirectSpreadForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            # 'latent_animals_can_infect_others',  # Indirect doesn't have this field
            'subclinical_animals_can_infect_others',
            'use_fixed_contact_rate',
            'contact_rate',
            'infection_probability',
            'distance_distribution',
            'transport_delay',
            'movement_control',
            submit_button()
        )
        return super().__init__(*args, **kwargs)
    class Meta:
        model = IndirectSpread
        exclude = ['_spread_method_code', '_disease']
        widgets = {'distance_distribution': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   '_disease': AddOrSelect(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'movement_control': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'transport_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'})}


class DirectSpreadForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'latent_animals_can_infect_others',
            'subclinical_animals_can_infect_others',
            'use_fixed_contact_rate',
            'contact_rate',
            'infection_probability',
            'distance_distribution',
            'transport_delay',
            'movement_control',
            submit_button()
        )
        return super().__init__(*args, **kwargs)
    class Meta:
        model = DirectSpread
        exclude = ['_spread_method_code', '_disease']
        widgets = {'distance_distribution': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'}),
                   '_disease': AddOrSelect(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'movement_control': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'transport_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'})}


class AirborneSpreadForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'spread_1km_probability',
            'max_distance',
            'wind_direction_start',
            'wind_direction_end',
            'transport_delay',
            submit_button()
        )
        return super().__init__(*args, **kwargs)
    class Meta:
        model = AirborneSpread
        exclude = ['_spread_method_code', '_disease']
        try:
            if Disease.objects.get(id=1).use_airborne_exponential_decay:
                exclude.append('max_distance')
        except (ObjectDoesNotExist, OperationalError):
            pass
        widgets = {'_disease': AddOrSelect(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'movement_control': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'transport_delay': AddOrSelect(attrs={'data-new-item-url': '/setup/ProbabilityFunction/new/'})}


class ScenarioForm(BaseForm):
    class Meta:
        model = Scenario
        exclude = ['language', 'use_fixed_random_seed', 'random_seed']
        widgets = {'language': Select(attrs={'data-toggle-controller': 'language',
                                             'data-required-value': 'Spanish'})}


class OutputSettingsForm(BaseForm):
    class Meta:
        model = OutputSettings
        exclude = ['_scenario']
        widgets = {'save_all_daily_outputs': RadioSelect(),
            'maximum_iterations_for_daily_output': NumberInput(attrs={'data-toggle-controller': 'save_all_daily_outputs',
                                                                      'data-required-value': 'False'}),
            'days': NumberInput(
                attrs={'data-toggle-controller': 'stop_criteria',
                       'data-required-value': 'stop-days'})
        }


class ProductionTypeForm(BaseForm):
    class Meta:
        model = ProductionType


class ProductionTypePairTransmissionForm(BaseForm):
    class Meta:
        model = ProductionTypePairTransmission
        # widgets = {'source_production_type': AddOrSelect(attrs={'data-new-item-url': '/setup/ProductionType/new/'}),
        #            'destination_production_type': AddOrSelect(attrs={'data-new-item-url': '/setup/ProductionType/new/'}),
        #            'direct_contact_spread': AddOrSelect(attrs={'data-new-item-url': '/setup/DirectSpread/new/'}),
        #            'indirect_contact_spread': AddOrSelect(attrs={'data-new-item-url': '/setup/IndirectSpread/new/'}),
        #            'airborne_spread': AddOrSelect(attrs={'data-new-item-url': '/setup/AirborneSpread/new/'})}


class ZoneForm(BaseForm):
    class Meta:
        model = Zone


class ZoneEffectOnProductionTypeForm(BaseForm):
    class Meta:
        model = ZoneEffectOnProductionType
        widgets = {'zone': AddOrSelect(attrs={'data-new-item-url': '/setup/Zone/new/'}),
                   'production_type': AddOrSelect(attrs={'data-new-item-url': '/setup/ProductionType/new/'}),
                   'zone_indirect_movement': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'}),
                   'zone_direct_movement': AddOrSelect(attrs={'data-new-item-url': '/setup/RelationalFunction/new/'})}


class ReadAllCodesForm(BaseForm):
    class Meta:
        model = ReadAllCodes
        exclude = ['_code', '_code_type', '_code_description']


class ReadAllCodeTypesForm(BaseForm):
    class Meta:
        model = ReadAllCodeTypes
        exclude = ['_code_type', '_code_type_description']
