"""This module reads an XML parameters file and creates the equivalent
database.  It was written primarily for migrating the automated test suite,
but it can also serve as an example for creating a ADSM parameter file
programmatically.

This script avoids direct SQL manipulation and instead uses the models.py file
defined for the ADSM project for all object creation."""

import xml.etree.ElementTree as ET
import warnings
from pyproj import Proj

from ScenarioCreator.models import *
from Results.models import *

CREATE_AT_A_TIME = 500 # for bulk object creation



def getProductionTypes( xml, attributeName, allowedNames ):
    """Returns a list or set of production type names extractedfrom an XML
    element.  "attributeName" gives the attribute to examine (typically it is
    "production-type", "from-production-type", or "to-production-type").
    "allowedNames" is a list of all production type names in the population.
    
    The text in the attribute can be a single production type name or a comma-
    separated list of production type names.  If the XML element does not have
    an attribute matching "attributeName", all of the allowedNames are
    returned.  In other words, omitting the production type name implies
    "all"."""
    if attributeName not in xml.attrib:
        types = allowedNames
    else:
        text = xml.attrib[attributeName]
        if text == '':
            types = allowedNames
        else:
            types = text.split(',')
    return types



def sequence( tag ):
    n = 1
    while True:
        yield '%s%i' % (tag, n)
        n += 1



def getPdf( xml, nameGenerator ):
    """Returns a ProbabilityFunction object corresponding to the XML."""
    assert isinstance( xml, ET.Element )
    firstChild = list( xml )[0]
    if firstChild.tag == 'probability-density-function':
        # New style
        try:
            name = firstChild.attrib['name']
        except KeyError:
            name = next( nameGenerator )
        firstChild = list( firstChild )[0]
        # Now "firstChild" is the PDF element
    else:
        name = next( nameGenerator )
    pdfType = firstChild.tag

    args = {'equation_type': pdfType.capitalize(), 'name': name}

    if pdfType == 'beta':
        args['alpha'] = float( firstChild.find( './alpha' ).text )
        args['alpha2'] = float( firstChild.find( './beta' ).text )
        args['min'] = float( firstChild.find( './location' ).text )
        args['max'] = float( firstChild.find( './scale' ).text )
    elif pdfType == 'beta-pert':
        args['equation_type'] = 'BetaPERT'
        args['min'] = float( firstChild.find( './min' ).text )
        args['mode'] = float( firstChild.find( './mode' ).text )
        args['max'] = float( firstChild.find( './max' ).text )
    elif pdfType == 'binomial':
        args['n'] = float( firstChild.find( './n' ).text )
        args['p'] = float( firstChild.find( './p' ).text )
    elif pdfType == 'discrete-uniform':
        args['equation_type'] = 'Discrete Uniform'
        args['min'] = float( firstChild.find( './min' ).text )
        args['max'] = float( firstChild.find( './max' ).text )
    elif pdfType == 'exponential':
        args['mean'] = float( firstChild.find( './mean' ).text )
    elif pdfType == 'gamma':
        args['alpha'] = float( firstChild.find( './alpha' ).text )
        args['beta'] = float( firstChild.find( './beta' ).text )
    elif pdfType == 'gaussian':
        args['mean'] = float( firstChild.find( './mean' ).text )
        args['std_dev'] = float( firstChild.find( './stddev' ).text )
    elif pdfType == 'histogram':
        graph = RelationalFunction( name=name + ' histogram data' )
        graph.save()
        x0s = [float(el.text) for el in firstChild.findall( './/x0' )]
        x1s = [float(el.text) for el in firstChild.findall( './/x1' )]
        ps = [float(el.text) for el in firstChild.findall( './/p' )]
        # Make sure the upper x-bound of each bin equals the lower x-bound of
        # the next bin.
        assert x0s[1:] == x1s[:-1]
        for i in range( len( x0s ) ):
            point = RelationalPoint( relational_function = graph, x = x0s[i], y = ps[i] )
            point.save()
        # Final point, y is always 0
        point = RelationalPoint( relational_function = graph, x = x1s[-1], y = 0 )
        point.save()
        args['graph'] = graph
    elif pdfType == 'hypergeometric':
        args['n'] = float( firstChild.find( './n' ).text )
        args['d'] = float( firstChild.find( './d' ).text )
        args['m'] = float( firstChild.find( './m' ).text )
    elif pdfType == 'inverse-gaussian':
        args['equation_type'] = 'Inverse Gaussian'
        args['mean'] = float( firstChild.find( './mu' ).text )
        args['shape'] = float( firstChild.find( './lambda' ).text )
    elif pdfType == 'logistic':
        args['location'] = float( firstChild.find( './location' ).text )
        args['scale'] = float( firstChild.find( './scale' ).text )
    elif pdfType == 'loglogistic':
        args['equation_type'] = 'LogLogistic'
        args['location'] = float( firstChild.find( './location' ).text )
        args['scale'] = float( firstChild.find( './scale' ).text )
        args['shape'] = float( firstChild.find( './shape' ).text )
    elif pdfType == 'lognormal':
        args['mean'] = float( firstChild.find( './zeta' ).text )
        args['std_dev'] = float( firstChild.find( './sigma' ).text )
    elif pdfType == 'negative-binomial':
        args['equation_type'] = 'Negative Binomial'
        args['s'] = float( firstChild.find( './s' ).text )
        args['p'] = float( firstChild.find( './p' ).text )
    elif pdfType == 'pareto':
        args['theta'] = float( firstChild.find( './theta' ).text )
        args['a'] = float( firstChild.find( './a' ).text )
    elif pdfType == 'pearson5':
        args['equation_type'] = 'Pearson 5'
        args['alpha'] = float( firstChild.find( './alpha' ).text )
        args['beta'] = float( firstChild.find( './beta' ).text )
    elif pdfType == 'piecewise':
        graph = RelationalFunction( name=name + ' histogram data' )
        graph.save()
        # NAADSM had both "old" and "new" style piecewise PDFs. The old style
        # contained a sequence of <value> <p> <value> <p>... elements. The new
        # style contained a sequence of <value> elements each containing an <x>
        # and a <p> element.
        newStyle = firstChild.find( './/x' ) is not None
        if newStyle:
            for value in firstChild.findall( './value' ):
                x = float( value.find( './x' ).text )
                p = float( value.find( './p' ).text )
                point = RelationalPoint( relational_function = graph, x = x, y = p )
                point.save()
            # end of loop over <value> elements
        else:
            atX = True
            for element in list( firstChild ):
                if atX:
                    x = float( element.text )
                    atX = False
                else:
                    p = float( element.text )
                    point = RelationalPoint( relational_function = graph, x = x, y = p )
                    point.save()
                    atX = True
            # end of loop over <value> and <p> elements
        args['graph'] = graph
    elif pdfType == 'point':
        args['equation_type'] = 'Fixed Value'
        args['mode'] = float( firstChild.text )
    elif pdfType == 'poisson':
        args['mean'] = float( firstChild.find( './mean' ).text )
    elif pdfType == 'triangular':
        args['min'] = float( firstChild.find( './a' ).text )
        args['mode'] = float( firstChild.find( './c' ).text )
        args['max'] = float( firstChild.find( './b' ).text )
    elif pdfType == 'uniform':
        args['min'] = float( firstChild.find( './a' ).text )
        args['max'] = float( firstChild.find( './b' ).text )
    elif pdfType == 'weibull':
        args['alpha'] = float( firstChild.find( './alpha' ).text )
        args['beta'] = float( firstChild.find( './beta' ).text )
    else:
        print( pdfType )
        raise NotImplementedError

    pdf = ProbabilityFunction( **args )
    pdf.save()
    return pdf



