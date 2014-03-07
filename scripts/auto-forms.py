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
        widgets = {'production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/InProductionType/new/'})}


class InChartForm(ModelForm):
    class Meta:
        model = InChart


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


class InControlGlobalForm(ModelForm):
    class Meta:
        model = InControlGlobal
        exclude = ['_include_detection', '_include_tracing', '_include_tracing_unit_exam', '_include_tracing_testing', '_include_destruction', '_include_vaccination', '_include_zones']
        widgets = {'destruction_capacity_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'}),
                   'vaccination_capacity_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'})}


class ProtocolAssignmentForm(ModelForm):
    class Meta:
        model = ProtocolAssignment
        widgets = {'production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/InProductionType/new/'}),
                   'control_protocol':Add_or_Select(attrs={'data-new-item-url': '/setup/ControlProtocol/new/'}),
                   'master_plan':Add_or_Select(attrs={'data-new-item-url': '/setup/InControlGlobal/new/'})}


class ControlProtocolForm(ModelForm):
    class Meta:
        model = ControlProtocol
        widgets = {'detection_probability_for_observed_time_in_clinical_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'}),
                   'detection_probability_report_vs_first_detection_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'}),
                   'trace_delay_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'vaccine_immune_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'test_delay_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'})}


class InDiseaseGlobalForm(ModelForm):
    class Meta:
        model = InDiseaseGlobal


class InDiseaseProductionTypeForm(ModelForm):
    class Meta:
        model = InDiseaseProductionType
        widgets = {'production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/InProductionType/new/'}),
                   'disease_latent_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'disease_subclinical_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'disease_clinical_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'disease_immune_period_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'disease_prevalence_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'})}


class InDiseaseSpreadForm(ModelForm):
    class Meta:
        model = InDiseaseSpread
        widgets = {'production_type_pair':Add_or_Select(attrs={'data-new-item-url': '/setup/InProductionTypePair/new/'}),
                   'distance_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'}),
                   'movement_control_relid':Add_or_Select(attrs={'data-new-item-url': '/setup/RelationalEquation/new/'}),
                   'transport_delay_pdf':Add_or_Select(attrs={'data-new-item-url': '/setup/ProbabilityEquation/new/'})}


class InGeneralForm(ModelForm):
    class Meta:
        model = InGeneral


class InProductionTypeForm(ModelForm):
    class Meta:
        model = InProductionType


class InProductionTypePairForm(ModelForm):
    class Meta:
        model = InProductionTypePair
        widgets = {'source_production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/InProductionType/new/'}),
                   'destination_production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/InProductionType/new/'}),
                   'direct_contact_spread_model':Add_or_Select(attrs={'data-new-item-url': '/setup/InDiseaseSpread/new/'}),
                   'indirect_contact_spread_model':Add_or_Select(attrs={'data-new-item-url': '/setup/InDiseaseSpread/new/'}),
                   'airborne_contact_spread_model':Add_or_Select(attrs={'data-new-item-url': '/setup/InDiseaseSpread/new/'})}


class InZoneForm(ModelForm):
    class Meta:
        model = InZone


class InZoneProductionTypeForm(ModelForm):
    class Meta:
        model = InZoneProductionType
        widgets = {'zone':Add_or_Select(attrs={'data-new-item-url': '/setup/InZone/new/'}),
                   'production_type':Add_or_Select(attrs={'data-new-item-url': '/setup/InProductionType/new/'}),
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

