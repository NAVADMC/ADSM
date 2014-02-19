# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Dbschemaversion(models.Model):
    version_number = models.TextField(unique=True)
    version_application = models.TextField()
    version_date = models.TextField()
    version_info_url = models.TextField(blank=True)
    version_id = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'dbschemaversion'

class Dynablob(models.Model):
    dynblob_id = models.TextField(unique=True)
    zone_perimeters = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'dynablob'

class Dynaherd(models.Model):
    herd_id = models.IntegerField(unique=True)
    productiontypeid = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    initial_state_code = models.TextField()
    days_in_initial_state = models.IntegerField()
    days_left_in_initial_state = models.IntegerField()
    initial_size = models.IntegerField()
    final_state_code = models.TextField(blank=True)
    final_control_state_code = models.TextField(blank=True)
    final_detection_state_code = models.TextField(blank=True)
    cum_infected = models.IntegerField(blank=True, null=True)
    cum_detected = models.IntegerField(blank=True, null=True)
    cum_destroyed = models.IntegerField(blank=True, null=True)
    cum_vaccinated = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'dynaherd'

class Inchart(models.Model):
    chartid = models.IntegerField(unique=True)
    fieldname = models.TextField(blank=True)
    chart_name = models.TextField()
    ispdf = models.IntegerField()
    chart_type = models.TextField(blank=True)
    mean = models.FloatField(blank=True, null=True)
    std_dev = models.FloatField(blank=True, null=True)
    min = models.FloatField(blank=True, null=True)
    mode = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)
    alpha = models.FloatField(blank=True, null=True)
    alpha2 = models.FloatField(blank=True, null=True)
    beta = models.FloatField(blank=True, null=True)
    location = models.FloatField(blank=True, null=True)
    scale = models.FloatField(blank=True, null=True)
    shape = models.FloatField(blank=True, null=True)
    n = models.IntegerField(blank=True, null=True)
    p = models.FloatField(blank=True, null=True)
    m = models.IntegerField(blank=True, null=True)
    d = models.IntegerField(blank=True, null=True)
    dmin = models.IntegerField(blank=True, null=True)
    dmax = models.IntegerField(blank=True, null=True)
    theta = models.FloatField(blank=True, null=True)
    a = models.FloatField(blank=True, null=True)
    s = models.IntegerField(blank=True, null=True)
    x_axis_units = models.TextField(blank=True)
    y_axis_units = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'inchart'

class Inchartdetail(models.Model):
    chartid = models.IntegerField()
    pointorder = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    class Meta:
        managed = False
        db_table = 'inchartdetail'

class Incontrolsglobal(models.Model):
    controlsglobalid = models.TextField()
    include_detection = models.IntegerField()
    include_tracing = models.IntegerField()
    include_tracing_herd_exam = models.IntegerField()
    include_tracing_testing = models.IntegerField()
    include_destruction = models.IntegerField()
    destruction_delay = models.IntegerField(blank=True, null=True)
    destrcapacityrelid = models.IntegerField(blank=True, null=True)
    destruction_priority_order = models.TextField(blank=True)
    destrucion_reason_order = models.TextField(blank=True)
    include_vaccination = models.IntegerField()
    vaccincation_detected_units_before_start = models.IntegerField(blank=True, null=True)
    vacccapacityrelid = models.IntegerField(blank=True, null=True)
    vaccination_priority_order = models.TextField(blank=True)
    include_zones = models.IntegerField()
    vaccination_retrospective_days = models.IntegerField(blank=True, null=True)
    vacccapacitystartrelid = models.IntegerField(blank=True, null=True)
    vacccapacityrestartrelid = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'incontrolsglobal'

class Indiseasespread(models.Model):
    productiontypepairid = models.IntegerField(unique=True)
    spreadmethodcode = models.TextField(blank=True)
    latent_can_infect = models.IntegerField(blank=True, null=True)
    subclinical_can_infect = models.IntegerField(blank=True, null=True)
    mean_contact_rate = models.FloatField(blank=True, null=True)
    use_fixed_contact_rate = models.IntegerField(blank=True, null=True)
    fixed_contact_rate = models.FloatField(blank=True, null=True)
    infection_probability = models.FloatField(blank=True, null=True)
    distancepdfid = models.IntegerField(blank=True, null=True)
    movementcontrolrelid = models.IntegerField(blank=True, null=True)
    transportdelaypdfid = models.IntegerField(blank=True, null=True)
    probairbornespread1km = models.FloatField(blank=True, null=True)
    maxdistairbornespread = models.FloatField(blank=True, null=True)
    wind_direction_start = models.IntegerField(blank=True, null=True)
    wind_direction_end = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'indiseasespread'