def getRelChart( xml, nameGenerator ):
    """Returns a RelationalFunction object corresponding to the XML."""
    assert isinstance( xml, ET.Element )
    firstChild = list( xml )[0]
    if firstChild.tag == 'relational-function':
        # New style
        try:
            name = firstChild.attrib['name']
        except KeyError:
            name = next( nameGenerator )
        relChart, created = RelationalFunction.objects.get_or_create( name=name )
        if created:
            # This is a new RelationalFunction: no RelationalFunction with this
            # name has been encountered in the XML so far.
            for xyPair in firstChild.findall( './value' ):
                point = RelationalPoint(
                    relational_function = relChart,
                    x = float( xyPair.find( './x' ).text ),
                    y = float( xyPair.find( './y' ).text )
                )
                point.save()
            # end of loop over points
        else:
            # One or more RelationalFunctions with this name have already been
            # encountered in the XML.  Check whether this RelationalFunction
            # contains exactly the same points as the previously-seen
            # RelationalFunction(s) with the same name.
            points = RelationalPoint.objects.filter( relational_function=relChart ).order_by( 'x' )
            same = True
            i = 0
            for xyPair in firstChild.findall( './value' ):
                x = float( xyPair.find( './x' ).text )
                y = float( xyPair.find( './y' ).text )
                if x != points[i].x or y != points[i].y:
                    same = False
                    break
                i += 1
            if not same:
                # The points in the current XML are *not* the same as the ones
                # in previously-seen RelationalFunction(s) with the same name.
                # Give this chart a new, automatically-generated name.
                relChart = RelationalFunction( name=next( nameGenerator ) )
                relChart.save()
                for xyPair in firstChild.findall( './value' ):
                    point = RelationalPoint(
                        relational_function = relChart,
                        x = float( xyPair.find( './x' ).text ),
                        y = float( xyPair.find( './y' ).text )
                    )
                    point.save()
                # end of loop over points
            # end of case where we create a new RelationalFunction
        # end of case where we are handling a "new-style" <relational-function>
        # element, that has a name attached to it.
    else:
        # Old style
        relChart = RelationalFunction( name=next( nameGenerator ) )
        relChart.save()
        values = [float( el.text ) for el in xml.findall( './/value' )]
        while values:
            point = RelationalPoint(
                relational_function = relChart,
                x = values[0],
                y = values[1]
            )
            point.save()
            values = values[2:]

    return relChart



def getBool( xml ):
    """Returns a boolean corresponding to the XML."""
    return xml.text.lower() in ('1', 'y', 'yes', 't', 'true')



def readPopulation( populationFileName ):
    fp = open( populationFileName, 'rb' )
    xml = ET.parse( fp ).getroot()
    fp.close()

    # Create a dictionary to remap long state names to one-letter codes.
    stateCodes = {}
    for code, fullName in Unit.initial_state_choices:
        stateCodes[fullName] = code
        stateCodes[fullName.replace( ' ', '' )] = code

    # Are the locations given in projected coordinates? If so, create an object
    # that can convert them to lat-long.
    projection = None
    srs = xml.find( './spatial_reference/PROJ4' )
    if srs is not None:
        projection = Proj( srs.text, preserve_units=True )

    population = Population()
    population.save()
    bulkUnits = []
    for el in xml.findall( './/herd' ):
        description = el.find( './id' )
        if description is None:
            description = ''
        else:
            description = description.text
        typeName = el.find( './production-type' ).text
        try:
            productionType = ProductionType.objects.get( name=typeName )
        except ProductionType.DoesNotExist:
            productionType = ProductionType( name=typeName )
            productionType.save()
        size = int( el.find( './size' ).text )
        if not projection:
            lat = float( el.find( './location/latitude' ).text )
            long = float( el.find( './location/longitude' ).text )
        else:
            x = float( el.find( './location/x' ).text )
            y = float( el.find( './location/y' ).text )
            long, lat = projection( x, y, inverse=True )

        state = el.find( './status' ).text
        if state not in stateCodes.values():
            try:
                state = stateCodes[state]
            except KeyError:
                raise Exception( '%s is not a valid state' % state )
        daysInState = el.find( './days-in-status' )
        if daysInState is not None:
            daysInState = int( daysInState.text )
        daysLeftInState = el.find( './days-left-in-status' )
        if daysLeftInState is not None:
            daysLeftInState = int( daysLeftInState.text )

        bulkUnits.append( Unit(
            _population = population,
            production_type = productionType,
            latitude = lat,
            longitude = long,
            initial_state = state,
            days_in_initial_state = daysInState,
            days_left_in_initial_state = daysLeftInState,
            initial_size = size,
            user_notes = description
        ))
        if len( bulkUnits ) >= CREATE_AT_A_TIME:
            Unit.objects.bulk_create( bulkUnits )
            bulkUnits = []
    # end of loop over units in XML file
    if bulkUnits:
        Unit.objects.bulk_create( bulkUnits )

    return # from readPopulation



