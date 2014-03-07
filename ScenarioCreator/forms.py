from ScenarioCreator.models import *
from floppyforms import ModelForm, Select, CharField


class Add_or_Select(Select):
    template_name = 'floppyforms/model_select.html'

    # def get_context(self, name, value, attrs=None, choices=()):
    #     context = super(Add_or_Select, self).get_context(name, value, attrs=None, choices=())
    #     context['attrs']['data-new-item-url'] = '/%s/new/' %


class DbSchemaVersionForm(ModelForm):
    class Meta:
        model = DbSchemaVersion


class DynamicBlobForm(ModelForm):
    class Meta:
        model = DynamicBlob


class DynamicUnitForm(ModelForm):
    class Meta:
        model = DynamicUnit
        exclude = ['_final_state_code', '_final_control_state_code', '_final_detection_state_code', '_cum_infected', '_cum_detected', '_cum_destroyed', '_cum_vaccinated']
        widgets = {'production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/ProductionType/new/'})}


class EquationForm(ModelForm):
    class Meta:
        model = Equation


class ProbabilityEquationForm(ModelForm):
    class Meta:
        model = ProbabilityEquation


class RelationalEquationForm(ModelForm):
    class Meta:
        model = RelationalEquation


class EquationPointForm(ModelForm):
    class Meta:
        model = EquationPoint
        exclude = ['_point_order']
        widgets = {'chart':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'})}


class ControlMasterPlanForm(ModelForm):
    class Meta:
        model = ControlMasterPlan
        exclude = ['_include_detection', '_include_tracing', '_include_tracing_unit_exam', '_include_tracing_testing', '_include_destruction', '_include_vaccination', '_include_zones']
        widgets = {'destruction_capacity_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'}),
                   'vaccination_capacity_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'})}


class ProtocolAssignmentForm(ModelForm):
    class Meta:
        model = ProtocolAssignment
        widgets = {'production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/ProductionType/new/'}),
                   'control_protocol':Add_or_Select(attrs={'data-new-item-url': '/setup/ControlProtocol/new/'}),
                   'master_plan':Add_or_Select(attrs={'data-new-item-url': '/setup/ControlMasterPlan/new/'})}


class ControlProtocolForm(ModelForm):
    class Meta:
        model = ControlProtocol
        widgets = {'detection_probability_for_observed_time_in_clinical_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'}),
                   'detection_probability_report_vs_first_detection_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'}),
                   'trace_delay_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'vaccine_immune_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'test_delay_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'})}


class DiseaseForm(ModelForm):
    class Meta:
        model = Disease


class DiseaseReactionForm(ModelForm):
    class Meta:
        model = DiseaseReaction
        widgets = {'disease':Add_or_Select(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'disease_latent_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'disease_subclinical_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'disease_clinical_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'disease_immune_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'disease_prevalence_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'})}


class DiseaseReactionAssignmentForm(ModelForm):
    class Meta:
        model = DiseaseReactionAssignment
        widgets = {'production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/ProductionType/new/'}),
                   'reaction':Add_or_Select(attrs={'data-new-item-url': '/setup/DiseaseReaction/new/'})}


class DiseaseSpreadModelForm(ModelForm):
    class Meta:
        model = DiseaseSpreadModel
        widgets = {'disease':Add_or_Select(attrs={'data-new-item-url': '/setup/Disease/new/'}),
                   'distance_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'movement_control_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'}),
                   'transport_delay_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'})}


class ScenarioForm(ModelForm):
    class Meta:
        model = Scenario


class ProductionTypeForm(ModelForm):
    class Meta:
        model = ProductionType


class ProductionTypePairTransmissionForm(ModelForm):
    class Meta:
        model = ProductionTypePairTransmission
        widgets = {'source_production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/ProductionType/new/'}),
                   'destination_production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/ProductionType/new/'}),
                   'direct_contact_spread_model':Add_or_Select(attrs={'data-new-item-url': '/setup/DiseaseSpreadModel/new/'}),
                   'indirect_contact_spread_model':Add_or_Select(attrs={'data-new-item-url': '/setup/DiseaseSpreadModel/new/'}),
                   'airborne_contact_spread_model':Add_or_Select(attrs={'data-new-item-url': '/setup/DiseaseSpreadModel/new/'})}


class ZoneForm(ModelForm):
    class Meta:
        model = Zone


class ZoneProductionTypeEffectForm(ModelForm):
    class Meta:
        model = ZoneProductionTypeEffect
        widgets = {'zone':Add_or_Select(attrs={'data-new-item-url': '/setup/Zone/new/'}),
                   'production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/ProductionType/new/'}),
                   'zone_indirect_movement_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'}),
                   'zone_direct_movement_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'})}


class ReadAllCodesForm(ModelForm):
    class Meta:
        model = ReadAllCodes
        exclude = ['_code', '_code_type', '_code_description']


class ReadAllCodeTypesForm(ModelForm):
    class Meta:
        model = ReadAllCodeTypes
        exclude = ['_code_type', '_code_type_description']

