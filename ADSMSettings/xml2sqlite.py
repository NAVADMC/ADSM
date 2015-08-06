"""This module reads an XML parameters file and creates the equivalent
database.  It was written primarily for migrating the automated test suite,
but it can also serve as an example for creating a ADSM parameter file
programmatically.

This script avoids direct SQL manipulation and instead uses the models.py file
defined for the ADSM project for all object creation."""

import xml.etree.ElementTree as ET
import warnings
from pyproj import Proj
from math import exp, sqrt

from ScenarioCreator.models import *
from Results.models import *

CREATE_AT_A_TIME = 500 # for bulk object creation


def create_no_duplicates(ModelClass, suggested_name, **kwargs):
    instance, created = ModelClass.objects.get_or_create(**kwargs)
    if suggested_name is not None:  # TODO: use Django _meta to check for a field called "name"
        if created:
            instance.name = suggested_name
        else:
            if instance.name != suggested_name:
                instance.name += ',' + suggested_name
        instance.save()
    return instance, created


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


def getProductionTypeObjects( xml, attributeName, allowedNames ):
    names = getProductionTypes(xml, attributeName, allowedNames)
    return [pt for pt in ProductionType.objects.all() if pt.name in names]


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

    args = {'equation_type': pdfType.capitalize(), }

    if pdfType == 'beta':
        args['alpha'] = float( required_text(firstChild, './alpha' ) )
        args['alpha2'] = float( required_text(firstChild, './beta' ) )
        args['min'] = float( required_text(firstChild, './location' ) )
        args['max'] = float( required_text(firstChild, './scale' ) )
    elif pdfType == 'beta-pert':
        args['equation_type'] = 'BetaPERT'
        args['min'] = float( required_text(firstChild, './min' ) )
        args['mode'] = float( required_text(firstChild, './mode' ) )
        args['max'] = float( required_text(firstChild, './max' ) )
    elif pdfType == 'binomial':
        args['s'] = float( required_text(firstChild, './n' ) )
        args['p'] = float( required_text(firstChild, './p' ) )
    elif pdfType == 'discrete-uniform':
        args['equation_type'] = 'Discrete Uniform'
        args['min'] = float( required_text(firstChild, './min' ) )
        args['max'] = float( required_text(firstChild, './max' ) )
    elif pdfType == 'exponential':
        args['mean'] = float( required_text(firstChild, './mean' ) )
    elif pdfType == 'gamma':
        args['alpha'] = float( required_text(firstChild, './alpha' ) )
        args['beta'] = float( required_text(firstChild, './beta' ) )
    elif pdfType == 'gaussian':
        args['mean'] = float( required_text(firstChild, './mean' ) )
        args['std_dev'] = float( required_text(firstChild, './stddev' ) )
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
        args['n'] = float( required_text(firstChild, './n' ) )
        args['d'] = float( required_text(firstChild, './d' ) )
        args['m'] = float( required_text(firstChild, './m' ) )
    elif pdfType == 'inverse-gaussian':
        args['equation_type'] = 'Inverse Gaussian'
        args['mean'] = float( required_text(firstChild, './mu' ) )
        args['shape'] = float( required_text(firstChild, './lambda' ) )
    elif pdfType == 'logistic':
        args['location'] = float( required_text(firstChild, './location' ) )
        args['scale'] = float( required_text(firstChild, './scale' ) )
    elif pdfType == 'loglogistic':
        args['equation_type'] = 'LogLogistic'
        args['location'] = float( required_text(firstChild, './location' ) )
        args['scale'] = float( required_text(firstChild, './scale' ) )
        args['shape'] = float( required_text(firstChild, './shape' ) )
    elif pdfType == 'lognormal':
        # Lognormal is represented in the XML as "zeta" and "sigma" as used in
    	# the GNU Scientific Library docs. Convert to mean and standard
    	# deviation.
        zeta = float( required_text(firstChild, './zeta' ) )
        sigma = float( required_text(firstChild, './sigma' ) )
        sigma_sq = sigma*sigma
        args['mean'] = exp( zeta + sigma_sq/2 )
        variance = exp( 2*zeta + sigma_sq ) * (exp(sigma_sq) - 1)
        args['std_dev'] = sqrt(variance)
    elif pdfType == 'negative-binomial':
        args['equation_type'] = 'Negative Binomial'
        args['s'] = float( required_text(firstChild, './s' ) )
        args['p'] = float( required_text(firstChild, './p' ) )
    elif pdfType == 'pareto':
        args['theta'] = float( required_text(firstChild, './theta' ) )
        args['a'] = float( required_text(firstChild, './a' ) )
    elif pdfType == 'pearson5':
        args['equation_type'] = 'Pearson 5'
        args['alpha'] = float( required_text(firstChild, './alpha' ) )
        args['beta'] = float( required_text(firstChild, './beta' ) )
    elif pdfType == 'piecewise':
        graph = RelationalFunction( name=name + ' piecewise data' )
        graph.save()
        # NAADSM had both "old" and "new" style piecewise PDFs. The old style
        # contained a sequence of <value> <p> <value> <p>... elements. The new
        # style contained a sequence of <value> elements each containing an <x>
        # and a <p> element.
        newStyle = firstChild.find( './/x' ) is not None
        if newStyle:
            for value in firstChild.findall( './value' ):
                x = float( required_text(value, './x' ) )
                p = float( required_text(value, './p' ) )
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
        args['mean'] = float( required_text(firstChild, './mean' ) )
    elif pdfType == 'triangular':
        args['min'] = float( required_text(firstChild, './a' ) )
        args['mode'] = float( required_text(firstChild, './c' ) )
        args['max'] = float( required_text(firstChild, './b' ) )
    elif pdfType == 'uniform':
        args['min'] = float( required_text(firstChild, './a' ) )
        args['max'] = float( required_text(firstChild, './b' ) )
    elif pdfType == 'weibull':
        args['alpha'] = float( required_text(firstChild, './alpha' ) )
        args['beta'] = float( required_text(firstChild, './beta' ) )
    else:
        raise NotImplementedError( pdfType )

    pdf, created = create_no_duplicates(ProbabilityFunction, name, **args)
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
                    x = float( required_text(xyPair, './x' ) ),
                    y = float( required_text(xyPair, './y' ) )
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
                x = float( required_text(xyPair, './x' ) )
                y = float( required_text(xyPair, './y' ) )
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
                        x = float( required_text(xyPair, './x' ) ),
                        y = float( required_text(xyPair, './y' ) )
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
    print("Reading population file: ", populationFileName)
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
            description = 'id=' + description.text
        typeName = required_text(el, './production-type' )
        productionType = ProductionType.objects.get_or_create( name=typeName )[0]
        size = int( required_text(el, './size' ) )
        if not projection:
            lat = float( required_text(el, './location/latitude' ) )
            long = float( required_text(el, './location/longitude' ) )
        else:
            x = float( required_text(el, './location/x' ) )
            y = float( required_text(el, './location/y' ) )
            long, lat = projection( x, y, inverse=True )

        state = required_text(el, './status' )
        if state not in stateCodes.values():
            try:
                state = stateCodes[state]
            except KeyError:
                state = Unit._meta.get_field('initial_state').get_default()
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