def readParameters( parameterFileName, saveIterationOutputsForUnits ):
    fp = open( parameterFileName, 'rb' )
    try:
        xml = ET.parse( fp ).getroot()
    except ET.ParseError as e:
        # XML parameter files exported from NAADSM contain elements with an
        # "xdf" prefix, but the files do not define that namespace. This can
        # result in an "unbound prefix" exception, which we handle here.
        #
        # Any exception other than "unbound prefix", we just re-raise.
        if not 'unbound prefix' in str( e ):
            raise
        # Rewind to the start of the file, and read it into memory as binary.
        fp.seek( 0 )
        fileAsBinary = bytearray( fp.read() )
        # Try to guess the encoding.
        possibleEncodings = ('utf-16', 'utf-8', 'us-ascii')
        fileAsString = None
        for encoding in possibleEncodings:
            try:
                fileAsString = fileAsBinary.decode( encoding )
                break
            except UnicodeDecodeError:
                pass
        # end of loop over possible encodings
        assert fileAsString is not None
        # Insert text to define the xdf namespace.
        fileAsString = fileAsString.replace( 'xmlns:', 'xmlns:xdf="http://xml.gsfc.nasa.gov/XDF" xmlns:', 1 )
        xml = ET.fromstring( fileAsString )
    fp.close()

    scenario = Scenario(
        description = xml.find( './description' ).text
    )
    scenario.save()

    if xml.find( './exit-condition/first-detection' ) is not None:
        earlyExitCondition = 'first-detection'
    elif xml.find( './exit-condition/disease-end' ) is not None:
        earlyExitCondition = 'disease-end'
    else:
        earlyExitCondition = ''
    outputSettings = OutputSettings(
        iterations = int( xml.find( './num-runs' ).text ),
        days = int( xml.find( './num-days' ).text ),
        stop_criteria = earlyExitCondition,
        save_daily_unit_states = (xml.find( './/state-table-writer' ) is not None),
        save_daily_events = (xml.find( './/apparent-events-table-writer' ) is not None),
        save_daily_exposures = (xml.find( './/exposures-table-writer' ) is not None),
        save_iteration_outputs_for_units = saveIterationOutputsForUnits,
        save_map_output = (xml.find( './/weekly-gis-writer' ) is not None or xml.find( './/summary-gis-writer' ) is not None),
        cost_track_zone_surveillance = (xml.find( './/economic-model/surveillance' ) is not None),
        cost_track_vaccination = (xml.find( './/economic-model/vaccination' ) is not None),
        cost_track_destruction = (xml.find( './/economic-model/euthanasia' ) is not None)
    )
    outputSettings.save()

    # Make a set containing all production type names. Initialize with the
    # names already found in readPopulation, then add any new ones found in the
    # parameters file.
    productionTypeNames = set( [productionType.name for productionType in ProductionType.objects.all()] )
    for el in xml.findall( './/*[@production-type]' ):
        productionTypeNames.update( getProductionTypes( el, 'production-type', [] ) )
    for el in xml.findall( './/*[@to-production-type]' ):
        productionTypeNames.update( getProductionTypes( el, 'to-production-type', [] ) )
    for el in xml.findall( './/*[@from-production-type]' ):
        productionTypeNames.update( getProductionTypes( el, 'from-production-type', [] ) )
    # If an empty production type attribute appeared anywhere in the XML,
    # ignore that.
    if '' in productionTypeNames:
        productionTypeNames.remove( '' )
    for name in productionTypeNames:  # Creates all the production types if they do not exist
        ProductionType.objects.get_or_create( name=name )

    useAirborneExponentialDecay = xml.find( './/airborne-spread-exponential-model' ) is not None
    disease = Disease(
        name='',
        include_airborne_spread = xml.find( './/airborne-spread-model' ) is not None or xml.find( './/airborne-spread-exponential-model' ) is not None,
        include_direct_contact_spread = False,
        include_indirect_contact_spread = False,
        use_airborne_exponential_decay = useAirborneExponentialDecay
    )
    disease.save()

    # Create a sequence to be used to give names to unnamed PDFs.
    pdfNameSequence = sequence( 'PDF' )
    # Create a sequence to be used to give names to unnamed relational charts.
    relChartNameSequence = sequence( 'Rel' )

    for el in xml.findall( './/disease-model' ):
        latentPeriod = getPdf( el.find( './latent-period' ), pdfNameSequence )
        subclinicalPeriod = getPdf( el.find( './infectious-subclinical-period' ), pdfNameSequence )
        clinicalPeriod = getPdf( el.find( './infectious-clinical-period' ), pdfNameSequence )
        immunePeriod = getPdf( el.find( './immunity-period' ), pdfNameSequence )
        if el.find( './prevalence' ) is not None:
            prevalence = getRelChart( el.find( './prevalence' ), relChartNameSequence )
        else:
            prevalence = None

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            diseaseProgression = DiseaseProgression(
                _disease = disease,
                name = typeName + ' Progression',
                disease_latent_period = latentPeriod,
                disease_subclinical_period = subclinicalPeriod,
                disease_clinical_period = clinicalPeriod,
                disease_immune_period = immunePeriod,
                disease_prevalence = prevalence,
            )
            diseaseProgression.save()

            diseaseProgressionAssignment = DiseaseProgressionAssignment(
                production_type = ProductionType.objects.get( name=typeName ),
                progression = diseaseProgression
            )
            diseaseProgressionAssignment.save()
        # end of loop over production types covered by this <disease-model> element
    # end of loop over <disease-model> elements

    for el in xml.findall( './/airborne-spread-model' ) + xml.findall( './/airborne-spread-exponential-model' ):
        if useAirborneExponentialDecay:
            maxDistance = 0
        else:
            maxDistance = float( el.find( './max-spread/value' ).text )
        if el.find( './delay' ) is not None:
            delay = getPdf( el.find( './delay' ), pdfNameSequence )
        else:
            delay = None

        for fromTypeName in getProductionTypes( el, 'from-production-type', productionTypeNames ):
            for toTypeName in getProductionTypes( el, 'to-production-type', productionTypeNames ):
                airborneSpread = AirborneSpread(
                  _disease = disease,
                  name = 'Airborne %s -> %s' % (fromTypeName, toTypeName),
                  max_distance = maxDistance,
                  spread_1km_probability = float( el.find( './prob-spread-1km' ).text ),
                  exposure_direction_start = float( el.find( './wind-direction-start/value' ).text ),
                  exposure_direction_end = float( el.find( './wind-direction-end/value' ).text ),
                  transport_delay = delay
                )
                airborneSpread.save()

                pairing = DiseaseSpreadAssignment(
                  source_production_type = ProductionType.objects.get( name=fromTypeName ),
                  destination_production_type = ProductionType.objects.get( name=toTypeName ),
                  airborne_spread = airborneSpread
                )
                pairing.save()
            # end of loop over to-production-types covered by this <airborne-spread[-exponential]-model> element
        # end of loop over from-production-types covered by this <airborne-spread[-exponential]-model> element
    # end of loop over <airborne-spread[-exponential]-model> elements

    for el in xml.findall( './/zone-model' ):
        name = el.find( './name' ).text
        radius = float( el.find( './radius/value' ).text )
        if radius > 0:
            zone = Zone( name=name, radius=radius )
            zone.save()
    # end of loop over <zone-model> elements

    for el in xml.findall( './/contact-spread-model' ):
        if 'zone' in el.attrib:
            continue
        fixedRate = (el.find( './fixed-movement-rate' ) is not None)
        if fixedRate:
            contactRate = float( el.find( './fixed-movement-rate/value' ).text )
        else:
            contactRate = float( el.find( './movement-rate/value' ).text )
        distance = getPdf( el.find( './distance' ), pdfNameSequence )
        if el.find( './delay' ) is not None:
            delay = getPdf( el.find( './delay' ), pdfNameSequence )
        else:
            delay = None
        if el.find( './prob-infect' ) is not None:
            probInfect = float( el.find( './prob-infect' ).text )
        else:
            probInfect = 0
        try:
            latentCanInfect = getBool( el.find( './latent-units-can-infect' ) )
        except AttributeError:
            latentCanInfect = True # default
        try:
            subclinicalCanInfect = getBool( el.find( './subclinical-units-can-infect' ) )
        except AttributeError:
            subclinicalCanInfect = True # default
        movementControl = getRelChart( el.find( './movement-control' ), relChartNameSequence )

        for fromTypeName in getProductionTypes( el, 'from-production-type', productionTypeNames ):
            for toTypeName in getProductionTypes( el, 'to-production-type', productionTypeNames ):
                if el.attrib['contact-type'] == 'direct':
                    contactSpreadModel = DirectSpread(
                        _disease = disease,
                        name='Direct %s -> %s' % (fromTypeName, toTypeName),
                        use_fixed_contact_rate = fixedRate,
                        contact_rate = contactRate,
                        movement_control = movementControl,
                        distance_distribution = distance,
                        transport_delay = delay,
                        infection_probability = probInfect,
                        latent_animals_can_infect_others = latentCanInfect,
                        subclinical_animals_can_infect_others = subclinicalCanInfect
                    )
                    disease.include_direct_contact_spread = True
                elif el.attrib['contact-type'] == 'indirect':
                    contactSpreadModel = IndirectSpread(
                        _disease = disease,
                        name='Indirect %s -> %s' % (fromTypeName, toTypeName),
                        use_fixed_contact_rate = fixedRate,
                        contact_rate = contactRate,
                        movement_control = movementControl,
                        distance_distribution = distance,
                        transport_delay = delay,
                        infection_probability = probInfect,
                        subclinical_animals_can_infect_others = subclinicalCanInfect
                    )
                    disease.include_indirect_contact_spread = True
                else:
                    assert False
                contactSpreadModel.save()
                disease.save()

                pairing, created = DiseaseSpreadAssignment.objects.get_or_create(
                    source_production_type = ProductionType.objects.get( name=fromTypeName ),
                    destination_production_type = ProductionType.objects.get( name=toTypeName )
                )
                if el.attrib['contact-type'] == 'direct':
                    pairing.direct_contact_spread = contactSpreadModel
                else:
                    pairing.indirect_contact_spread = contactSpreadModel
                pairing.save()
            # end of loop over to-production-types covered by this <contact-spread-model> element
        # end of loop over from-production-types covered by this <contact-spread-model> element
    # end of loop over <contact-spread-model> elements without a "zone" attribute

    for el in xml.findall( './/contact-spread-model' ):
        if 'zone' not in el.attrib:
            continue

        fromTypeNames = getProductionTypes( el, 'from-production-type', productionTypeNames )
        if 'contact-type' in el.attrib:
            contactType = el.attrib['contact-type']
            assert (contactType == 'direct' or contactType == 'indirect')
        else:
            contactType = 'both'
        zoneName = el.attrib['zone']
        movementControl = getRelChart( el.find( './movement-control' ), relChartNameSequence )

        for fromTypeName in fromTypeNames:
            # If a ZoneEffect object has already been assigned to this
            # combination of zone and production type, retrieve it; otherwise,
            # create a new one.
            try:
                assignment = ZoneEffectAssignment.objects.get(
                    zone__name=zoneName,
                    production_type__name=fromTypeName
                )
                effect = assignment.effect
            except ZoneEffectAssignment.DoesNotExist:
                effect = ZoneEffect(name = zoneName + ' effect on ' + fromTypeName)
                effect.save()
                assignment = ZoneEffectAssignment(
                    zone = Zone.objects.get( name=zoneName ),
                    production_type = ProductionType.objects.get( name=fromTypeName ),
                    effect = effect
                )
                assignment.save()
            if contactType == 'direct' or contactType == 'both':
                effect.zone_direct_movement = movementControl
            if contactType == 'indirect' or contactType == 'both':
                effect.zone_indirect_movement = movementControl
            effect.save()
        # end of loop over from-production-types covered by this <contact-spread-model> element
    # end of loop over <contact-spread-model> elements with a "zone" attribute

    plan = None
    useDetection = (xml.find( './/detection-model' ) is not None)
    useTracing = (
    (xml.find( './/trace-model' ) is not None)
    or (xml.find( './/trace-back-destruction-model' ) is not None)
    )
    useVaccination = (
    (xml.find( './/vaccine-model' ) is not None)
    or (xml.find( './/ring-vaccination-model' ) is not None)
    )
    useDestruction = (
    (xml.find( './/basic-destruction-model' ) is not None)
    or (xml.find( './/trace-destruction-model' ) is not None)
    or (xml.find( './/trace-back-destruction-model' ) is not None)
    or (xml.find( './/ring-destruction-model' ) is not None)
    )

    if useDetection or useTracing or useVaccination or useDestruction:
        plan = ControlMasterPlan()
        plan.save()

    # Create a PDF that always returns 0. Will be used as the default for the
    # test delay PDF.
    zeroDelay = ProbabilityFunction( name='Zero delay', equation_type='Fixed Value', mode=0 )
    zeroDelay.save()

    for el in xml.findall( './/detection-model' ):
        # <detection-model> elements come in 2 forms. The first form, with a
        # production-type attribute, specifies the probability of observing
        # clinical signs of disease and the probability of reporting those
        # signs. The second form, with a production-type attribute and a zone
        # attribute, specifies a multiplier to use on the probability of
        # observing clinical signs when inside a zone.
        if 'zone' in el.attrib:
            multiplier = float( el.find( './zone-prob-multiplier' ).text )
        else:
            observing = getRelChart( el.find( './prob-report-vs-time-clinical' ), relChartNameSequence )
            reporting = getRelChart( el.find( './prob-report-vs-time-since-outbreak' ), relChartNameSequence )

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            if 'zone' in el.attrib:
                zoneName = el.attrib['zone']
                # If a ZoneEffect object has already been assigned to this
                # combination of zone and production type, retrieve it; otherwise,
                # create a new one.
                try:
                    assignment = ZoneEffectAssignment.objects.get(
                        zone__name=zoneName,
                        production_type__name=typeName
                    )
                    effect = assignment.effect
                except ZoneEffectAssignment.DoesNotExist:
                    effect = ZoneEffect(name= zoneName + ' effect on ' + typeName)
                    effect.save()
                    assignment = ZoneEffectAssignment(
                        zone = Zone.objects.get( name=zoneName ),
                        production_type = ProductionType.objects.get( name=typeName ),
                        effect = effect
                    )
                    assignment.save()
                effect.zone_detection_multiplier = multiplier
                effect.save()
            else:
                protocol = ControlProtocol(
                    name = typeName + " Protocol",
                    use_detection = True,
                    detection_probability_for_observed_time_in_clinical = observing,
                    detection_probability_report_vs_first_detection = reporting,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
        # end of loop over production-types covered by this <detection-model> element
    # end of loop over <detection-model> elements

    for el in xml.findall( './/contact-recorder-model' ):
        try:
            contactType = el.attrib['contact-type']
            assert (contactType == 'direct' or contactType == 'indirect')
        except KeyError:
            contactType = 'both'
        try:
            direction = el.attrib['direction']
            assert (direction == 'in' or direction == 'out')
        except KeyError:
            direction = 'both'
        traceSuccess = float( el.find( './trace-success' ).text )
        if el.find( './trace-delay' ) is not None:
            traceDelay = getPdf( el.find( './trace-delay' ), pdfNameSequence )
        else:
            traceDelay = zeroDelay # default

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            if contactType == 'direct' or contactType == 'both':
                protocol.direct_trace_success_rate = traceSuccess
            if contactType == 'indirect' or contactType == 'both':
                protocol.indirect_trace_success = traceSuccess
            protocol.trace_result_delay = traceDelay
            protocol.save()
        # end of loop over production types covered by this <contact-recorder-model> element
    # end of loop over <contact-recorder-model> elements

    for el in xml.findall( './/trace-model' ):
        try:
            contactType = el.attrib['contact-type']
            assert (contactType == 'direct' or contactType == 'indirect')
        except KeyError:
            contactType = 'both'
        try:
            direction = el.attrib['direction']
            assert (direction == 'in' or direction == 'out')
        except KeyError:
            direction = 'both'
        tracePeriod = int( el.find( './trace-period/value' ).text )

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.use_tracing = True
            if contactType == 'direct' or contactType == 'both':
                if direction == 'out' or direction == 'both':
                    protocol.trace_direct_forward = True
                if direction == 'in' or direction == 'both':
                    protocol.trace_direct_back = True
                protocol.direct_trace_period = tracePeriod
            if contactType == 'indirect' or contactType == 'both':
                if direction == 'out' or direction == 'both':
                    protocol.trace_indirect_forward = True
                if direction == 'in' or direction == 'both':
                    protocol.trace_indirect_back = True
                protocol.indirect_trace_period = tracePeriod
            protocol.save()
        # end of loop over production types covered by this <trace-model> element
    # end of loop over <trace-model> elements

    for el in xml.findall( './/trace-exam-model' ):
        try:
            contactType = el.attrib['contact-type']
            assert (contactType == 'direct' or contactType == 'indirect')
        except KeyError:
            contactType = 'both'
        try:
            direction = el.attrib['direction']
            assert (direction == 'in' or direction == 'out')
        except KeyError:
            direction = 'both'
        detectionMultiplier = float( el.find( './detection-multiplier' ).text )
        try:
            testIfNoSigns = getBool( el.find( './test-if-no-signs' ) )
        except AttributeError:
            testIfNoSigns = False

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            if contactType == 'direct' or contactType == 'both':
                if direction == 'out' or direction == 'both':
                    protocol.examine_direct_forward_traces = True
                    protocol.exam_direct_forward_success_multiplier = detectionMultiplier
                    protocol.test_direct_forward_traces = testIfNoSigns
                if direction == 'in' or direction == 'both':
                    protocol.examine_direct_back_traces = True
                    protocol.exam_direct_back_success_multiplier = detectionMultiplier
                    protocol.test_direct_back_traces = testIfNoSigns
            if contactType == 'indirect' or contactType == 'both':
                if direction == 'out' or direction == 'both':
                    protocol.examine_indirect_forward_traces = True
                    protocol.exam_indirect_forward_success_multiplier = detectionMultiplier
                    protocol.test_indirect_forward_traces = testIfNoSigns
                if direction == 'in' or direction == 'both':
                    protocol.examine_indirect_back_traces = True
                    protocol.examine_indirect_back_success_multiplier = detectionMultiplier
                    protocol.test_indirect_back_traces = testIfNoSigns
            protocol.save()
        # end of loop over production types covered by this <trace-exam-model> element
    # end of loop over <trace-exam-model> elements

    for el in xml.findall( './/test-model' ):
        sensitivity = float( el.find( './sensitivity' ).text )
        specificity = float( el.find( './specificity' ).text )
        delay = getPdf( el.find( './delay' ), pdfNameSequence )
        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.use_testing = True
            protocol.test_sensitivity = sensitivity
            protocol.test_specificity = specificity
            protocol.test_delay = delay
            protocol.save()
        # end of loop over production types covered by this <test-model> element		
    # end of loop over <test-model> elements

    for el in xml.findall( './/basic-zone-focus-model' ):
        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.detection_is_a_zone_trigger = True
            protocol.save()
        # end of loop over production types covered by this <basic-zone-focus-model> element
    # end of loop over <basic-zone-focus-model> elements

    for el in xml.findall( './/trace-back-zone-focus-model' ) + xml.findall( './/trace-zone-focus-model' ):
        # <trace-back-zone-focus-model> is an older module, superseded by the
        # combination of contact-recorder-model, trace-model, and trace-zone-
        # focus-model.

        if 'contact-type' in el.attrib:
            contactType = el.attrib['contact-type']
            assert (contactType == 'direct' or contactType == 'indirect')
        else:
            contactType = 'both'

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.use_tracing = True
            if contactType == 'direct' or contactType == 'both':
                protocol.direct_trace_is_a_zone_trigger = True
            if contactType == 'indirect' or contactType == 'both':
                protocol.indirect_trace_is_a_zone_trigger = True
            protocol.save()
        # end of loop over production types covered by this <trace-back-zone-focus-model> or <trace-zone-focus-model> element
    # end of loop over <trace-back-zone-focus-model> and <trace-zone-focus-model> elements

    # Vaccination priority order information is distributed among several
    # different elements. Keep a list that will help sort it out later.
    vaccinationProductionTypeOrder = []

    productionTypesWithVaccineEffectsDefined = set()
    for el in xml.findall( './/vaccine-model' ):
        delay = int( el.find( './delay/value' ).text )
        immunityPeriod = getPdf( el.find( './immunity-period' ), pdfNameSequence )

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.days_to_immunity = delay
            protocol.vaccine_immune_period = immunityPeriod
            protocol.save()
            productionTypesWithVaccineEffectsDefined.add( typeName )
        # end of loop over production types covered by this <vaccine-model> element
    # end of loop over <vaccine-model> elements

    productionTypesThatAreVaccinated = set()
    for el in xml.findall( './/ring-vaccination-model' ):
        # Older XML files allowed just a "production-type" attribute and an
        # implied "from-any" functionality.
        if 'production-type' in el.attrib:
            fromTypeNames = productionTypeNames
            toTypeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        else:
            fromTypeNames = getProductionTypes( el, 'from-production-type', productionTypeNames )
            toTypeNames = getProductionTypes( el, 'to-production-type', productionTypeNames )

        radius = float( el.find( './radius/value' ).text )
        for fromTypeName in fromTypeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=fromTypeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=fromTypeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.trigger_vaccination_ring = True
            protocol.vaccination_ring_radius = radius
            protocol.save()
        # end of loop over from-production-types covered by this <ring-vaccination-model> element

        priority = int( el.find( './priority' ).text )
        minTimeBetweenVaccinations = int( el.find( './min-time-between-vaccinations/value' ).text )
        try:
            vaccinateDetectedUnits = getBool( el.find( './vaccinate-detected-units' ) )
        except AttributeError:
            vaccinateDetectedUnits = True
        for toTypeName in toTypeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=toTypeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=toTypeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.use_vaccination = True
            protocol.minimum_time_between_vaccinations = minTimeBetweenVaccinations
            protocol.vaccinate_detected_units = vaccinateDetectedUnits
            protocol.save()
            vaccinationProductionTypeOrder.append( (priority, toTypeName) )
            productionTypesThatAreVaccinated.add( toTypeName )
        # end of loop over to-production-types covered by this <ring-vaccination-model> element
    # end of loop over <ring-vaccination-model> elements

    if len( productionTypesThatAreVaccinated - productionTypesWithVaccineEffectsDefined ) > 0:
        raise Exception( 'some production types that are vaccinated do not have vaccine effects defined' )
    if productionTypesThatAreVaccinated != productionTypesWithVaccineEffectsDefined:
        warnings.warn( 'mismatch between production types that are vaccinated and production types that have vaccine effects defined', Warning )

    # Destruction priority order information is distributed among several
    # different elements. Keep 2 lists that will help sort it out later.
    destructionReasonOrder = []
    destructionProductionTypeOrder = []

    for el in xml.findall( './/trace-back-destruction-model' ):
        # This is an older module, superseded by the combination of contact-
        # recorder-model, trace-model, and trace-destruction-model.

        # Enable trace forward/out from all production types.
        contactType = el.attrib['contact-type']
        assert (contactType == 'direct' or contactType == 'indirect')
        tracePeriod = int( el.find( './trace-period/value' ).text )
        traceSuccess = float( el.find( './trace-success' ).text )
        for typeName in productionTypeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.use_tracing = True
            if contactType == 'direct':
                protocol.trace_direct_forward = True
                protocol.direct_trace_success_rate = traceSuccess
                protocol.direct_trace_period = tracePeriod
            else:
                protocol.trace_indirect_forward = True
                protocol.indirect_trace_success = traceSuccess
                protocol.indirect_trace_period = tracePeriod
            protocol.trace_result_delay = zeroDelay
            protocol.save()
        # end of loop to enable trace forward/out from all production types

        # Enable destruction of specific production types when identified by
        # trace.
        priority = int( el.find( './priority' ).text )
        try:
            quarantineOnly = getBool( el.find( './quarantine-only' ) )
        except AttributeError:
            quarantineOnly = False
        if not quarantineOnly:
            typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
            for typeName in typeNames:
                # If a ControlProtocol object has already been assigned to this
                # production type, retrieve it; otherwise, create a new one.
                try:
                    assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                    protocol = assignment.control_protocol
                except ProtocolAssignment.DoesNotExist:
                    protocol = ControlProtocol(
                        use_detection = False,
                        test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                    )
                    protocol.save()
                    assignment = ProtocolAssignment(
                        production_type = ProductionType.objects.get( name=typeName ),
                        control_protocol = protocol
                    )
                    assignment.save()
                if contactType == 'direct':
                    protocol.destroy_direct_forward_traces = True
                    reason = 'Trace fwd direct'
                else:
                    protocol.destroy_indirect_forward_traces = True
                    reason = 'Trace fwd indirect'
                protocol.save()
                destructionReasonOrder.append( (priority, reason) )
                destructionProductionTypeOrder.append ( (priority, typeName) )
            # end of loop over production-types covered by this <trace-back-destruction-model> element
        # end of if not quarantineOnly
    # end of loop over <trace-back-destruction-model> elements

    for el in xml.findall( './/basic-destruction-model' ):
        priority = int( el.find( './priority' ).text )

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.use_destruction = True
            protocol.save()
            destructionReasonOrder.append( (priority, 'Basic') )
            destructionProductionTypeOrder.append ( (priority, typeName) )
        # end of loop over production-types covered by this <basic-destruction-model> element
    # end of loop over <basic-destruction-model> elements

    for el in xml.findall( './/trace-destruction-model' ):
        try:
            contactType = el.attrib['contact-type']
            assert (contactType == 'direct' or contactType == 'indirect')
        except KeyError:
            contactType = 'both'
        try:
            direction = el.attrib['direction']
            assert (direction == 'in' or direction == 'out')
        except KeyError:
            direction = 'both'
        priority = int( el.find( './priority' ).text )

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            if contactType == 'direct' or contactType == 'both':
                if direction == 'out' or direction == 'both':
                    protocol.destroy_direct_forward_traces = True
                    destructionReasonOrder.append( (priority, 'Trace fwd direct') )
                if direction == 'in' or direction == 'both':
                    protocol.destroy_direct_back_traces = True
                    destructionReasonOrder.append( (priority, 'Trace back direct') )
            if contactType == 'indirect' or contactType == 'both':
                if direction == 'out' or direction == 'both':
                    protocol.destroy_indirect_forward_traces = True
                    destructionReasonOrder.append( (priority, 'Trace fwd indirect') )
                if direction == 'in' or direction == 'both':
                    protocol.destroy_indirect_back_traces = True
                    destructionReasonOrder.append( (priority, 'Trace back indirect') )
            protocol.save()
            destructionProductionTypeOrder.append ( (priority, typeName) )
        # end of loop over production-types covered by this <trace-destruction-model> element
    # end of loop over <trace-destruction-model> elements

    for el in xml.findall( './/ring-destruction-model' ):
        # Older XML files allowed just a "production-type" attribute and an
        # implied "from-any" functionality.
        if 'production-type' in el.attrib:
            fromTypeNames = productionTypeNames
            toTypeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        else:
            fromTypeNames = getProductionTypes( el, 'from-production-type', productionTypeNames )
            toTypeNames = getProductionTypes( el, 'to-production-type', productionTypeNames )

        radius = float( el.find( './radius/value' ).text )
        for fromTypeName in fromTypeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=fromTypeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=fromTypeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.destruction_is_a_ring_trigger = True
            protocol.destruction_ring_radius = radius
            protocol.save()
        # end of loop over from-production-types covered by this <ring-destruction-model> element

        priority = int( el.find( './priority' ).text )
        for toTypeName in toTypeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=toTypeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=toTypeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.destruction_is_a_ring_target = True
            protocol.save()
            destructionReasonOrder.append( (priority, 'Ring') )
            destructionProductionTypeOrder.append( (priority, toTypeName) )
        # end of loop over to-production-types covered by this <ring-destruction-model> element
    # end of loop over <ring-destruction-model> elements

    for el in xml.findall( './/resources-and-implementation-of-controls-model' ):
        if useDestruction:
            plan.destruction_program_delay = int( el.find( './destruction-program-delay/value' ).text )
            plan.destruction_capacity = getRelChart( el.find( './destruction-capacity' ), relChartNameSequence )
            try:
                order = el.find( './destruction-priority-order' ).text.strip()
            except AttributeError:
                order = 'reason,production type,time waiting' # the old default
            # The XML did not put spaces after the commas, but the Django
            # model does.
            order = ', '.join( order.split( ',' ) )
            plan.destruction_priority_order = order

            # Create a new version of destructionReasonOrder where a) only the
            # minimum priority number attached to each reason is preserved and
            # b) the list is sorted by priority.
            newDestructionReasonOrder = []
            for reason in set( [item[1] for item in destructionReasonOrder] ):
                minPriority = min( [item[0] for item in filter( lambda item: item[1]==reason, destructionReasonOrder )] )
                newDestructionReasonOrder.append( (minPriority, reason) )
            newDestructionReasonOrder.sort()
            plan.destruction_reason_order = ', '.join( [item[1] for item in newDestructionReasonOrder] )

            # Similar process for destructionProductionTypeOrder.
            newDestructionProductionTypeOrder = []
            for typeName in set( [item[1] for item in destructionProductionTypeOrder] ):
                minPriority = min( [item[0] for item in filter( lambda item: item[1]==typeName, destructionProductionTypeOrder )] )
                newDestructionProductionTypeOrder.append( (minPriority, typeName) )
            newDestructionProductionTypeOrder.sort()
            newDestructionProductionTypeOrder = [item[1] for item in newDestructionProductionTypeOrder]
            priority = 1
            for typeName in newDestructionProductionTypeOrder:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
                protocol.destruction_priority = priority
                protocol.save()
                priority += 1

            plan.save()
        # end of if useDestruction==True

        if useVaccination:
            try:
                plan.units_detected_before_triggering_vaccination = int( el.find( './vaccination-program-delay' ).text )
            except AttributeError:
                plan.units_detected_before_triggering_vaccination = 1 # default
            plan.vaccination_capacity = getRelChart( el.find( './vaccination-capacity' ), relChartNameSequence )
            order = el.find( './vaccination-priority-order' ).text.strip()
            # The XML did not put spaces after the commas, but the Django
            # model does.
            order = ', '.join( order.split( ',' ) )
            plan.vaccination_priority_order = order

            # Create a new version of vaccinationProductionTypeOrder where a)
            # only the minimum priority number attached to each production type
            # is preserved and b) the list is sorted by priority.
            newVaccinationProductionTypeOrder = []
            for typeName in set( [item[1] for item in vaccinationProductionTypeOrder] ):
                minPriority = min( [item[0] for item in filter( lambda item: item[1]==typeName, vaccinationProductionTypeOrder )] )
                newVaccinationProductionTypeOrder.append( (minPriority, typeName) )
            newVaccinationProductionTypeOrder.sort()
            newVaccinationProductionTypeOrder = [item[1] for item in newVaccinationProductionTypeOrder]
            priority = 1
            for typeName in newVaccinationProductionTypeOrder:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
                protocol.vaccination_priority = priority
                protocol.save()
                priority += 1

            plan.save()
        # end of if useVaccination==True
    # end of loop over <resources-and-implementation-of-control-model> elements

    for el in xml.findall( './/economic-model' ):
        try:
            vaccinationFixed = float( el.find( './vaccination-fixed/value' ).text )
        except AttributeError:
            vaccinationFixed = None
        try:
            vaccinationBase = float( el.find( './vaccination/value' ).text )
        except AttributeError:
            vaccinationBase = None
        try:
            vaccinationExtra = float( el.find( './additional-vaccination/value' ).text )
        except AttributeError:
            vaccinationExtra = None
        try:
            baselineCapacity = int( el.find( './baseline-vaccination-capacity' ).text )
        except AttributeError:
            baselineCapacity = None

        try:
            appraisal = float( el.find( './appraisal/value' ).text )
        except AttributeError:
            appraisal = None
        try:
            euthanasia = float( el.find( './euthanasia/value' ).text )
        except AttributeError:
            euthanasia = None
        try:
            indemnification = float( el.find( './indemnification/value' ).text )
        except AttributeError:
            indemnification = None
        try:
            disposal = float( el.find( './carcass-disposal/value' ).text )
        except AttributeError:
            disposal = None
        try:
            cleaning = float( el.find( './cleaning-disinfecting/value' ).text )
        except AttributeError:
            cleaning = None

        try:
            surveillance = float( el.find( './surveillance/value' ).text )
        except AttributeError:
            surveillance = None

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False,
                    test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.use_cost_accounting = True
            if vaccinationFixed is not None:
                protocol.cost_of_vaccination_setup_per_unit = vaccinationFixed
            if vaccinationBase is not None:
                protocol.cost_of_vaccination_baseline_per_animal = vaccinationBase
            if vaccinationExtra is not None:
                protocol.cost_of_vaccination_additional_per_animal = vaccinationExtra
            if baselineCapacity is not None:
                protocol.vaccination_demand_threshold = baselineCapacity
            if appraisal is not None:
                protocol.cost_of_destruction_appraisal_per_unit = appraisal
            if euthanasia is not None:
                protocol.cost_of_euthanasia_per_animal = euthanasia
            if indemnification is not None:
                protocol.cost_of_indemnification_per_animal = indemnification
            if disposal is not None:
                protocol.cost_of_carcass_disposal_per_animal = disposal
            if cleaning is not None:
                protocol.cost_of_destruction_cleaning_per_unit = cleaning
            protocol.save()

            if 'zone' in el.attrib and surveillance is not None:
                zoneName = el.attrib['zone']
                # If a ZoneEffect object has already been
                # assigned to this combination of production type and zone,
                # retrieve it; otherwise, create a new one.
                try:
                    assignment = ZoneEffectAssignment.objects.get(
                        zone__name=zoneName,
                        production_type__name=typeName
                    )
                    effect = assignment.effect
                except ZoneEffectAssignment.DoesNotExist:
                    effect = ZoneEffect(name = zoneName + ' effect on ' + typeName)
                    effect.save()
                    assignment = ZoneEffectAssignment(
                        zone = Zone.objects.get( name=zoneName ),
                        production_type = ProductionType.objects.get( name=typeName ),
                        effect = effect
                    )
                    assignment.save()
                effect.cost_of_surveillance_per_animal_day = surveillance
                effect.save()
        # end of loop over production types covered by this <economic-model> element
    # end of loop over <economic-model> elements

    return # from readParameters


def import_naadsm_xml(populationFileName, parameterFileName, saveIterationOutputsForUnits=True):
    """ Load activeSession with the contents of 2 XML files.  This can be saved normally after the scenario_db is populated.
    Database routing is done through the normal ScenarioCreator/router.py"""
    readPopulation(populationFileName)
    readParameters(parameterFileName, saveIterationOutputsForUnits)