class Ingeneral(models.Model):
    ingeneralid = models.TextField(blank=True)
    language = models.CharField(max_length=12)
    frequency = models.CharField(db_column='Frequency', max_length=200, blank=True) # Field name made lowercase.
    scenario_description = models.TextField(blank=True)
    iterations = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    simstopreason = models.TextField(blank=True)
    includecontactspread = models.IntegerField(blank=True, null=True)
    includeairbornespread = models.IntegerField(blank=True, null=True)
    use_airborne_exponential_decay = models.IntegerField(blank=True, null=True)
    use_within_herd_prevalence = models.IntegerField(blank=True, null=True)
    cost_track_destruction = models.IntegerField(blank=True, null=True)
    cost_track_vaccination = models.IntegerField(blank=True, null=True)
    cost_track_zone_surveillance = models.IntegerField(blank=True, null=True)
    use_fixed_random_seed = models.IntegerField(blank=True, null=True)
    randomseed = models.IntegerField(blank=True, null=True)
    save_all_daily_outputs = models.IntegerField(blank=True, null=True)
    save_daily_outputs_for_iterations = models.IntegerField(blank=True, null=True)
    write_daily_states_file = models.IntegerField(blank=True, null=True)
    daily_states_filename = models.TextField(blank=True)
    save_daily_events = models.IntegerField(blank=True, null=True)
    save_daily_exposures = models.IntegerField(blank=True, null=True)
    save_iteration_outputs_for_herds = models.IntegerField(blank=True, null=True)
    write_map_output = models.IntegerField(blank=True, null=True)
    map_directory = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'ingeneral'

class Ingroup(models.Model):
    groupid = models.IntegerField(unique=True)
    subgroupid = models.IntegerField()
    groupproductiontypes = models.TextField()
    class Meta:
        managed = False
        db_table = 'ingroup'

