class DbSchemaVersionForm(ModelForm):
    class Meta:
        model = DbSchemaVersion


class DynamicBlobForm(ModelForm):
    class Meta:
        model = DynamicBlob


class DynamicHerdForm(ModelForm):
    class Meta:
        model = DynamicHerd
        exclude = ['_final_state_code', '_final_control_state_code', '_final_detection_state_code', '_cum_infected', '_cum_detected', '_cum_destroyed', '_cum_vaccinated']


class InChartForm(ModelForm):
    class Meta:
        model = InChart
        exclude = ['_ispdf', '_notes']


class InChartDetailForm(ModelForm):
    class Meta:
        model = InChartDetail
        exclude = ['_chartid', '_pointorder', '_x', '_y']


class InControlGlobalForm(ModelForm):
    class Meta:
        model = InControlGlobal
        exclude = ['_destrcapacityrelid', '_vacccapacityrelid', '_vacccapacitystartrelid', '_vacccapacityrestartrelid']


class InControlPlanForm(ModelForm):
    class Meta:
        model = InControlPlan


class InControlsProductionTypeForm(ModelForm):
    class Meta:
        model = InControlsProductionType
        exclude = ['_detprobobsvstimeclinicalrelid', '_detprobreportvsfirstdetectionrelid', '_tracedelaypdfid', '_vaccimmuneperiodpdfid', '_testdelaypdfid']


class InDiseaseGlobalForm(ModelForm):
    class Meta:
        model = InDiseaseGlobal


class InDiseaseProductionTypeForm(ModelForm):
    class Meta:
        model = InDiseaseProductionType
        exclude = ['_production_type_id', '_dislatentperiodpdfid', '_dissubclinicalperiodpdfid', '_disclinicalperiodpdfid', '_disimmuneperiodpdfid', '_disprevalencerelid']


class InDiseaseSpreadForm(ModelForm):
    class Meta:
        model = InDiseaseSpread
        exclude = ['_productiontypepairid', '_distancepdfid', '_movementcontrolrelid', '_transportdelaypdfid']


class InGeneralForm(ModelForm):
    class Meta:
        model = InGeneral


class InProductionTypeForm(ModelForm):
    class Meta:
        model = InProductionType


class InProductionTypePairForm(ModelForm):
    class Meta:
        model = InProductionTypePair
        exclude = ['_sourceproductiontypeid', '_destproductiontypeid', '_directcontactspreadid', '_indirectcontactspreadid', '_airbornecontactspreadid']


class InZoneForm(ModelForm):
    class Meta:
        model = InZone


class InZoneProductionTypePairForm(ModelForm):
    class Meta:
        model = InZoneProductionTypePair
        exclude = ['_zoneid', '_production_type_id', '_zonedirectmovementrelid', '_zoneindirectmovementrelid']


class ReadAllCodesForm(ModelForm):
    class Meta:
        model = ReadAllCodes
        exclude = ['_code', '_code_type', '_code_description']


class ReadAllCodeTypesForm(ModelForm):
    class Meta:
        model = ReadAllCodeTypes
        exclude = ['_code_type', '_code_type_description']

