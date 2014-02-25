class DbschemaversionForm(ModelForm):
    class Meta:
        model = Dbschemaversion


class DynablobForm(ModelForm):
    class Meta:
        model = Dynablob


class DynaherdForm(ModelForm):
    class Meta:
        model = Dynaherd
        exclude = ['_final_state_code', '_final_control_state_code', '_final_detection_state_code', '_cum_infected', '_cum_detected', '_cum_destroyed', '_cum_vaccinated']


class InchartForm(ModelForm):
    class Meta:
        model = Inchart
        exclude = ['_ispdf', '_notes']


class InchartdetailForm(ModelForm):
    class Meta:
        model = Inchartdetail
        exclude = ['_chartid', '_pointorder', '_x', '_y']


class IncontrolglobalForm(ModelForm):
    class Meta:
        model = Incontrolglobal
        exclude = ['_destrcapacityrelid', '_vacccapacityrelid', '_vacccapacitystartrelid', '_vacccapacityrestartrelid']


class IncontrolplanForm(ModelForm):
    class Meta:
        model = Incontrolplan


class IncontrolsproductiontypeForm(ModelForm):
    class Meta:
        model = Incontrolsproductiontype
        exclude = ['_detprobobsvstimeclinicalrelid', '_detprobreportvsfirstdetectionrelid', '_tracedelaypdfid', '_vaccimmuneperiodpdfid', '_testdelaypdfid']


class IndiseaseglobalForm(ModelForm):
    class Meta:
        model = Indiseaseglobal


class IndiseaseproductiontypeForm(ModelForm):
    class Meta:
        model = Indiseaseproductiontype
        exclude = ['_production_type_id', '_dislatentperiodpdfid', '_dissubclinicalperiodpdfid', '_disclinicalperiodpdfid', '_disimmuneperiodpdfid', '_disprevalencerelid']


class IndiseasespreadForm(ModelForm):
    class Meta:
        model = Indiseasespread
        exclude = ['_productiontypepairid', '_distancepdfid', '_movementcontrolrelid', '_transportdelaypdfid']


class IngeneralForm(ModelForm):
    class Meta:
        model = Ingeneral


class InproductiontypeForm(ModelForm):
    class Meta:
        model = Inproductiontype


class InproductiontypepairForm(ModelForm):
    class Meta:
        model = Inproductiontypepair
        exclude = ['_sourceproductiontypeid', '_destproductiontypeid', '_directcontactspreadid', '_indirectcontactspreadid', '_airbornecontactspreadid']


class InzoneForm(ModelForm):
    class Meta:
        model = Inzone


class InzoneproductiontypepairForm(ModelForm):
    class Meta:
        model = Inzoneproductiontypepair
        exclude = ['_zoneid', '_production_type_id', '_zonedirectmovementrelid', '_zoneindirectmovementrelid']


class ReadallcodesForm(ModelForm):
    class Meta:
        model = Readallcodes
        exclude = ['_code', '_code_type', '_code_description']


class ReadallcodetypesForm(ModelForm):
    class Meta:
        model = Readallcodetypes
        exclude = ['_code_type', '_code_type_description']