class Inproductiontype(models.Model):
    production_type_id = models.IntegerField(unique=True)
    production_type_name = models.TextField()
    use_disease_transition = models.IntegerField(blank=True, null=True)
    dislatentperiodpdfid = models.IntegerField(blank=True, null=True)
    dissubclinicalperiodpdfid = models.IntegerField(blank=True, null=True)
    disclinicalperiodpdfid = models.IntegerField(blank=True, null=True)
    disimmuneperiodpdfid = models.IntegerField(blank=True, null=True)
    disprevalencerelid = models.IntegerField(blank=True, null=True)
    use_detection = models.IntegerField(blank=True, null=True)
    detprobobsvstimeclinicalrelid = models.IntegerField(blank=True, null=True)
    detprobreportvsfirstdetectionrelid = models.IntegerField(blank=True, null=True)
    trace_direct_forward = models.IntegerField(blank=True, null=True)
    trace_direct_back = models.IntegerField(blank=True, null=True)
    trace_direct_success = models.FloatField(blank=True, null=True)
    trace_direct_trace_period = models.IntegerField(blank=True, null=True)
    trace_indirect_forward = models.IntegerField(blank=True, null=True)
    trace_indirect_back = models.IntegerField(blank=True, null=True)
    trace_indirect_success = models.FloatField(blank=True, null=True)
    trace_indirect_trace_period = models.IntegerField(blank=True, null=True)
    tracedelaypdfid = models.IntegerField(blank=True, null=True)
    use_destruction = models.IntegerField(blank=True, null=True)
    destruction_is_ring_trigger = models.IntegerField(blank=True, null=True)
    destruction_ring_radius = models.FloatField(blank=True, null=True)
    destruction_is_ring_target = models.IntegerField(blank=True, null=True)
    destroy_direct_forward_traces = models.IntegerField(blank=True, null=True)
    destroy_indirect_forward_traces = models.IntegerField(blank=True, null=True)
    destroy_direct_back_traces = models.IntegerField(blank=True, null=True)
    destroy_indirect_back_traces = models.IntegerField(blank=True, null=True)
    destruction_priority = models.IntegerField(blank=True, null=True)
    use_vaccination = models.IntegerField(blank=True, null=True)
    vacc_min_time_between_vaccinations = models.IntegerField(blank=True, null=True)
    vacc_vaccinate_detected = models.IntegerField(blank=True, null=True)
    vacc_days_to_immunity = models.IntegerField(blank=True, null=True)
    vaccimmuneperiodpdfid = models.IntegerField(blank=True, null=True)
    vacc_ring = models.IntegerField(blank=True, null=True)
    vacc_ring_radius = models.FloatField(blank=True, null=True)
    vacc_priority = models.IntegerField(blank=True, null=True)
    cost_destr_appraisal_per_unit = models.FloatField(blank=True, null=True)
    cost_destr_cleaning_per_unit = models.FloatField(blank=True, null=True)
    cost_destr_euthanasia_per_animal = models.FloatField(blank=True, null=True)
    cost_destr_indemnification_per_animal = models.FloatField(blank=True, null=True)
    cost_destr_disposal_per_animal = models.FloatField(blank=True, null=True)
    cost_vacc_setup_per_unit = models.FloatField(blank=True, null=True)
    cost_vacc_threshold = models.IntegerField(blank=True, null=True)
    cost_vacc_baseline_per_animal = models.FloatField(blank=True, null=True)
    cost_vacc_additional_per_animal = models.FloatField(blank=True, null=True)
    zone_detection_is_trigger = models.IntegerField(blank=True, null=True)
    zone_direct_trace_is_trigger = models.IntegerField(blank=True, null=True)
    zone_indirect_trace_is_trigger = models.IntegerField(blank=True, null=True)
    exam_direct_forward = models.IntegerField(blank=True, null=True)
    exam_direct_forward_multiplier = models.FloatField(blank=True, null=True)
    exam_indirect_forward = models.IntegerField(blank=True, null=True)
    exam_indirect_forward_multiplier = models.FloatField(blank=True, null=True)
    exam_direc_tback = models.IntegerField(blank=True, null=True)
    exam_direct_back_multiplier = models.FloatField(blank=True, null=True)
    exam_indirect_back = models.IntegerField(blank=True, null=True)
    exam_indirect_back_multiplier = models.FloatField(blank=True, null=True)
    test_direct_forward = models.IntegerField(blank=True, null=True)
    test_indirect_forward = models.IntegerField(blank=True, null=True)
    test_direct_back = models.IntegerField(blank=True, null=True)
    test_indirect_back = models.IntegerField(blank=True, null=True)
    test_specificity = models.FloatField(blank=True, null=True)
    test_sensitivity = models.FloatField(blank=True, null=True)
    testdelaypdfid = models.IntegerField(blank=True, null=True)
    vacc_restrospective_days = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'inproductiontype'

class Inproductiontypepair(models.Model):
    productiontypepairid = models.TextField(unique=True) # This field type is a guess.
    sourceproductiontypeid = models.IntegerField()
    destproductiontypeid = models.IntegerField()
    use_direct_contact = models.IntegerField()
    directcontactspreadid = models.IntegerField(blank=True, null=True)
    use_indirect_contact = models.IntegerField()
    indirectcontactspreadid = models.IntegerField(blank=True, null=True)
    use_airborne_spread = models.IntegerField()
    airbornecontactspreadid = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'inproductiontypepair'

class Intrigger(models.Model):
    triggerid = models.IntegerField(unique=True)
    triggercode = models.IntegerField()
    trigger_days = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'intrigger'

class Inzone(models.Model):
    zoneid = models.IntegerField(unique=True)
    zone_description = models.TextField()
    zone_radius = models.FloatField()
    class Meta:
        managed = False
        db_table = 'inzone'

class Inzoneproductiontypepair(models.Model):
    inzoneproductiontypepairid = models.IntegerField(unique=True)
    zoneid = models.IntegerField()
    productiontypeid = models.IntegerField()
    use_directmovement_control = models.IntegerField()
    zonedirectmovementrelid = models.IntegerField(blank=True, null=True)
    use_indirect_movement_control = models.IntegerField()
    zoneindirectmovementrelid = models.IntegerField(blank=True, null=True)
    use_detection_multiplier = models.IntegerField()
    zone_detection_multiplier = models.FloatField(blank=True, null=True)
    cost_surv_per_animal_day = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'inzoneproductiontypepair'

