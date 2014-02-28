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


class InChartForm(ModelForm):
    class Meta:
        model = InChart
        exclude = ['_notes']


class ProbabilityEquationForm(ModelForm):
    class Meta:
        model = ProbabilityEquation


class RelationalEquationForm(ModelForm):
    class Meta:
        model = RelationalEquation


class EquationPointForm(ModelForm):
    class Meta:
        model = EquationPoint
        exclude = ['_point_order', '_x', '_y']


class InControlGlobalForm(ModelForm):
    class Meta:
        model = InControlGlobal


class InControlPlanForm(ModelForm):
    class Meta:
        model = InControlPlan


class InControlsProductionTypeForm(ModelForm):
    class Meta:
        model = InControlsProductionType


class InDiseaseGlobalForm(ModelForm):
    class Meta:
        model = InDiseaseGlobal


class InDiseaseProductionTypeForm(ModelForm):
    class Meta:
        model = InDiseaseProductionType


class InDiseaseSpreadForm(ModelForm):
    class Meta:
        model = InDiseaseSpread


class InGeneralForm(ModelForm):
    class Meta:
        model = InGeneral


class InProductionTypeForm(ModelForm):
    class Meta:
        model = InProductionType


class InProductionTypePairForm(ModelForm):
    class Meta:
        model = InProductionTypePair


class InZoneForm(ModelForm):
    class Meta:
        model = InZone


class InZoneProductionTypePairForm(ModelForm):
    class Meta:
        model = InZoneProductionTypePair


class ReadAllCodesForm(ModelForm):
    class Meta:
        model = ReadAllCodes
        exclude = ['_code', '_code_type', '_code_description']


class ReadAllCodeTypesForm(ModelForm):
    class Meta:
        model = ReadAllCodeTypes
        exclude = ['_code_type', '_code_type_description']