def required_text(element, tag):
    try:
        child = element.find(tag)
        return child.text
    except (AttributeError, Exception) as e:
        raise AttributeError("Missing required value " + str(tag) + " in " + str(element).replace('<',''))


def readParameters( parameterFileName, saveIterationOutputsForUnits ):
    print("Reading parameters file:", parameterFileName)
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
    print("Done reading parameters file.  Constructing New Scenario...")

    Scenario.objects.get_or_create(description = required_text(xml,  './description' ))

    if xml.find( './exit-condition/first-detection' ) is not None:
        earlyExitCondition = 'first-detection'
    elif xml.find( './exit-condition/disease-end' ) is not None:
        earlyExitCondition = 'disease-end'
    else:
        earlyExitCondition = ''
    outputSettings = OutputSettings(
        iterations = int( required_text(xml, './num-runs' ) ),
        days = int( required_text(xml, './num-days' ) ),
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
        use_airborne_exponential_decay = useAirborneExponentialDecay,
        use_within_unit_prevalence = False
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
            disease.use_within_unit_prevalence = True
            disease.save()
        else:
            prevalence = None

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            diseaseProgression, created = create_no_duplicates(DiseaseProgression, typeName + ' Progression',  
                _disease = disease,
                disease_latent_period = latentPeriod,
                disease_subclinical_period = subclinicalPeriod,
                disease_clinical_period = clinicalPeriod,
                disease_immune_period = immunePeriod,
                disease_prevalence = prevalence,
            )

            DiseaseProgressionAssignment.objects.get_or_create(
                production_type = ProductionType.objects.get( name=typeName ),
                progression = diseaseProgression
            )
        # end of loop over production types covered by this <disease-model> element
    # end of loop over <disease-model> elements

    for el in xml.findall( './/airborne-spread-model' ) + xml.findall( './/airborne-spread-exponential-model' ):
        if useAirborneExponentialDecay:
            maxDistance = 0
        else:
            maxDistance = float( required_text(el, './max-spread/value' ) )
        if el.find( './delay' ) is not None:
            delay = getPdf( el.find( './delay' ), pdfNameSequence )
        else:
            delay = None

        for fromTypeName in getProductionTypes( el, 'from-production-type', productionTypeNames ):
            for toTypeName in getProductionTypes( el, 'to-production-type', productionTypeNames ):
                airborneSpread, created = create_no_duplicates(AirborneSpread, 'Airborne %s -> %s' % (fromTypeName, toTypeName),
                  _disease = disease,
                  max_distance = maxDistance,
                  spread_1km_probability = float( required_text(el, './prob-spread-1km' ) ),
                  exposure_direction_start = float( required_text(el, './wind-direction-start/value' ) ),
                  exposure_direction_end = float( required_text(el, './wind-direction-end/value' ) ),
                  transport_delay = delay
                )
                airborneSpread.save()

                pairing, created = create_no_duplicates(DiseaseSpreadAssignment, suggested_name=None,
                  source_production_type = ProductionType.objects.get( name=fromTypeName ),
                  destination_production_type = ProductionType.objects.get( name=toTypeName )
                )
                pairing.airborne_spread = airborneSpread  # assign the airborneSpread in addition to the other two spreads
                pairing.save()
            # end of loop over to-production-types covered by this <airborne-spread[-exponential]-model> element
        # end of loop over from-production-types covered by this <airborne-spread[-exponential]-model> element
    # end of loop over <airborne-spread[-exponential]-model> elements

    for el in xml.findall( './/zone-model' ):
        name = required_text(el, './name' )
        radius = float( required_text(el, './radius/value' ) )
        if radius > 0:
            zone, created = create_no_duplicates(Zone, suggested_name=name, radius=radius )
    # end of loop over <zone-model> elements

    for el in xml.findall( './/contact-spread-model' ):
        if 'zone' in el.attrib:
            continue
        fixedRate = (el.find( './fixed-movement-rate' ) is not None)
        if fixedRate:
            contactRate = float( required_text(el, './fixed-movement-rate/value' ) )
        else:
            contactRate = float( required_text(el, './movement-rate/value' ) )
        distance = getPdf( el.find( './distance' ), pdfNameSequence )
        if el.find( './delay' ) is not None:
            delay = getPdf( el.find( './delay' ), pdfNameSequence )
        else:
            delay = None
        if el.find( './prob-infect' ) is not None:
            probInfect = float( required_text(el, './prob-infect' ) )
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
                    contactSpreadModel, created = create_no_duplicates(DirectSpread, 'Direct %s -> %s' % (fromTypeName, toTypeName), 
                        _disease = disease,
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
                    contactSpreadModel, created = create_no_duplicates(IndirectSpread, 'Indirect %s -> %s' % (fromTypeName, toTypeName),
                        _disease = disease,
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

        production_types = getProductionTypeObjects( el, 'from-production-type', productionTypeNames )
        if 'contact-type' in el.attrib:
            contactType = el.attrib['contact-type']
            assert (contactType == 'direct' or contactType == 'indirect')
        else:
            contactType = 'both'
        zone = Zone.objects.get(name=el.attrib['zone'])
        movementControl = getRelChart( el.find( './movement-control' ), relChartNameSequence )

        for fromType in production_types:
            # If a ZoneEffect object has already been assigned to this
            # combination of zone and production type, retrieve it; otherwise,
            # create a new one.
            assignment, created = create_no_duplicates(ZoneEffectAssignment, suggested_name=None,
                                                       zone=zone,
                                                       production_type=fromType)
            effect = assignment.effect
            if effect is None:
                effect = ZoneEffect(name = zone.name + ' effect on ' + fromType.name)
                effect.save()  # TODO: could be simplified further
                assignment.effect = effect
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


    for el in xml.findall( './/detection-model' ):
        # <detection-model> elements come in 2 forms. The first form, with a
        # production-type attribute, specifies the probability of observing
        # clinical signs of disease and the probability of reporting those
        # signs. The second form, with a production-type attribute and a zone
        # attribute, specifies a multiplier to use on the probability of
        # observing clinical signs when inside a zone.
        if 'zone' in el.attrib:
            multiplier = float( required_text(el, './zone-prob-multiplier' ) )
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
                    detection_probability_report_vs_first_detection = reporting
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
        traceSuccess = float( required_text(el, './trace-success' ) )
        if el.find( './trace-delay' ) is not None:
            traceDelay = getPdf( el.find( './trace-delay' ), pdfNameSequence )
        else:
            traceDelay = None # default

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False
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
        tracePeriod = int( required_text(el, './trace-period/value' ) )

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False
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
        detectionMultiplier = float( required_text(el, './detection-multiplier' ) )
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
                    use_detection = False
                )
                protocol.save()
                assignment = ProtocolAssignment(
                    production_type = ProductionType.objects.get( name=typeName ),
                    control_protocol = protocol
                )
                assignment.save()
            protocol.use_exams = True
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
        sensitivity = float( required_text(el, './sensitivity' ) )
        specificity = float( required_text(el, './specificity' ) )
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
                    use_detection = False
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
                    use_detection = False
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
                    use_detection = False
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
        delay = int( required_text(el, './delay/value' ) )
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
                    use_detection = False
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

        radius = float( required_text(el, './radius/value' ) )
        for fromTypeName in fromTypeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=fromTypeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False
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

        priority = int( required_text(el, './priority' ) )
        minTimeBetweenVaccinations = int( required_text(el, './min-time-between-vaccinations/value' ) )
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
                    use_detection = False
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
        tracePeriod = int( required_text(el, './trace-period/value' ) )
        traceSuccess = float( required_text(el, './trace-success' ) )
        for typeName in productionTypeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False
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
            protocol.save()
        # end of loop to enable trace forward/out from all production types

        # Enable destruction of specific production types when identified by
        # trace.
        priority = int( required_text(el, './priority' ) )
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
                        use_detection = False
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
        priority = int( required_text(el, './priority' ) )

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False
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
        priority = int( required_text(el, './priority' ) )

        typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
        for typeName in typeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False
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

        radius = float( required_text(el, './radius/value' ) )
        for fromTypeName in fromTypeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=fromTypeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False
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

        priority = int( required_text(el, './priority' ) )
        for toTypeName in toTypeNames:
            # If a ControlProtocol object has already been assigned to this
            # production type, retrieve it; otherwise, create a new one.
            try:
                assignment = ProtocolAssignment.objects.get( production_type__name=toTypeName )
                protocol = assignment.control_protocol
            except ProtocolAssignment.DoesNotExist:
                protocol = ControlProtocol(
                    use_detection = False
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
            plan.destruction_program_delay = int( required_text(el, './destruction-program-delay/value' ) )
            plan.destruction_capacity = getRelChart( el.find( './destruction-capacity' ), relChartNameSequence )
            try:
                order = required_text(el, './destruction-priority-order' ).strip()
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
                unitsDetectedBeforeTriggeringVaccination = max( 1, int( el.find( './vaccination-program-delay' ).text ))
            except AttributeError:
                unitsDetectedBeforeTriggeringVaccination = 1 # default
            trigger = DiseaseDetection(
                number_of_units = unitsDetectedBeforeTriggeringVaccination
            )
            trigger.save()
            for productionType in ProductionType.objects.all():
                trigger.trigger_group.add( productionType )
            plan.vaccination_capacity = getRelChart( el.find( './vaccination-capacity' ), relChartNameSequence )
            order = required_text(el, './vaccination-priority-order' ).strip()
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
                    use_detection = False
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
    try:
        readPopulation(populationFileName)
    except Exception as e:
        raise ValueError("<p><strong>Bad Population file:</strong> " + str(e) + ".</p>\n <p>Please export a new <strong>Population</strong> XML file from NAADSM 3.2.19</p>")
    try:
        readParameters(parameterFileName, saveIterationOutputsForUnits)
    except Exception as e:
        raise ValueError("<p><strong>Bad Parameters file:</strong> " + str(e) + ".</p>\n <p>Please export a new <strong>Parameters</strong> XML file from NAADSM 3.2.19</p>")