class Outdailybyproductiontype(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    productiontypeid = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    tsdususc = models.IntegerField(blank=True, null=True)
    tsdasusc = models.IntegerField(blank=True, null=True)
    tsdulat = models.IntegerField(blank=True, null=True)
    tsdalat = models.IntegerField(blank=True, null=True)
    tsdusubc = models.IntegerField(blank=True, null=True)
    tsdasubc = models.IntegerField(blank=True, null=True)
    tsduclin = models.IntegerField(blank=True, null=True)
    tsdaclin = models.IntegerField(blank=True, null=True)
    tsdunimm = models.IntegerField(blank=True, null=True)
    tsdanimm = models.IntegerField(blank=True, null=True)
    tsduvimm = models.IntegerField(blank=True, null=True)
    tsdavimm = models.IntegerField(blank=True, null=True)
    tsdudest = models.IntegerField(blank=True, null=True)
    tsdadest = models.IntegerField(blank=True, null=True)
    tscususc = models.IntegerField(blank=True, null=True)
    tscasusc = models.IntegerField(blank=True, null=True)
    tsculat = models.IntegerField(blank=True, null=True)
    tscalat = models.IntegerField(blank=True, null=True)
    tscusubc = models.IntegerField(blank=True, null=True)
    tscasubc = models.IntegerField(blank=True, null=True)
    tscuclin = models.IntegerField(blank=True, null=True)
    tscaclin = models.IntegerField(blank=True, null=True)
    tscunimm = models.IntegerField(blank=True, null=True)
    tscanimm = models.IntegerField(blank=True, null=True)
    tscuvimm = models.IntegerField(blank=True, null=True)
    tscavimm = models.IntegerField(blank=True, null=True)
    tscudest = models.IntegerField(blank=True, null=True)
    tscadest = models.IntegerField(blank=True, null=True)
    infnuair = models.IntegerField(blank=True, null=True)
    infnaair = models.IntegerField(blank=True, null=True)
    infnudir = models.IntegerField(blank=True, null=True)
    infnadir = models.IntegerField(blank=True, null=True)
    infnuind = models.IntegerField(blank=True, null=True)
    infnaind = models.IntegerField(blank=True, null=True)
    infcuini = models.IntegerField(blank=True, null=True)
    infcaini = models.IntegerField(blank=True, null=True)
    infcuair = models.IntegerField(blank=True, null=True)
    infcaair = models.IntegerField(blank=True, null=True)
    infcudir = models.IntegerField(blank=True, null=True)
    infcadir = models.IntegerField(blank=True, null=True)
    infcuind = models.IntegerField(blank=True, null=True)
    infcaind = models.IntegerField(blank=True, null=True)
    expcudir = models.IntegerField(blank=True, null=True)
    expcadir = models.IntegerField(blank=True, null=True)
    expcuind = models.IntegerField(blank=True, null=True)
    expcaind = models.IntegerField(blank=True, null=True)
    trcudirfwd = models.IntegerField(blank=True, null=True)
    trcadirfwd = models.IntegerField(blank=True, null=True)
    trcuindfwd = models.IntegerField(blank=True, null=True)
    trcaindfwd = models.IntegerField(blank=True, null=True)
    trcudirpfwd = models.IntegerField(blank=True, null=True)
    trcadirpfwd = models.IntegerField(blank=True, null=True)
    trcuindpfwd = models.IntegerField(blank=True, null=True)
    trcaindpfwd = models.IntegerField(blank=True, null=True)
    tocudirfwd = models.IntegerField(blank=True, null=True)
    tocuindfwd = models.IntegerField(blank=True, null=True)
    tocudirback = models.IntegerField(blank=True, null=True)
    tocuindback = models.IntegerField(blank=True, null=True)
    trnudirfwd = models.IntegerField(blank=True, null=True)
    trnadirfwd = models.IntegerField(blank=True, null=True)
    trnuindfwd = models.IntegerField(blank=True, null=True)
    trnaindfwd = models.IntegerField(blank=True, null=True)
    trcudirback = models.IntegerField(blank=True, null=True)
    trcadirback = models.IntegerField(blank=True, null=True)
    trcuindback = models.IntegerField(blank=True, null=True)
    trcaindback = models.IntegerField(blank=True, null=True)
    trcudirpback = models.IntegerField(blank=True, null=True)
    trcadirpback = models.IntegerField(blank=True, null=True)
    trcuindpback = models.IntegerField(blank=True, null=True)
    trcaindpback = models.IntegerField(blank=True, null=True)
    trnudirback = models.IntegerField(blank=True, null=True)
    trnadirback = models.IntegerField(blank=True, null=True)
    trnuindback = models.IntegerField(blank=True, null=True)
    trnaindback = models.IntegerField(blank=True, null=True)
    tonudirfwd = models.IntegerField(blank=True, null=True)
    tonuindfwd = models.IntegerField(blank=True, null=True)
    tonudirback = models.IntegerField(blank=True, null=True)
    tonuindback = models.IntegerField(blank=True, null=True)
    exmcudirfwd = models.IntegerField(blank=True, null=True)
    exmcadirfwd = models.IntegerField(blank=True, null=True)
    exmcuindfwd = models.IntegerField(blank=True, null=True)
    exmcaindfwd = models.IntegerField(blank=True, null=True)
    exmcudirback = models.IntegerField(blank=True, null=True)
    exmcadirback = models.IntegerField(blank=True, null=True)
    exmcuindback = models.IntegerField(blank=True, null=True)
    exmcaindback = models.IntegerField(blank=True, null=True)
    exmnuall = models.IntegerField(blank=True, null=True)
    exmnaall = models.IntegerField(blank=True, null=True)
    tstcudirfwd = models.IntegerField(blank=True, null=True)
    tstcadirfwd = models.IntegerField(blank=True, null=True)
    tstcuindfwd = models.IntegerField(blank=True, null=True)
    tstcaindfwd = models.IntegerField(blank=True, null=True)
    tstcudirback = models.IntegerField(blank=True, null=True)
    tstcadirback = models.IntegerField(blank=True, null=True)
    tstcuindback = models.IntegerField(blank=True, null=True)
    tstcaindback = models.IntegerField(blank=True, null=True)
    tstcutruepos = models.IntegerField(blank=True, null=True)
    tstcatruepos = models.IntegerField(blank=True, null=True)
    tstnutruepos = models.IntegerField(blank=True, null=True)
    tstnatruepos = models.IntegerField(blank=True, null=True)
    tstcutrueneg = models.IntegerField(blank=True, null=True)
    tstcatrueneg = models.IntegerField(blank=True, null=True)
    tstnutrueneg = models.IntegerField(blank=True, null=True)
    tstnatrueneg = models.IntegerField(blank=True, null=True)
    tstcufalsepos = models.IntegerField(blank=True, null=True)
    tstcafalsepos = models.IntegerField(blank=True, null=True)
    tstnufalsepos = models.IntegerField(blank=True, null=True)
    tstnafalsepos = models.IntegerField(blank=True, null=True)
    tstcufalseneg = models.IntegerField(blank=True, null=True)
    tstcafalseneg = models.IntegerField(blank=True, null=True)
    tstnufalseneg = models.IntegerField(blank=True, null=True)
    tstnafalseneg = models.IntegerField(blank=True, null=True)
    detnuclin = models.IntegerField(blank=True, null=True)
    detnaclin = models.IntegerField(blank=True, null=True)
    detcuclin = models.IntegerField(blank=True, null=True)
    detcaclin = models.IntegerField(blank=True, null=True)
    detnutest = models.IntegerField(blank=True, null=True)
    detnatest = models.IntegerField(blank=True, null=True)
    detcutest = models.IntegerField(blank=True, null=True)
    detcatest = models.IntegerField(blank=True, null=True)
    descuini = models.IntegerField(blank=True, null=True)
    descaini = models.IntegerField(blank=True, null=True)
    descudet = models.IntegerField(blank=True, null=True)
    descadet = models.IntegerField(blank=True, null=True)
    descudirfwd = models.IntegerField(blank=True, null=True)
    descadirfwd = models.IntegerField(blank=True, null=True)
    descuindfwd = models.IntegerField(blank=True, null=True)
    descaindfwd = models.IntegerField(blank=True, null=True)
    descudirback = models.IntegerField(blank=True, null=True)
    descadirback = models.IntegerField(blank=True, null=True)
    descuindback = models.IntegerField(blank=True, null=True)
    descaindback = models.IntegerField(blank=True, null=True)
    descuring = models.IntegerField(blank=True, null=True)
    descaring = models.IntegerField(blank=True, null=True)
    desnuall = models.IntegerField(blank=True, null=True)
    desnaall = models.IntegerField(blank=True, null=True)
    deswuall = models.IntegerField(blank=True, null=True)
    deswaall = models.IntegerField(blank=True, null=True)
    vaccuini = models.IntegerField(blank=True, null=True)
    vaccaini = models.IntegerField(blank=True, null=True)
    vaccuring = models.IntegerField(blank=True, null=True)
    vaccaring = models.IntegerField(blank=True, null=True)
    vacnuall = models.IntegerField(blank=True, null=True)
    vacnaall = models.IntegerField(blank=True, null=True)
    vacwuall = models.IntegerField(blank=True, null=True)
    vacwaall = models.IntegerField(blank=True, null=True)
    zonnfoci = models.IntegerField(blank=True, null=True)
    zoncfoci = models.IntegerField(blank=True, null=True)
    appduinfectious = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outdailybyproductiontype'

class Outdailybyzone(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    zoneid = models.IntegerField(blank=True, null=True)
    zonearea = models.FloatField(blank=True, null=True)
    zoneperimeter = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outdailybyzone'

class Outdailybyzoneandproductiontype(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    zoneid = models.IntegerField(blank=True, null=True)
    productiontypeid = models.IntegerField(blank=True, null=True)
    unitdaysinzone = models.IntegerField(blank=True, null=True)
    animaldaysinzone = models.IntegerField(blank=True, null=True)
    unitsinzone = models.IntegerField(blank=True, null=True)
    animalsinzone = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outdailybyzoneandproductiontype'

class Outdailyevents(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    event = models.IntegerField(blank=True, null=True)
    herdid = models.IntegerField(blank=True, null=True)
    zoneid = models.IntegerField(blank=True, null=True)
    eventcode = models.TextField(blank=True)
    newstatecode = models.TextField(blank=True)
    testresultcode = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'outdailyevents'

class Outdailyexposures(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    exposure = models.IntegerField(blank=True, null=True)
    initiatedday = models.IntegerField(blank=True, null=True)
    exposedherdid = models.IntegerField(blank=True, null=True)
    exposedzoneid = models.IntegerField(blank=True, null=True)
    exposingherdid = models.IntegerField(blank=True, null=True)
    exposingzoneid = models.IntegerField(blank=True, null=True)
    spreadmethodcode = models.TextField(blank=True)
    isadequate = models.IntegerField(blank=True, null=True)
    exposingherdstatuscode = models.TextField(blank=True)
    exposedherdstatuscode = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'outdailyexposures'

class Outepidemiccurves(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    productiontypeid = models.IntegerField(blank=True, null=True)
    infectedunits = models.IntegerField(blank=True, null=True)
    infectedanimals = models.IntegerField(blank=True, null=True)
    detectedunits = models.IntegerField(blank=True, null=True)
    detectedanimals = models.IntegerField(blank=True, null=True)
    infectiousunits = models.IntegerField(blank=True, null=True)
    apparentinfectiousunits = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outepidemiccurves'

class Outgeneral(models.Model):
    outgeneralid = models.TextField(blank=True)
    simulationstarttime = models.TextField(blank=True)
    simulationendtime = models.TextField(blank=True)
    completediterations = models.IntegerField(blank=True, null=True)
    version = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'outgeneral'

class Outiteration(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    diseaseended = models.IntegerField(blank=True, null=True)
    diseaseendday = models.IntegerField(blank=True, null=True)
    outbreakended = models.IntegerField(blank=True, null=True)
    outbreakendday = models.IntegerField(blank=True, null=True)
    zonefocicreated = models.IntegerField(blank=True, null=True)
    deswumax = models.IntegerField(blank=True, null=True)
    deswumaxday = models.IntegerField(blank=True, null=True)
    deswamax = models.FloatField(blank=True, null=True)
    deswamaxday = models.IntegerField(blank=True, null=True)
    deswutimemax = models.IntegerField(blank=True, null=True)
    deswutimeavg = models.FloatField(blank=True, null=True)
    vacwumax = models.IntegerField(blank=True, null=True)
    vacwumaxday = models.IntegerField(blank=True, null=True)
    vacwamax = models.FloatField(blank=True, null=True)
    vacwamaxday = models.IntegerField(blank=True, null=True)
    vacwutimemax = models.IntegerField(blank=True, null=True)
    vacwutimeavg = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outiteration'

class Outiterationbyherd(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    herdid = models.IntegerField(blank=True, null=True)
    laststatuscode = models.TextField(blank=True)
    laststatusday = models.IntegerField(blank=True, null=True)
    lastcontrolstatecode = models.TextField(blank=True)
    lastcontrolstateday = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outiterationbyherd'

class Outiterationbyproductiontype(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    productiontypeid = models.IntegerField(blank=True, null=True)
    tscususc = models.IntegerField(blank=True, null=True)
    tscasusc = models.IntegerField(blank=True, null=True)
    tsculat = models.IntegerField(blank=True, null=True)
    tscalat = models.IntegerField(blank=True, null=True)
    tscusubc = models.IntegerField(blank=True, null=True)
    tscasubc = models.IntegerField(blank=True, null=True)
    tscuclin = models.IntegerField(blank=True, null=True)
    tscaclin = models.IntegerField(blank=True, null=True)
    tscunimm = models.IntegerField(blank=True, null=True)
    tscanimm = models.IntegerField(blank=True, null=True)
    tscuvimm = models.IntegerField(blank=True, null=True)
    tscavimm = models.IntegerField(blank=True, null=True)
    tscudest = models.IntegerField(blank=True, null=True)
    tscadest = models.IntegerField(blank=True, null=True)
    infcuini = models.IntegerField(blank=True, null=True)
    infcaini = models.IntegerField(blank=True, null=True)
    infcuair = models.IntegerField(blank=True, null=True)
    infcaair = models.IntegerField(blank=True, null=True)
    infcudir = models.IntegerField(blank=True, null=True)
    infcadir = models.IntegerField(blank=True, null=True)
    infcuind = models.IntegerField(blank=True, null=True)
    infcaind = models.IntegerField(blank=True, null=True)
    expcudir = models.IntegerField(blank=True, null=True)
    expcadir = models.IntegerField(blank=True, null=True)
    expcuind = models.IntegerField(blank=True, null=True)
    expcaind = models.IntegerField(blank=True, null=True)
    trcudirfwd = models.IntegerField(blank=True, null=True)
    trcadirfwd = models.IntegerField(blank=True, null=True)
    trcuindfwd = models.IntegerField(blank=True, null=True)
    trcaindfwd = models.IntegerField(blank=True, null=True)
    trcudirpfwd = models.IntegerField(blank=True, null=True)
    trcadirpfwd = models.IntegerField(blank=True, null=True)
    trcuindpfwd = models.IntegerField(blank=True, null=True)
    trcaindpfwd = models.IntegerField(blank=True, null=True)
    trcudirback = models.IntegerField(blank=True, null=True)
    trcadirback = models.IntegerField(blank=True, null=True)
    trcuindback = models.IntegerField(blank=True, null=True)
    trcaindback = models.IntegerField(blank=True, null=True)
    trcudirpback = models.IntegerField(blank=True, null=True)
    trcadirpback = models.IntegerField(blank=True, null=True)
    trcuindpback = models.IntegerField(blank=True, null=True)
    trcaindpback = models.IntegerField(blank=True, null=True)
    tocudirfwd = models.IntegerField(blank=True, null=True)
    tocuindfwd = models.IntegerField(blank=True, null=True)
    tocudirback = models.IntegerField(blank=True, null=True)
    tocuindback = models.IntegerField(blank=True, null=True)
    exmcudirfwd = models.IntegerField(blank=True, null=True)
    exmcadirfwd = models.IntegerField(blank=True, null=True)
    exmcuindfwd = models.IntegerField(blank=True, null=True)
    exmcaindfwd = models.IntegerField(blank=True, null=True)
    exmcudirback = models.IntegerField(blank=True, null=True)
    exmcadirback = models.IntegerField(blank=True, null=True)
    exmcuindback = models.IntegerField(blank=True, null=True)
    exmcaindback = models.IntegerField(blank=True, null=True)
    tstcudirfwd = models.IntegerField(blank=True, null=True)
    tstcadirfwd = models.IntegerField(blank=True, null=True)
    tstcuindfwd = models.IntegerField(blank=True, null=True)
    tstcaindfwd = models.IntegerField(blank=True, null=True)
    tstcudirback = models.IntegerField(blank=True, null=True)
    tstcadirback = models.IntegerField(blank=True, null=True)
    tstcuindback = models.IntegerField(blank=True, null=True)
    tstcaindback = models.IntegerField(blank=True, null=True)
    tstcutruepos = models.IntegerField(blank=True, null=True)
    tstcatruepos = models.IntegerField(blank=True, null=True)
    tstcutrueneg = models.IntegerField(blank=True, null=True)
    tstcatrueneg = models.IntegerField(blank=True, null=True)
    tstcufalsepos = models.IntegerField(blank=True, null=True)
    tstcafalsepos = models.IntegerField(blank=True, null=True)
    tstcufalseneg = models.IntegerField(blank=True, null=True)
    tstcafalseneg = models.IntegerField(blank=True, null=True)
    detcuclin = models.IntegerField(blank=True, null=True)
    detcaclin = models.IntegerField(blank=True, null=True)
    detcutest = models.IntegerField(blank=True, null=True)
    detcatest = models.IntegerField(blank=True, null=True)
    descuini = models.IntegerField(blank=True, null=True)
    descaini = models.IntegerField(blank=True, null=True)
    descudet = models.IntegerField(blank=True, null=True)
    descadet = models.IntegerField(blank=True, null=True)
    descudirfwd = models.IntegerField(blank=True, null=True)
    descadirfwd = models.IntegerField(blank=True, null=True)
    descuindfwd = models.IntegerField(blank=True, null=True)
    descaindfwd = models.IntegerField(blank=True, null=True)
    descudirback = models.IntegerField(blank=True, null=True)
    descadirback = models.IntegerField(blank=True, null=True)
    descuindback = models.IntegerField(blank=True, null=True)
    descaindback = models.IntegerField(blank=True, null=True)
    descuring = models.IntegerField(blank=True, null=True)
    descaring = models.IntegerField(blank=True, null=True)
    deswumax = models.IntegerField(blank=True, null=True)
    deswamax = models.TextField(blank=True) # This field type is a guess.
    deswamaxday = models.IntegerField(blank=True, null=True)
    deswutimemax = models.IntegerField(blank=True, null=True)
    deswutimeavg = models.TextField(blank=True) # This field type is a guess.
    vaccaini = models.IntegerField(blank=True, null=True)
    vaccuring = models.IntegerField(blank=True, null=True)
    vaccaring = models.IntegerField(blank=True, null=True)
    vacwumax = models.IntegerField(blank=True, null=True)
    vacwamax = models.TextField(blank=True) # This field type is a guess.
    vacwamaxday = models.IntegerField(blank=True, null=True)
    vacwutimemax = models.TextField(blank=True) # This field type is a guess.
    zoncfoci = models.IntegerField(blank=True, null=True)
    firstdetection = models.IntegerField(blank=True, null=True)
    firstdetuinf = models.IntegerField(blank=True, null=True)
    firstdetainf = models.IntegerField(blank=True, null=True)
    firstdestruction = models.IntegerField(blank=True, null=True)
    firstvaccination = models.IntegerField(blank=True, null=True)
    lastdetection = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outiterationbyproductiontype'

class Outiterationbyzone(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    zoneid = models.IntegerField(blank=True, null=True)
    maxzonearea = models.FloatField(blank=True, null=True)
    maxzoneareaday = models.IntegerField(blank=True, null=True)
    finalzonearea = models.FloatField(blank=True, null=True)
    maxzoneperimeter = models.FloatField(blank=True, null=True)
    maxzoneperimeterday = models.IntegerField(blank=True, null=True)
    finalzoneperimeter = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outiterationbyzone'

class Outiterationbyzoneandproductiontype(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    zoneid = models.IntegerField(blank=True, null=True)
    productiontypeid = models.IntegerField(blank=True, null=True)
    unitdaysinzone = models.IntegerField(blank=True, null=True)
    animaldaysinzone = models.IntegerField(blank=True, null=True)
    costsurveillance = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outiterationbyzoneandproductiontype'

class Outiterationcosts(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    productiontypeid = models.IntegerField(blank=True, null=True)
    destrappraisal = models.FloatField(blank=True, null=True)
    destrcleaning = models.FloatField(blank=True, null=True)
    destreuthanasia = models.FloatField(blank=True, null=True)
    destrindemnification = models.FloatField(blank=True, null=True)
    destrdisposal = models.FloatField(blank=True, null=True)
    vaccsetup = models.FloatField(blank=True, null=True)
    vaccvaccination = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'outiterationcosts'

class Readallcodes(models.Model):
    code_id = models.IntegerField(unique=True)
    code = models.TextField()
    code_type = models.TextField()
    code_description = models.TextField()
    class Meta:
        managed = False
        db_table = 'readallcodes'

class Readallcodetypes(models.Model):
    code_type_id = models.IntegerField(unique=True)
    code_type = models.TextField()
    code_description = models.TextField()
    class Meta:
        managed = False
        db_table = 'readallcodetypes'

