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
    versionnumber = models.TextField(db_column='VERSIONNUMBER', unique=True)
    versionapplication = models.TextField(db_column='VERSIONAPPLICATION')
    versiondate = models.TextField(db_column='VERSIONDATE')
    versioninfourl = models.TextField(db_column='VERSIONINFOURL', blank=True)
    versionid = models.IntegerField(db_column='VERSIONID', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'DBSCHEMAVERSION'

class Dynablob(models.Model):
    dynblobid = models.TextField(db_column='DYNBLOBID', unique=True)
    zoneperimeters = models.TextField(db_column='ZONEPERIMETERS', blank=True)
    class Meta:
        managed = False
        db_table = 'DYNABLOB'

class Dynaherd(models.Model):
    herdid = models.IntegerField(db_column='HERDID', unique=True)
    productiontypeid = models.IntegerField(db_column='PRODUCTIONTYPEID')
    latitude = models.FloatField(db_column='LATITUDE')
    longitude = models.FloatField(db_column='LONGITUDE')
    initialstatecode = models.TextField(db_column='INITIALSTATECODE')
    daysininitialstate = models.IntegerField(db_column='DAYSININITIALSTATE')
    daysleftininitialstate = models.IntegerField(db_column='DAYSLEFTININITIALSTATE')
    initialsize = models.IntegerField(db_column='INITIALSIZE')
    finalstatecode = models.TextField(db_column='FINALSTATECODE', blank=True)# This field type is a guess.
    finalcontrolstatecode = models.TextField(db_column='FINALCONTROLSTATECODE', blank=True)
    finaldetectionstatecode = models.TextField(db_column='FINALDETECTIONSTATECODE', blank=True)
    cumulinfected = models.IntegerField(db_column='CUMULINFECTED', blank=True, null=True)
    cumuldetected = models.IntegerField(db_column='CUMULDETECTED', blank=True, null=True)
    cumuldestroyed = models.IntegerField(db_column='CUMULDESTROYED', blank=True, null=True)
    cumulvaccinated = models.IntegerField(db_column='CUMULVACCINATED', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'DYNAHERD'

class Inchart(models.Model):
    chartid = models.IntegerField(db_column='CHARTID', unique=True)
    fieldname = models.TextField(db_column='FIELDNAME', blank=True)
    chartname = models.TextField(db_column='CHARTNAME')
    ispdf = models.IntegerField(db_column='ISPDF')
    charttype = models.TextField(db_column='CHARTTYPE', blank=True)
    mean = models.FloatField(db_column='MEAN', blank=True, null=True)
    stddev = models.FloatField(db_column='STDDEV', blank=True, null=True)
    min = models.FloatField(db_column='MIN', blank=True, null=True)
    mode = models.FloatField(db_column='MODE', blank=True, null=True)
    max = models.FloatField(db_column='MAX', blank=True, null=True)
    alpha = models.FloatField(db_column='ALPHA', blank=True, null=True)
    alpha2 = models.FloatField(db_column='ALPHA2', blank=True, null=True)
    beta = models.FloatField(db_column='BETA', blank=True, null=True)
    location = models.FloatField(db_column='LOCATION', blank=True, null=True)
    scale = models.FloatField(db_column='SCALE', blank=True, null=True)
    shape = models.FloatField(db_column='SHAPE', blank=True, null=True)
    n = models.IntegerField(db_column='N', blank=True, null=True)
    p = models.FloatField(db_column='P', blank=True, null=True)
    m = models.IntegerField(db_column='M', blank=True, null=True)
    d = models.IntegerField(db_column='D', blank=True, null=True)
    dmin = models.IntegerField(db_column='DMIN', blank=True, null=True)
    dmax = models.IntegerField(db_column='DMAX', blank=True, null=True)
    theta = models.FloatField(db_column='THETA', blank=True, null=True)
    a = models.FloatField(db_column='A', blank=True, null=True)
    s = models.IntegerField(db_column='S', blank=True, null=True)
    xaxisunits = models.TextField(db_column='XAXISUNITS', blank=True)
    yaxisunits = models.TextField(db_column='YAXISUNITS', blank=True)
    notes = models.TextField(db_column='NOTES', blank=True)
    class Meta:
        managed = False
        db_table = 'INCHART'

class Inchartdetail(models.Model):
    chartid = models.IntegerField(db_column='CHARTID')
    pointorder = models.IntegerField(db_column='POINTORDER')
    x = models.FloatField(db_column='X')
    y = models.FloatField(db_column='Y')
    class Meta:
        managed = False
        db_table = 'INCHARTDETAIL'

class Incontrolsglobal(models.Model):
    controlsglobalid = models.TextField(db_column='CONTROLSGLOBALID')
    includedetection = models.IntegerField(db_column='INCLUDEDETECTION')
    includetracing = models.IntegerField(db_column='INCLUDETRACING')
    includetracingherdexam = models.IntegerField(db_column='INCLUDETRACINGHERDEXAM')
    includetracingtesting = models.IntegerField(db_column='INCLUDETRACINGTESTING')
    includedestruction = models.IntegerField(db_column='INCLUDEDESTRUCTION')
    destrprogramdelay = models.IntegerField(db_column='DESTRPROGRAMDELAY', blank=True, null=True)
    destrcapacityrelid = models.IntegerField(db_column='DESTRCAPACITYRELID', blank=True, null=True)
    destrpriorityorder = models.TextField(db_column='DESTRPRIORITYORDER', blank=True)
    destrreasonorder = models.TextField(db_column='DESTRREASONORDER', blank=True)
    includevaccination = models.IntegerField(db_column='INCLUDEVACCINATION')
    vaccdetectedunitsbeforestart = models.IntegerField(db_column='VACCDETECTEDUNITSBEFORESTART', blank=True, null=True)
    vacccapacityrelid = models.IntegerField(db_column='VACCCAPACITYRELID', blank=True, null=True)
    vaccpriorityorder = models.TextField(db_column='VACCPRIORITYORDER', blank=True)
    includezones = models.IntegerField(db_column='INCLUDEZONES')
    vaccretrospectivedays = models.IntegerField(db_column='VACCRETROSPECTIVEDAYS', blank=True, null=True)
    vacccapacitystartrelid = models.IntegerField(db_column='VACCCAPACITYSTARTRELID', blank=True, null=True)
    vacccapacityrestartrelid = models.IntegerField(db_column='VACCCAPACITYRESTARTRELID', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'INCONTROLSGLOBAL'

class Incustomoutputdefinitions(models.Model):
    defid = models.IntegerField(db_column='DEFID', unique=True)
    outputname = models.TextField(db_column='OUTPUTNAME')
    outputtypecode = models.TextField(db_column='OUTPUTTYPECODE', blank=True)
    outputfrequencycode = models.TextField(db_column='OUTPUTFREQUENCYCODE', blank=True)
    sql = models.TextField(db_column='SQL', blank=True)
    class Meta:
        managed = False
        db_table = 'INCUSTOMOUTPUTDEFINITIONS'

class Indiseasespread(models.Model):
    productiontypepairid = models.IntegerField(db_column='PRODUCTIONTYPEPAIRID', unique=True)
    spreadmethodcode = models.TextField(db_column='SPREADMETHODCODE', blank=True)
    latentcaninfect = models.IntegerField(db_column='LATENTCANINFECT', blank=True, null=True)
    subclinicalcaninfect = models.IntegerField(db_column='SUBCLINICALCANINFECT', blank=True, null=True)
    meancontactrate = models.FloatField(db_column='MEANCONTACTRATE', blank=True, null=True)
    usefixedcontactrate = models.IntegerField(db_column='USEFIXEDCONTACTRATE', blank=True, null=True)
    fixedcontactrate = models.FloatField(db_column='FIXEDCONTACTRATE', blank=True, null=True)
    infectionprobability = models.FloatField(db_column='INFECTIONPROBABILITY', blank=True, null=True)
    distancepdfid = models.IntegerField(db_column='DISTANCEPDFID', blank=True, null=True)
    movementcontrolrelid = models.IntegerField(db_column='MOVEMENTCONTROLRELID', blank=True, null=True)
    transportdelaypdfid = models.IntegerField(db_column='TRANSPORTDELAYPDFID', blank=True, null=True)
    probairbornespread1km = models.FloatField(db_column='PROBAIRBORNESPREAD1KM', blank=True, null=True)
    maxdistairbornespread = models.FloatField(db_column='MAXDISTAIRBORNESPREAD', blank=True, null=True)
    winddirectionstart = models.IntegerField(db_column='WINDDIRECTIONSTART', blank=True, null=True)
    winddirectionend = models.IntegerField(db_column='WINDDIRECTIONEND', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'INDISEASESPREAD'

class Ingeneral(models.Model):
    ingeneralid = models.TextField(db_column='INGENERALID', blank=True)
    language = models.TextField(db_column='LANGUAGE', blank=True)
    scenariodescr = models.TextField(db_column='SCENARIODESCR', blank=True)
    iterations = models.IntegerField(db_column='ITERATIONS', blank=True, null=True)
    days = models.IntegerField(db_column='DAYS', blank=True, null=True)
    simstopreason = models.TextField(db_column='SIMSTOPREASON', blank=True)
    includecontactspread = models.IntegerField(db_column='INCLUDECONTACTSPREAD', blank=True, null=True)
    includeairbornespread = models.IntegerField(db_column='INCLUDEAIRBORNESPREAD', blank=True, null=True)
    useairborneexponentialdecay = models.IntegerField(db_column='USEAIRBORNEEXPONENTIALDECAY', blank=True, null=True)
    usewithinherdprevalence = models.IntegerField(db_column='USEWITHINHERDPREVALENCE', blank=True, null=True)
    costtrackdestruction = models.IntegerField(db_column='COSTTRACKDESTRUCTION', blank=True, null=True)
    costtrackvaccination = models.IntegerField(db_column='COSTTRACKVACCINATION', blank=True, null=True)
    costtrackzonesurveillance = models.IntegerField(db_column='COSTTRACKZONESURVEILLANCE', blank=True, null=True)
    usefixedrandomseed = models.IntegerField(db_column='USEFIXEDRANDOMSEED', blank=True, null=True)
    randomseed = models.IntegerField(db_column='RANDOMSEED', blank=True, null=True)
    savealldailyoutputs = models.IntegerField(db_column='SAVEALLDAILYOUTPUTS', blank=True, null=True)
    savedailyoutputsforiterations = models.IntegerField(db_column='SAVEDAILYOUTPUTSFORITERATIONS', blank=True, null=True)
    writedailystatesfile = models.IntegerField(db_column='WRITEDAILYSTATESFILE', blank=True, null=True)
    dailystatesfilename = models.TextField(db_column='DAILYSTATESFILENAME', blank=True)
    savedailyevents = models.IntegerField(db_column='SAVEDAILYEVENTS', blank=True, null=True)
    savedailyexposures = models.IntegerField(db_column='SAVEDAILYEXPOSURES', blank=True, null=True)
    saveiterationoutputsforherds = models.IntegerField(db_column='SAVEITERATIONOUTPUTSFORHERDS', blank=True, null=True)
    usecustomoutputs = models.IntegerField(db_column='USECUSTOMOUTPUTS', blank=True, null=True)
    writenaadsmapoutput = models.IntegerField(db_column='WRITENAADSMAPOUTPUT', blank=True, null=True)
    naadsmapdirectory = models.TextField(db_column='NAADSMAPDIRECTORY', blank=True)
    class Meta:
        managed = False
        db_table = 'INGENERAL'

class Ingroup(models.Model):
    groupid = models.IntegerField(db_column='GROUPID', unique=True)
    subgroupid = models.IntegerField(db_column='SUBGROUPID')
    groupproductiontypes = models.TextField(db_column='GROUPPRODUCTIONTYPES')
    class Meta:
        managed = False
        db_table = 'INGROUP'

class Inproductiontype(models.Model):
    productiontypeid = models.IntegerField(db_column='PRODUCTIONTYPEID', unique=True)
    prodtypedescr = models.TextField(db_column='PRODTYPEDESCR')
    usediseasetransition = models.IntegerField(db_column='USEDISEASETRANSITION', blank=True, null=True)
    dislatentperiodpdfid = models.IntegerField(db_column='DISLATENTPERIODPDFID', blank=True, null=True)
    dissubclinicalperiodpdfid = models.IntegerField(db_column='DISSUBCLINICALPERIODPDFID', blank=True, null=True)
    disclinicalperiodpdfid = models.IntegerField(db_column='DISCLINICALPERIODPDFID', blank=True, null=True)
    disimmuneperiodpdfid = models.IntegerField(db_column='DISIMMUNEPERIODPDFID', blank=True, null=True)
    disprevalencerelid = models.IntegerField(db_column='DISPREVALENCERELID', blank=True, null=True)
    usedetection = models.IntegerField(db_column='USEDETECTION', blank=True, null=True)
    detprobobsvstimeclinicalrelid = models.IntegerField(db_column='DETPROBOBSVSTIMECLINICALRELID', blank=True, null=True)
    detprobreportvsfirstdetectionrelid = models.IntegerField(db_column='DETPROBREPORTVSFIRSTDETECTIONRELID', blank=True, null=True)
    tracedirectforward = models.IntegerField(db_column='TRACEDIRECTFORWARD', blank=True, null=True)
    tracedirectback = models.IntegerField(db_column='TRACEDIRECTBACK', blank=True, null=True)
    tracedirectsuccess = models.FloatField(db_column='TRACEDIRECTSUCCESS', blank=True, null=True)
    tracedirecttraceperiod = models.IntegerField(db_column='TRACEDIRECTTRACEPERIOD', blank=True, null=True)
    traceindirectforward = models.IntegerField(db_column='TRACEINDIRECTFORWARD', blank=True, null=True)
    traceindirectback = models.IntegerField(db_column='TRACEINDIRECTBACK', blank=True, null=True)
    traceindirectsuccess = models.FloatField(db_column='TRACEINDIRECTSUCCESS', blank=True, null=True)
    traceindirecttraceperiod = models.IntegerField(db_column='TRACEINDIRECTTRACEPERIOD', blank=True, null=True)
    tracedelaypdfid = models.IntegerField(db_column='TRACEDELAYPDFID', blank=True, null=True)
    usebasicdestruction = models.IntegerField(db_column='USEBASICDESTRUCTION', blank=True, null=True)
    destrisringtrigger = models.IntegerField(db_column='DESTRISRINGTRIGGER', blank=True, null=True)
    destrringradius = models.FloatField(db_column='DESTRRINGRADIUS', blank=True, null=True)
    destrisringtarget = models.IntegerField(db_column='DESTRISRINGTARGET', blank=True, null=True)
    destrdirectforwardtraces = models.IntegerField(db_column='DESTRDIRECTFORWARDTRACES', blank=True, null=True)
    destrindirectforwardtraces = models.IntegerField(db_column='DESTRINDIRECTFORWARDTRACES', blank=True, null=True)
    destrdirectbacktraces = models.IntegerField(db_column='DESTRDIRECTBACKTRACES', blank=True, null=True)
    destrindirectbacktraces = models.IntegerField(db_column='DESTRINDIRECTBACKTRACES', blank=True, null=True)
    destrpriority = models.IntegerField(db_column='DESTRPRIORITY', blank=True, null=True)
    usevaccination = models.IntegerField(db_column='USEVACCINATION', blank=True, null=True)
    vaccmintimebetweenvaccinations = models.IntegerField(db_column='VACCMINTIMEBETWEENVACCINATIONS', blank=True, null=True)
    vaccvaccinatedetected = models.IntegerField(db_column='VACCVACCINATEDETECTED', blank=True, null=True)
    vaccdaystoimmunity = models.IntegerField(db_column='VACCDAYSTOIMMUNITY', blank=True, null=True)
    vaccimmuneperiodpdfid = models.IntegerField(db_column='VACCIMMUNEPERIODPDFID', blank=True, null=True)
    vaccring = models.IntegerField(db_column='VACCRING', blank=True, null=True)
    vaccringradius = models.FloatField(db_column='VACCRINGRADIUS', blank=True, null=True)
    vaccpriority = models.IntegerField(db_column='VACCPRIORITY', blank=True, null=True)
    costdestrappraisalperunit = models.FloatField(db_column='COSTDESTRAPPRAISALPERUNIT', blank=True, null=True)
    costdestrcleaningperunit = models.FloatField(db_column='COSTDESTRCLEANINGPERUNIT', blank=True, null=True)
    costdestreuthanasiaperanimal = models.FloatField(db_column='COSTDESTREUTHANASIAPERANIMAL', blank=True, null=True)
    costdestrindemnificationperanimal = models.FloatField(db_column='COSTDESTRINDEMNIFICATIONPERANIMAL', blank=True, null=True)
    costdestrdisposalperanimal = models.FloatField(db_column='COSTDESTRDISPOSALPERANIMAL', blank=True, null=True)
    costvaccsetupperunit = models.FloatField(db_column='COSTVACCSETUPPERUNIT', blank=True, null=True)
    costvaccthreshold = models.IntegerField(db_column='COSTVACCTHRESHOLD', blank=True, null=True)
    costvaccbaselineperanimal = models.FloatField(db_column='COSTVACCBASELINEPERANIMAL', blank=True, null=True)
    costvaccadditionalperanimal = models.FloatField(db_column='COSTVACCADDITIONALPERANIMAL', blank=True, null=True)
    zonedetectionistrigger = models.IntegerField(db_column='ZONEDETECTIONISTRIGGER', blank=True, null=True)
    zonedirecttraceistrigger = models.IntegerField(db_column='ZONEDIRECTTRACEISTRIGGER', blank=True, null=True)
    zoneindirecttraceistrigger = models.IntegerField(db_column='ZONEINDIRECTTRACEISTRIGGER', blank=True, null=True)
    examdirectforward = models.IntegerField(db_column='EXAMDIRECTFORWARD', blank=True, null=True)
    examdirectforwardmultiplier = models.FloatField(db_column='EXAMDIRECTFORWARDMULTIPLIER', blank=True, null=True)
    examindirectforward = models.IntegerField(db_column='EXAMINDIRECTFORWARD', blank=True, null=True)
    examindirectforwardmultiplier = models.FloatField(db_column='EXAMINDIRECTFORWARDMULTIPLIER', blank=True, null=True)
    examdirectback = models.IntegerField(db_column='EXAMDIRECTBACK', blank=True, null=True)
    examdirectbackmultiplier = models.FloatField(db_column='EXAMDIRECTBACKMULTIPLIER', blank=True, null=True)
    examindirectback = models.IntegerField(db_column='EXAMINDIRECTBACK', blank=True, null=True)
    examindirectbackmultiplier = models.FloatField(db_column='EXAMINDIRECTBACKMULTIPLIER', blank=True, null=True)
    testdirectforward = models.IntegerField(db_column='TESTDIRECTFORWARD', blank=True, null=True)
    testindirectforward = models.IntegerField(db_column='TESTINDIRECTFORWARD', blank=True, null=True)
    testdirectback = models.IntegerField(db_column='TESTDIRECTBACK', blank=True, null=True)
    testindirectback = models.IntegerField(db_column='TESTINDIRECTBACK', blank=True, null=True)
    testspecificity = models.FloatField(db_column='TESTSPECIFICITY', blank=True, null=True)
    testsensitivity = models.FloatField(db_column='TESTSENSITIVITY', blank=True, null=True)
    testdelaypdfid = models.IntegerField(db_column='TESTDELAYPDFID', blank=True, null=True)
    vaccrestrospectivedays = models.IntegerField(db_column='VACCRESTROSPECTIVEDAYS', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'INPRODUCTIONTYPE'

class Inproductiontypepair(models.Model):
    productiontypepairid = models.TextField(db_column='PRODUCTIONTYPEPAIRID', unique=True)# This field type is a guess.
    sourceproductiontypeid = models.IntegerField(db_column='SOURCEPRODUCTIONTYPEID')
    destproductiontypeid = models.IntegerField(db_column='DESTPRODUCTIONTYPEID')
    usedirectcontact = models.IntegerField(db_column='USEDIRECTCONTACT')
    directcontactspreadid = models.IntegerField(db_column='DIRECTCONTACTSPREADID', blank=True, null=True)
    useindirectcontact = models.IntegerField(db_column='USEINDIRECTCONTACT')
    indirectcontactspreadid = models.IntegerField(db_column='INDIRECTCONTACTSPREADID', blank=True, null=True)
    useairbornespread = models.IntegerField(db_column='USEAIRBORNESPREAD')
    airbornecontactspreadid = models.IntegerField(db_column='AIRBORNECONTACTSPREADID', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'INPRODUCTIONTYPEPAIR'

class Intrigger(models.Model):
    triggerid = models.IntegerField(db_column='TRIGGERID', unique=True)
    triggercode = models.IntegerField(db_column='TRIGGERCODE')
    triggerdays = models.TextField(db_column='TRIGGERDAYS', blank=True)# This field type is a guess.
    class Meta:
        managed = False
        db_table = 'INTRIGGER'

class Inzone(models.Model):
    zoneid = models.IntegerField(db_column='ZONEID', unique=True)
    zonedescription = models.TextField(db_column='ZONEDESCRIPTION')
    zoneradius = models.FloatField(db_column='ZONERADIUS')
    class Meta:
        managed = False
        db_table = 'INZONE'

class Inzoneproductiontypepair(models.Model):
    inzoneproductiontypepairid = models.IntegerField(db_column='INZONEPRODUCTIONTYPEPAIRID', unique=True)
    zoneid = models.IntegerField(db_column='ZONEID')
    productiontypeid = models.IntegerField(db_column='PRODUCTIONTYPEID')
    usedirectmovementcontrol = models.IntegerField(db_column='USEDIRECTMOVEMENTCONTROL')
    zonedirectmovementrelid = models.IntegerField(db_column='ZONEDIRECTMOVEMENTRELID', blank=True, null=True)
    useindirectmovementcontrol = models.IntegerField(db_column='USEINDIRECTMOVEMENTCONTROL')
    zoneindirectmovementrelid = models.IntegerField(db_column='ZONEINDIRECTMOVEMENTRELID', blank=True, null=True)
    usedetectionmultiplier = models.IntegerField(db_column='USEDETECTIONMULTIPLIER')
    zonedetectionmultiplier = models.FloatField(db_column='ZONEDETECTIONMULTIPLIER', blank=True, null=True)
    costsurvperanimalday = models.FloatField(db_column='COSTSURVPERANIMALDAY', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'INZONEPRODUCTIONTYPEPAIR'

class Outdailybyproductiontype(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    productiontypeid = models.IntegerField(db_column='PRODUCTIONTYPEID', blank=True, null=True)
    day = models.IntegerField(db_column='DAY', blank=True, null=True)
    tsdususc = models.IntegerField(db_column='TSDUSUSC', blank=True, null=True)
    tsdasusc = models.IntegerField(db_column='TSDASUSC', blank=True, null=True)
    tsdulat = models.IntegerField(db_column='TSDULAT', blank=True, null=True)
    tsdalat = models.IntegerField(db_column='TSDALAT', blank=True, null=True)
    tsdusubc = models.IntegerField(db_column='TSDUSUBC', blank=True, null=True)
    tsdasubc = models.IntegerField(db_column='TSDASUBC', blank=True, null=True)
    tsduclin = models.IntegerField(db_column='TSDUCLIN', blank=True, null=True)
    tsdaclin = models.IntegerField(db_column='TSDACLIN', blank=True, null=True)
    tsdunimm = models.IntegerField(db_column='TSDUNIMM', blank=True, null=True)
    tsdanimm = models.IntegerField(db_column='TSDANIMM', blank=True, null=True)
    tsduvimm = models.IntegerField(db_column='TSDUVIMM', blank=True, null=True)
    tsdavimm = models.IntegerField(db_column='TSDAVIMM', blank=True, null=True)
    tsdudest = models.IntegerField(db_column='TSDUDEST', blank=True, null=True)
    tsdadest = models.IntegerField(db_column='TSDADEST', blank=True, null=True)
    tscususc = models.IntegerField(db_column='TSCUSUSC', blank=True, null=True)
    tscasusc = models.IntegerField(db_column='TSCASUSC', blank=True, null=True)
    tsculat = models.IntegerField(db_column='TSCULAT', blank=True, null=True)
    tscalat = models.IntegerField(db_column='TSCALAT', blank=True, null=True)
    tscusubc = models.IntegerField(db_column='TSCUSUBC', blank=True, null=True)
    tscasubc = models.IntegerField(db_column='TSCASUBC', blank=True, null=True)
    tscuclin = models.IntegerField(db_column='TSCUCLIN', blank=True, null=True)
    tscaclin = models.IntegerField(db_column='TSCACLIN', blank=True, null=True)
    tscunimm = models.IntegerField(db_column='TSCUNIMM', blank=True, null=True)
    tscanimm = models.IntegerField(db_column='TSCANIMM', blank=True, null=True)
    tscuvimm = models.IntegerField(db_column='TSCUVIMM', blank=True, null=True)
    tscavimm = models.IntegerField(db_column='TSCAVIMM', blank=True, null=True)
    tscudest = models.IntegerField(db_column='TSCUDEST', blank=True, null=True)
    tscadest = models.IntegerField(db_column='TSCADEST', blank=True, null=True)
    infnuair = models.IntegerField(db_column='INFNUAIR', blank=True, null=True)
    infnaair = models.IntegerField(db_column='INFNAAIR', blank=True, null=True)
    infnudir = models.IntegerField(db_column='INFNUDIR', blank=True, null=True)
    infnadir = models.IntegerField(db_column='INFNADIR', blank=True, null=True)
    infnuind = models.IntegerField(db_column='INFNUIND', blank=True, null=True)
    infnaind = models.IntegerField(db_column='INFNAIND', blank=True, null=True)
    infcuini = models.IntegerField(db_column='INFCUINI', blank=True, null=True)
    infcaini = models.IntegerField(db_column='INFCAINI', blank=True, null=True)
    infcuair = models.IntegerField(db_column='INFCUAIR', blank=True, null=True)
    infcaair = models.IntegerField(db_column='INFCAAIR', blank=True, null=True)
    infcudir = models.IntegerField(db_column='INFCUDIR', blank=True, null=True)
    infcadir = models.IntegerField(db_column='INFCADIR', blank=True, null=True)
    infcuind = models.IntegerField(db_column='INFCUIND', blank=True, null=True)
    infcaind = models.IntegerField(db_column='INFCAIND', blank=True, null=True)
    expcudir = models.IntegerField(db_column='EXPCUDIR', blank=True, null=True)
    expcadir = models.IntegerField(db_column='EXPCADIR', blank=True, null=True)
    expcuind = models.IntegerField(db_column='EXPCUIND', blank=True, null=True)
    expcaind = models.IntegerField(db_column='EXPCAIND', blank=True, null=True)
    trcudirfwd = models.IntegerField(db_column='TRCUDIRFWD', blank=True, null=True)
    trcadirfwd = models.IntegerField(db_column='TRCADIRFWD', blank=True, null=True)
    trcuindfwd = models.IntegerField(db_column='TRCUINDFWD', blank=True, null=True)
    trcaindfwd = models.IntegerField(db_column='TRCAINDFWD', blank=True, null=True)
    trcudirpfwd = models.IntegerField(db_column='TRCUDIRPFWD', blank=True, null=True)
    trcadirpfwd = models.IntegerField(db_column='TRCADIRPFWD', blank=True, null=True)
    trcuindpfwd = models.IntegerField(db_column='TRCUINDPFWD', blank=True, null=True)
    trcaindpfwd = models.IntegerField(db_column='TRCAINDPFWD', blank=True, null=True)
    tocudirfwd = models.IntegerField(db_column='TOCUDIRFWD', blank=True, null=True)
    tocuindfwd = models.IntegerField(db_column='TOCUINDFWD', blank=True, null=True)
    tocudirback = models.IntegerField(db_column='TOCUDIRBACK', blank=True, null=True)
    tocuindback = models.IntegerField(db_column='TOCUINDBACK', blank=True, null=True)
    trnudirfwd = models.IntegerField(db_column='TRNUDIRFWD', blank=True, null=True)
    trnadirfwd = models.IntegerField(db_column='TRNADIRFWD', blank=True, null=True)
    trnuindfwd = models.IntegerField(db_column='TRNUINDFWD', blank=True, null=True)
    trnaindfwd = models.IntegerField(db_column='TRNAINDFWD', blank=True, null=True)
    trcudirback = models.IntegerField(db_column='TRCUDIRBACK', blank=True, null=True)
    trcadirback = models.IntegerField(db_column='TRCADIRBACK', blank=True, null=True)
    trcuindback = models.IntegerField(db_column='TRCUINDBACK', blank=True, null=True)
    trcaindback = models.IntegerField(db_column='TRCAINDBACK', blank=True, null=True)
    trcudirpback = models.IntegerField(db_column='TRCUDIRPBACK', blank=True, null=True)
    trcadirpback = models.IntegerField(db_column='TRCADIRPBACK', blank=True, null=True)
    trcuindpback = models.IntegerField(db_column='TRCUINDPBACK', blank=True, null=True)
    trcaindpback = models.IntegerField(db_column='TRCAINDPBACK', blank=True, null=True)
    trnudirback = models.IntegerField(db_column='TRNUDIRBACK', blank=True, null=True)
    trnadirback = models.IntegerField(db_column='TRNADIRBACK', blank=True, null=True)
    trnuindback = models.IntegerField(db_column='TRNUINDBACK', blank=True, null=True)
    trnaindback = models.IntegerField(db_column='TRNAINDBACK', blank=True, null=True)
    tonudirfwd = models.IntegerField(db_column='TONUDIRFWD', blank=True, null=True)
    tonuindfwd = models.IntegerField(db_column='TONUINDFWD', blank=True, null=True)
    tonudirback = models.IntegerField(db_column='TONUDIRBACK', blank=True, null=True)
    tonuindback = models.IntegerField(db_column='TONUINDBACK', blank=True, null=True)
    exmcudirfwd = models.IntegerField(db_column='EXMCUDIRFWD', blank=True, null=True)
    exmcadirfwd = models.IntegerField(db_column='EXMCADIRFWD', blank=True, null=True)
    exmcuindfwd = models.IntegerField(db_column='EXMCUINDFWD', blank=True, null=True)
    exmcaindfwd = models.IntegerField(db_column='EXMCAINDFWD', blank=True, null=True)
    exmcudirback = models.IntegerField(db_column='EXMCUDIRBACK', blank=True, null=True)
    exmcadirback = models.IntegerField(db_column='EXMCADIRBACK', blank=True, null=True)
    exmcuindback = models.IntegerField(db_column='EXMCUINDBACK', blank=True, null=True)
    exmcaindback = models.IntegerField(db_column='EXMCAINDBACK', blank=True, null=True)
    exmnuall = models.IntegerField(db_column='EXMNUALL', blank=True, null=True)
    exmnaall = models.IntegerField(db_column='EXMNAALL', blank=True, null=True)
    tstcudirfwd = models.IntegerField(db_column='TSTCUDIRFWD', blank=True, null=True)
    tstcadirfwd = models.IntegerField(db_column='TSTCADIRFWD', blank=True, null=True)
    tstcuindfwd = models.IntegerField(db_column='TSTCUINDFWD', blank=True, null=True)
    tstcaindfwd = models.IntegerField(db_column='TSTCAINDFWD', blank=True, null=True)
    tstcudirback = models.IntegerField(db_column='TSTCUDIRBACK', blank=True, null=True)
    tstcadirback = models.IntegerField(db_column='TSTCADIRBACK', blank=True, null=True)
    tstcuindback = models.IntegerField(db_column='TSTCUINDBACK', blank=True, null=True)
    tstcaindback = models.IntegerField(db_column='TSTCAINDBACK', blank=True, null=True)
    tstcutruepos = models.IntegerField(db_column='TSTCUTRUEPOS', blank=True, null=True)
    tstcatruepos = models.IntegerField(db_column='TSTCATRUEPOS', blank=True, null=True)
    tstnutruepos = models.IntegerField(db_column='TSTNUTRUEPOS', blank=True, null=True)
    tstnatruepos = models.IntegerField(db_column='TSTNATRUEPOS', blank=True, null=True)
    tstcutrueneg = models.IntegerField(db_column='TSTCUTRUENEG', blank=True, null=True)
    tstcatrueneg = models.IntegerField(db_column='TSTCATRUENEG', blank=True, null=True)
    tstnutrueneg = models.IntegerField(db_column='TSTNUTRUENEG', blank=True, null=True)
    tstnatrueneg = models.IntegerField(db_column='TSTNATRUENEG', blank=True, null=True)
    tstcufalsepos = models.IntegerField(db_column='TSTCUFALSEPOS', blank=True, null=True)
    tstcafalsepos = models.IntegerField(db_column='TSTCAFALSEPOS', blank=True, null=True)
    tstnufalsepos = models.IntegerField(db_column='TSTNUFALSEPOS', blank=True, null=True)
    tstnafalsepos = models.IntegerField(db_column='TSTNAFALSEPOS', blank=True, null=True)
    tstcufalseneg = models.IntegerField(db_column='TSTCUFALSENEG', blank=True, null=True)
    tstcafalseneg = models.IntegerField(db_column='TSTCAFALSENEG', blank=True, null=True)
    tstnufalseneg = models.IntegerField(db_column='TSTNUFALSENEG', blank=True, null=True)
    tstnafalseneg = models.IntegerField(db_column='TSTNAFALSENEG', blank=True, null=True)
    detnuclin = models.IntegerField(db_column='DETNUCLIN', blank=True, null=True)
    detnaclin = models.IntegerField(db_column='DETNACLIN', blank=True, null=True)
    detcuclin = models.IntegerField(db_column='DETCUCLIN', blank=True, null=True)
    detcaclin = models.IntegerField(db_column='DETCACLIN', blank=True, null=True)
    detnutest = models.IntegerField(db_column='DETNUTEST', blank=True, null=True)
    detnatest = models.IntegerField(db_column='DETNATEST', blank=True, null=True)
    detcutest = models.IntegerField(db_column='DETCUTEST', blank=True, null=True)
    detcatest = models.IntegerField(db_column='DETCATEST', blank=True, null=True)
    descuini = models.IntegerField(db_column='DESCUINI', blank=True, null=True)
    descaini = models.IntegerField(db_column='DESCAINI', blank=True, null=True)
    descudet = models.IntegerField(db_column='DESCUDET', blank=True, null=True)
    descadet = models.IntegerField(db_column='DESCADET', blank=True, null=True)
    descudirfwd = models.IntegerField(db_column='DESCUDIRFWD', blank=True, null=True)
    descadirfwd = models.IntegerField(db_column='DESCADIRFWD', blank=True, null=True)
    descuindfwd = models.IntegerField(db_column='DESCUINDFWD', blank=True, null=True)
    descaindfwd = models.IntegerField(db_column='DESCAINDFWD', blank=True, null=True)
    descudirback = models.IntegerField(db_column='DESCUDIRBACK', blank=True, null=True)
    descadirback = models.IntegerField(db_column='DESCADIRBACK', blank=True, null=True)
    descuindback = models.IntegerField(db_column='DESCUINDBACK', blank=True, null=True)
    descaindback = models.IntegerField(db_column='DESCAINDBACK', blank=True, null=True)
    descuring = models.IntegerField(db_column='DESCURING', blank=True, null=True)
    descaring = models.IntegerField(db_column='DESCARING', blank=True, null=True)
    desnuall = models.IntegerField(db_column='DESNUALL', blank=True, null=True)
    desnaall = models.IntegerField(db_column='DESNAALL', blank=True, null=True)
    deswuall = models.IntegerField(db_column='DESWUALL', blank=True, null=True)
    deswaall = models.IntegerField(db_column='DESWAALL', blank=True, null=True)
    vaccuini = models.IntegerField(db_column='VACCUINI', blank=True, null=True)
    vaccaini = models.IntegerField(db_column='VACCAINI', blank=True, null=True)
    vaccuring = models.IntegerField(db_column='VACCURING', blank=True, null=True)
    vaccaring = models.IntegerField(db_column='VACCARING', blank=True, null=True)
    vacnuall = models.IntegerField(db_column='VACNUALL', blank=True, null=True)
    vacnaall = models.IntegerField(db_column='VACNAALL', blank=True, null=True)
    vacwuall = models.IntegerField(db_column='VACWUALL', blank=True, null=True)
    vacwaall = models.IntegerField(db_column='VACWAALL', blank=True, null=True)
    zonnfoci = models.IntegerField(db_column='ZONNFOCI', blank=True, null=True)
    zoncfoci = models.IntegerField(db_column='ZONCFOCI', blank=True, null=True)
    appduinfectious = models.IntegerField(db_column='APPDUINFECTIOUS', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTDAILYBYPRODUCTIONTYPE'

class Outdailybyzone(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    day = models.IntegerField(db_column='DAY', blank=True, null=True)
    zoneid = models.IntegerField(db_column='ZONEID', blank=True, null=True)
    zonearea = models.FloatField(db_column='ZONEAREA', blank=True, null=True)
    zoneperimeter = models.FloatField(db_column='ZONEPERIMETER', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTDAILYBYZONE'

class Outdailybyzoneandproductiontype(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    day = models.IntegerField(db_column='DAY', blank=True, null=True)
    zoneid = models.IntegerField(db_column='ZONEID', blank=True, null=True)
    productiontypeid = models.IntegerField(db_column='PRODUCTIONTYPEID', blank=True, null=True)
    unitdaysinzone = models.IntegerField(db_column='UNITDAYSINZONE', blank=True, null=True)
    animaldaysinzone = models.IntegerField(db_column='ANIMALDAYSINZONE', blank=True, null=True)
    unitsinzone = models.IntegerField(db_column='UNITSINZONE', blank=True, null=True)
    animalsinzone = models.IntegerField(db_column='ANIMALSINZONE', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTDAILYBYZONEANDPRODUCTIONTYPE'

class Outdailyevents(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    day = models.IntegerField(db_column='DAY', blank=True, null=True)
    event = models.IntegerField(db_column='EVENT', blank=True, null=True)
    herdid = models.IntegerField(db_column='HERDID', blank=True, null=True)
    zoneid = models.IntegerField(db_column='ZONEID', blank=True, null=True)
    eventcode = models.TextField(db_column='EVENTCODE', blank=True)
    newstatecode = models.TextField(db_column='NEWSTATECODE', blank=True)
    testresultcode = models.TextField(db_column='TESTRESULTCODE', blank=True)
    class Meta:
        managed = False
        db_table = 'OUTDAILYEVENTS'

class Outdailyexposures(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    day = models.IntegerField(db_column='DAY', blank=True, null=True)
    exposure = models.IntegerField(db_column='EXPOSURE', blank=True, null=True)
    initiatedday = models.IntegerField(db_column='INITIATEDDAY', blank=True, null=True)
    exposedherdid = models.IntegerField(db_column='EXPOSEDHERDID', blank=True, null=True)
    exposedzoneid = models.IntegerField(db_column='EXPOSEDZONEID', blank=True, null=True)
    exposingherdid = models.IntegerField(db_column='EXPOSINGHERDID', blank=True, null=True)
    exposingzoneid = models.IntegerField(db_column='EXPOSINGZONEID', blank=True, null=True)
    spreadmethodcode = models.TextField(db_column='SPREADMETHODCODE', blank=True)
    isadequate = models.IntegerField(db_column='ISADEQUATE', blank=True, null=True)
    exposingherdstatuscode = models.TextField(db_column='EXPOSINGHERDSTATUSCODE', blank=True)
    exposedherdstatuscode = models.TextField(db_column='EXPOSEDHERDSTATUSCODE', blank=True)
    class Meta:
        managed = False
        db_table = 'OUTDAILYEXPOSURES'

class Outepidemiccurves(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    day = models.IntegerField(db_column='DAY', blank=True, null=True)
    productiontypeid = models.IntegerField(db_column='PRODUCTIONTYPEID', blank=True, null=True)
    infectedunits = models.IntegerField(db_column='INFECTEDUNITS', blank=True, null=True)
    infectedanimals = models.IntegerField(db_column='INFECTEDANIMALS', blank=True, null=True)
    detectedunits = models.IntegerField(db_column='DETECTEDUNITS', blank=True, null=True)
    detectedanimals = models.IntegerField(db_column='DETECTEDANIMALS', blank=True, null=True)
    infectiousunits = models.IntegerField(db_column='INFECTIOUSUNITS', blank=True, null=True)
    apparentinfectiousunits = models.IntegerField(db_column='APPARENTINFECTIOUSUNITS', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTEPIDEMICCURVES'

class Outgeneral(models.Model):
    outgeneralid = models.TextField(db_column='OUTGENERALID', blank=True)
    simulationstarttime = models.TextField(db_column='SIMULATIONSTARTTIME', blank=True)
    simulationendtime = models.TextField(db_column='SIMULATIONENDTIME', blank=True)
    completediterations = models.IntegerField(db_column='COMPLETEDITERATIONS', blank=True, null=True)
    version = models.TextField(db_column='VERSION', blank=True)
    class Meta:
        managed = False
        db_table = 'OUTGENERAL'

class Outiteration(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    diseaseended = models.IntegerField(db_column='DISEASEENDED', blank=True, null=True)
    diseaseendday = models.IntegerField(db_column='DISEASEENDDAY', blank=True, null=True)
    outbreakended = models.IntegerField(db_column='OUTBREAKENDED', blank=True, null=True)
    outbreakendday = models.IntegerField(db_column='OUTBREAKENDDAY', blank=True, null=True)
    zonefocicreated = models.IntegerField(db_column='ZONEFOCICREATED', blank=True, null=True)
    deswumax = models.IntegerField(db_column='DESWUMAX', blank=True, null=True)
    deswumaxday = models.IntegerField(db_column='DESWUMAXDAY', blank=True, null=True)
    deswamax = models.FloatField(db_column='DESWAMAX', blank=True, null=True)
    deswamaxday = models.IntegerField(db_column='DESWAMAXDAY', blank=True, null=True)
    deswutimemax = models.IntegerField(db_column='DESWUTIMEMAX', blank=True, null=True)
    deswutimeavg = models.FloatField(db_column='DESWUTIMEAVG', blank=True, null=True)
    vacwumax = models.IntegerField(db_column='VACWUMAX', blank=True, null=True)
    vacwumaxday = models.IntegerField(db_column='VACWUMAXDAY', blank=True, null=True)
    vacwamax = models.FloatField(db_column='VACWAMAX', blank=True, null=True)
    vacwamaxday = models.IntegerField(db_column='VACWAMAXDAY', blank=True, null=True)
    vacwutimemax = models.IntegerField(db_column='VACWUTIMEMAX', blank=True, null=True)
    vacwutimeavg = models.FloatField(db_column='VACWUTIMEAVG', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTITERATION'

class Outiterationbyherd(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    herdid = models.IntegerField(db_column='HERDID', blank=True, null=True)
    laststatuscode = models.TextField(db_column='LASTSTATUSCODE', blank=True)
    laststatusday = models.IntegerField(db_column='LASTSTATUSDAY', blank=True, null=True)
    lastcontrolstatecode = models.TextField(db_column='LASTCONTROLSTATECODE', blank=True)
    lastcontrolstateday = models.IntegerField(db_column='LASTCONTROLSTATEDAY', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTITERATIONBYHERD'

class Outiterationbyproductiontype(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    productiontypeid = models.IntegerField(db_column='PRODUCTIONTYPEID', blank=True, null=True)
    tscususc = models.IntegerField(db_column='TSCUSUSC', blank=True, null=True)
    tscasusc = models.IntegerField(db_column='TSCASUSC', blank=True, null=True)
    tsculat = models.IntegerField(db_column='TSCULAT', blank=True, null=True)
    tscalat = models.IntegerField(db_column='TSCALAT', blank=True, null=True)
    tscusubc = models.IntegerField(db_column='TSCUSUBC', blank=True, null=True)
    tscasubc = models.IntegerField(db_column='TSCASUBC', blank=True, null=True)
    tscuclin = models.IntegerField(db_column='TSCUCLIN', blank=True, null=True)
    tscaclin = models.IntegerField(db_column='TSCACLIN', blank=True, null=True)
    tscunimm = models.IntegerField(db_column='TSCUNIMM', blank=True, null=True)
    tscanimm = models.IntegerField(db_column='TSCANIMM', blank=True, null=True)
    tscuvimm = models.IntegerField(db_column='TSCUVIMM', blank=True, null=True)
    tscavimm = models.IntegerField(db_column='TSCAVIMM', blank=True, null=True)
    tscudest = models.IntegerField(db_column='TSCUDEST', blank=True, null=True)
    tscadest = models.IntegerField(db_column='TSCADEST', blank=True, null=True)
    infcuini = models.IntegerField(db_column='INFCUINI', blank=True, null=True)
    infcaini = models.IntegerField(db_column='INFCAINI', blank=True, null=True)
    infcuair = models.IntegerField(db_column='INFCUAIR', blank=True, null=True)
    infcaair = models.IntegerField(db_column='INFCAAIR', blank=True, null=True)
    infcudir = models.IntegerField(db_column='INFCUDIR', blank=True, null=True)
    infcadir = models.IntegerField(db_column='INFCADIR', blank=True, null=True)
    infcuind = models.IntegerField(db_column='INFCUIND', blank=True, null=True)
    infcaind = models.IntegerField(db_column='INFCAIND', blank=True, null=True)
    expcudir = models.IntegerField(db_column='EXPCUDIR', blank=True, null=True)
    expcadir = models.IntegerField(db_column='EXPCADIR', blank=True, null=True)
    expcuind = models.IntegerField(db_column='EXPCUIND', blank=True, null=True)
    expcaind = models.IntegerField(db_column='EXPCAIND', blank=True, null=True)
    trcudirfwd = models.IntegerField(db_column='TRCUDIRFWD', blank=True, null=True)
    trcadirfwd = models.IntegerField(db_column='TRCADIRFWD', blank=True, null=True)
    trcuindfwd = models.IntegerField(db_column='TRCUINDFWD', blank=True, null=True)
    trcaindfwd = models.IntegerField(db_column='TRCAINDFWD', blank=True, null=True)
    trcudirpfwd = models.IntegerField(db_column='TRCUDIRPFWD', blank=True, null=True)
    trcadirpfwd = models.IntegerField(db_column='TRCADIRPFWD', blank=True, null=True)
    trcuindpfwd = models.IntegerField(db_column='TRCUINDPFWD', blank=True, null=True)
    trcaindpfwd = models.IntegerField(db_column='TRCAINDPFWD', blank=True, null=True)
    trcudirback = models.IntegerField(db_column='TRCUDIRBACK', blank=True, null=True)
    trcadirback = models.IntegerField(db_column='TRCADIRBACK', blank=True, null=True)
    trcuindback = models.IntegerField(db_column='TRCUINDBACK', blank=True, null=True)
    trcaindback = models.IntegerField(db_column='TRCAINDBACK', blank=True, null=True)
    trcudirpback = models.IntegerField(db_column='TRCUDIRPBACK', blank=True, null=True)
    trcadirpback = models.IntegerField(db_column='TRCADIRPBACK', blank=True, null=True)
    trcuindpback = models.IntegerField(db_column='TRCUINDPBACK', blank=True, null=True)
    trcaindpback = models.IntegerField(db_column='TRCAINDPBACK', blank=True, null=True)
    tocudirfwd = models.IntegerField(db_column='TOCUDIRFWD', blank=True, null=True)
    tocuindfwd = models.IntegerField(db_column='TOCUINDFWD', blank=True, null=True)
    tocudirback = models.IntegerField(db_column='TOCUDIRBACK', blank=True, null=True)
    tocuindback = models.IntegerField(db_column='TOCUINDBACK', blank=True, null=True)
    exmcudirfwd = models.IntegerField(db_column='EXMCUDIRFWD', blank=True, null=True)
    exmcadirfwd = models.IntegerField(db_column='EXMCADIRFWD', blank=True, null=True)
    exmcuindfwd = models.IntegerField(db_column='EXMCUINDFWD', blank=True, null=True)
    exmcaindfwd = models.IntegerField(db_column='EXMCAINDFWD', blank=True, null=True)
    exmcudirback = models.IntegerField(db_column='EXMCUDIRBACK', blank=True, null=True)
    exmcadirback = models.IntegerField(db_column='EXMCADIRBACK', blank=True, null=True)
    exmcuindback = models.IntegerField(db_column='EXMCUINDBACK', blank=True, null=True)
    exmcaindback = models.IntegerField(db_column='EXMCAINDBACK', blank=True, null=True)
    tstcudirfwd = models.IntegerField(db_column='TSTCUDIRFWD', blank=True, null=True)
    tstcadirfwd = models.IntegerField(db_column='TSTCADIRFWD', blank=True, null=True)
    tstcuindfwd = models.IntegerField(db_column='TSTCUINDFWD', blank=True, null=True)
    tstcaindfwd = models.IntegerField(db_column='TSTCAINDFWD', blank=True, null=True)
    tstcudirback = models.IntegerField(db_column='TSTCUDIRBACK', blank=True, null=True)
    tstcadirback = models.IntegerField(db_column='TSTCADIRBACK', blank=True, null=True)
    tstcuindback = models.IntegerField(db_column='TSTCUINDBACK', blank=True, null=True)
    tstcaindback = models.IntegerField(db_column='TSTCAINDBACK', blank=True, null=True)
    tstcutruepos = models.IntegerField(db_column='TSTCUTRUEPOS', blank=True, null=True)
    tstcatruepos = models.IntegerField(db_column='TSTCATRUEPOS', blank=True, null=True)
    tstcutrueneg = models.IntegerField(db_column='TSTCUTRUENEG', blank=True, null=True)
    tstcatrueneg = models.IntegerField(db_column='TSTCATRUENEG', blank=True, null=True)
    tstcufalsepos = models.IntegerField(db_column='TSTCUFALSEPOS', blank=True, null=True)
    tstcafalsepos = models.IntegerField(db_column='TSTCAFALSEPOS', blank=True, null=True)
    tstcufalseneg = models.IntegerField(db_column='TSTCUFALSENEG', blank=True, null=True)
    tstcafalseneg = models.IntegerField(db_column='TSTCAFALSENEG', blank=True, null=True)
    detcuclin = models.IntegerField(db_column='DETCUCLIN', blank=True, null=True)
    detcaclin = models.IntegerField(db_column='DETCACLIN', blank=True, null=True)
    detcutest = models.IntegerField(db_column='DETCUTEST', blank=True, null=True)
    detcatest = models.IntegerField(db_column='DETCATEST', blank=True, null=True)
    descuini = models.IntegerField(db_column='DESCUINI', blank=True, null=True)
    descaini = models.IntegerField(db_column='DESCAINI', blank=True, null=True)
    descudet = models.IntegerField(db_column='DESCUDET', blank=True, null=True)
    descadet = models.IntegerField(db_column='DESCADET', blank=True, null=True)
    descudirfwd = models.IntegerField(db_column='DESCUDIRFWD', blank=True, null=True)
    descadirfwd = models.IntegerField(db_column='DESCADIRFWD', blank=True, null=True)
    descuindfwd = models.IntegerField(db_column='DESCUINDFWD', blank=True, null=True)
    descaindfwd = models.IntegerField(db_column='DESCAINDFWD', blank=True, null=True)
    descudirback = models.IntegerField(db_column='DESCUDIRBACK', blank=True, null=True)
    descadirback = models.IntegerField(db_column='DESCADIRBACK', blank=True, null=True)
    descuindback = models.IntegerField(db_column='DESCUINDBACK', blank=True, null=True)
    descaindback = models.IntegerField(db_column='DESCAINDBACK', blank=True, null=True)
    descuring = models.IntegerField(db_column='DESCURING', blank=True, null=True)
    descaring = models.IntegerField(db_column='DESCARING', blank=True, null=True)
    deswumax = models.IntegerField(db_column='DESWUMAX', blank=True, null=True)
    deswamax = models.TextField(db_column='DESWAMAX', blank=True)# This field type is a guess.
    deswamaxday = models.IntegerField(db_column='DESWAMAXDAY', blank=True, null=True)
    deswutimemax = models.IntegerField(db_column='DESWUTIMEMAX', blank=True, null=True)
    deswutimeavg = models.TextField(db_column='DESWUTIMEAVG', blank=True)# This field type is a guess.
    vaccaini = models.IntegerField(db_column='VACCAINI', blank=True, null=True)
    vaccuring = models.IntegerField(db_column='VACCURING', blank=True, null=True)
    vaccaring = models.IntegerField(db_column='VACCARING', blank=True, null=True)
    vacwumax = models.IntegerField(db_column='VACWUMAX', blank=True, null=True)
    vacwamax = models.TextField(db_column='VACWAMAX', blank=True)# This field type is a guess.
    vacwamaxday = models.IntegerField(db_column='VACWAMAXDAY', blank=True, null=True)
    vacwutimemax = models.TextField(db_column='VACWUTIMEMAX', blank=True)# This field type is a guess.
    zoncfoci = models.IntegerField(db_column='ZONCFOCI', blank=True, null=True)
    firstdetection = models.IntegerField(db_column='FIRSTDETECTION', blank=True, null=True)
    firstdetuinf = models.IntegerField(db_column='FIRSTDETUINF', blank=True, null=True)
    firstdetainf = models.IntegerField(db_column='FIRSTDETAINF', blank=True, null=True)
    firstdestruction = models.IntegerField(db_column='FIRSTDESTRUCTION', blank=True, null=True)
    firstvaccination = models.IntegerField(db_column='FIRSTVACCINATION', blank=True, null=True)
    lastdetection = models.IntegerField(db_column='LASTDETECTION', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTITERATIONBYPRODUCTIONTYPE'

class Outiterationbyzone(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    zoneid = models.IntegerField(db_column='ZONEID', blank=True, null=True)
    maxzonearea = models.FloatField(db_column='MAXZONEAREA', blank=True, null=True)
    maxzoneareaday = models.IntegerField(db_column='MAXZONEAREADAY', blank=True, null=True)
    finalzonearea = models.FloatField(db_column='FINALZONEAREA', blank=True, null=True)
    maxzoneperimeter = models.FloatField(db_column='MAXZONEPERIMETER', blank=True, null=True)
    maxzoneperimeterday = models.IntegerField(db_column='MAXZONEPERIMETERDAY', blank=True, null=True)
    finalzoneperimeter = models.FloatField(db_column='FINALZONEPERIMETER', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTITERATIONBYZONE'

class Outiterationbyzoneandproductiontype(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    zoneid = models.IntegerField(db_column='ZONEID', blank=True, null=True)
    productiontypeid = models.IntegerField(db_column='PRODUCTIONTYPEID', blank=True, null=True)
    unitdaysinzone = models.IntegerField(db_column='UNITDAYSINZONE', blank=True, null=True)
    animaldaysinzone = models.IntegerField(db_column='ANIMALDAYSINZONE', blank=True, null=True)
    costsurveillance = models.FloatField(db_column='COSTSURVEILLANCE', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTITERATIONBYZONEANDPRODUCTIONTYPE'

class Outiterationcosts(models.Model):
    iteration = models.IntegerField(db_column='ITERATION', blank=True, null=True)
    productiontypeid = models.IntegerField(db_column='PRODUCTIONTYPEID', blank=True, null=True)
    destrappraisal = models.FloatField(db_column='DESTRAPPRAISAL', blank=True, null=True)
    destrcleaning = models.FloatField(db_column='DESTRCLEANING', blank=True, null=True)
    destreuthanasia = models.FloatField(db_column='DESTREUTHANASIA', blank=True, null=True)
    destrindemnification = models.FloatField(db_column='DESTRINDEMNIFICATION', blank=True, null=True)
    destrdisposal = models.FloatField(db_column='DESTRDISPOSAL', blank=True, null=True)
    vaccsetup = models.FloatField(db_column='VACCSETUP', blank=True, null=True)
    vaccvaccination = models.FloatField(db_column='VACCVACCINATION', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'OUTITERATIONCOSTS'

class Readallcodes(models.Model):
    codeid = models.IntegerField(db_column='CODEID', unique=True)
    code = models.TextField(db_column='CODE')
    codetype = models.TextField(db_column='CODETYPE')
    codedescription = models.TextField(db_column='CODEDESCRIPTION')
    class Meta:
        managed = False
        db_table = 'READALLCODES'

class Readallcodetypes(models.Model):
    codetypeid = models.IntegerField(db_column='CODETYPEID', unique=True)
    codetype = models.TextField(db_column='CODETYPE')
    codedescription = models.TextField(db_column='CODEDESCRIPTION')
    class Meta:
        managed = False
        db_table = 'READALLCODETYPES'

