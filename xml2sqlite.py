#!/usr/bin/env python
"""This script reads an XML parameters file and creates the equivalent
database.  It was written primarily for migrating the automated test suite,
but it can also serve as an example for creating a SpreadModel parameter file
programmatically.

This script avoids direct SQL manipulation and instead uses the models.py file
defined for the SpreadModel project for all object creation."""



import sys
from django.conf import settings
from django.core.management import call_command
import xml.etree.ElementTree as ET
import warnings



def getProductionTypes( xml, attributeName, allowedNames ):
	if attributeName not in xml.attrib:
		types = allowedNames
	else:
		text = xml.attrib[attributeName]
		if text == '':
			types = allowedNames
		else:
			types = text.split(',')
	return types



def getPdf( xml ):
	"""Returns a ProbabilityFunction object corresponding to the XML."""
	assert isinstance( xml, ET.Element )
	firstChild = list( xml )[0]
	if firstChild.tag == 'probability-density-function':
		# New style
		name = firstChild.attrib['name']
		firstChild = list( firstChild )[0]
		# Now "firstChild" is the PDF element
	else:
		name = ''
	pdfType = firstChild.tag

	args = {'equation_type': pdfType.capitalize(), 'name': name}

	if pdfType == 'beta-pert':
		args['equation_type'] = 'BetaPERT'
		args['min'] = float( firstChild.find( './min' ).text )
		args['mode'] = float( firstChild.find( './mode' ).text )
		args['max'] = float( firstChild.find( './max' ).text )
	elif pdfType == 'gamma':
		args['alpha'] = float( firstChild.find( './alpha' ).text )
		args['beta'] = float( firstChild.find( './beta' ).text )
	elif pdfType == 'inverse-gaussian':
		args['equation_type'] = 'Inverse Gaussian'
		args['mean'] = float( firstChild.find( './mu' ).text )
		args['shape'] = float( firstChild.find( './lambda' ).text )		
	elif pdfType == 'point':
		args['mode'] = float( firstChild.text )
	elif pdfType == 'triangular':
		args['min'] = float( firstChild.find( './a' ).text )
		args['mode'] = float( firstChild.find( './c' ).text )
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



def getRelChart( xml ):
	"""Returns a RelationalFunction object corresponding to the XML."""
	assert isinstance( xml, ET.Element )
	firstChild = list( xml )[0]
	if firstChild.tag == 'relational-function':
		# New style
		name = firstChild.attrib['name']
		relChart = RelationalFunction( name=name )
		relChart.save()
		for xyPair in firstChild.findall( './value' ):
			point = RelationalPoint(
			  relational_function = relChart,
			  x = float( xyPair.find( './x' ).text ),
			  y = float( xyPair.find( './y' ).text )
			)
			point.save()
	else:
		# Old style
		relChart = RelationalFunction( name='' )
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
	return (xml.text.lower() in ('1', 'y', 'yes', 't', 'true'))



def main():
	# Make sure the database has all the correct tables.
	call_command('syncdb', verbosity=0)

	# sys.stdin is implicitly treated as having whatever encoding is returned
	# by locale.getpreferredencoding(). That can cause problems: for example,
	# if locale.getpreferredencoding() returns 'UTF-8' and the XML file we are
	# reading is ISO-8859-1, then reads from sys.stdin will fail (even if the
	# XML file properly declares its encoding). Using sys.stdin.detach() makes
	# the input stream get treated as binary, and then it's up to ET.parse() to
	# figure out the XML file's encoding.
	xml = ET.parse( sys.stdin.detach() ).getroot()

	useEconomic = (xml.find( './/economic-model' ) != None)
	scenario = Scenario(
	  description = xml.find( './description' ).text
	)
	scenario.save()

	if xml.find( './/state-table-writer' ) != None:
		statesFile = '-'
	else:
		statesFile = None
	if xml.find( './exit-condition/first-detection' ) != None:
		earlyExitCondition = 'first-detection'
	elif xml.find( './exit-condition/disease-end' ) != None:
		earlyExitCondition = 'disease-end'	
	else:
		earlyExitCondition = ''
	outputSettings = OutputSettings(
      iterations = int( xml.find( './num-runs' ).text ),
      days = int( xml.find( './num-days' ).text ),
      stop_criteria = earlyExitCondition,
      daily_states_filename = statesFile,
      cost_track_zone_surveillance = (xml.find( './/economic-model/surveillance' ) != None),
	  cost_track_vaccination = (xml.find( './/economic-model/vaccination' ) != None),
	  cost_track_destruction = (xml.find( './/economic-model/euthanasia' ) != None)
    )
	outputSettings.save()

	# Gather the production type names into a set.
	productionTypeNames = set()
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
	for name in productionTypeNames:
		productionType = ProductionType( name=name )
		productionType.save()

	useAirborneExponentialDecay = (xml.find( './/airborne-spread-exponential-model' ) != None)
	disease = Disease(
	  name='',
	  include_airborne_spread = (xml.find( './/airborne-spread-model' ) != None or xml.find( './/airborne-spread-exponential-model' ) != None),
	  use_airborne_exponential_decay = useAirborneExponentialDecay
	)
	disease.save()

	for el in xml.findall( './/disease-model' ):
		latentPeriod = getPdf( el.find( './latent-period' ) )
		subclinicalPeriod = getPdf( el.find( './infectious-subclinical-period' ) )
		clinicalPeriod = getPdf( el.find( './infectious-clinical-period' ) )
		immunePeriod = getPdf( el.find( './immunity-period' ) )
		if el.find( './prevalence' ) != None:
			prevalence = getRelChart( el.find( './prevalence' ) )
		else:
			prevalence = None
		diseaseProgression = DiseaseProgression(
		  _disease = disease,
		  disease_latent_period = latentPeriod,
		  disease_subclinical_period = subclinicalPeriod,
		  disease_clinical_period = clinicalPeriod,
		  disease_immune_period = immunePeriod,
		  disease_prevalence = prevalence,
		)
		diseaseProgression.save()

		typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
		for typeName in typeNames:
			diseaseProgressionAssignment = DiseaseProgressionAssignment(
			  production_type = ProductionType.objects.get( name=typeName ),
			  progression = diseaseProgression
			)
			diseaseProgressionAssignment.save()
		# end of loop over production types covered by this <disease-model> element
	# end of loop over <disease-model> elements

	# Create a PDF that always returns 0. Will be used as the default when the
	# transport delay PDF is missing.
	zeroDelay = ProbabilityFunction( equation_type='Point', mode=0 )
	zeroDelay.save()

	for el in xml.findall( './/airborne-spread-model' ) + xml.findall( './/airborne-spread-exponential-model' ):
		if useAirborneExponentialDecay:
			maxDistance = 0
		else:
			maxDistance = float( el.find( './max-spread/value' ).text )
		if el.find( './delay' ) != None:
			delay = getPdf( el.find( './delay' ) )
		else:
			delay = zeroDelay
		airborneSpread = AirborneSpread(
		  _disease = disease,
		  max_distance = maxDistance,
		  spread_1km_probability = float( el.find( './prob-spread-1km' ).text ),
		  wind_direction_start = float( el.find( './wind-direction-start/value' ).text ),
		  wind_direction_end = float( el.find( './wind-direction-end/value' ).text ),
		  transport_delay = delay
		)
		airborneSpread.save()

		for fromTypeName in getProductionTypes( el, 'from-production-type', productionTypeNames ):
			for toTypeName in getProductionTypes( el, 'to-production-type', productionTypeNames ):
				pairing = ProductionTypePairTransmission(
				  source_production_type = ProductionType.objects.get( name=fromTypeName ),
				  destination_production_type = ProductionType.objects.get( name=toTypeName ),
				  airborne_spread = airborneSpread
				)
				pairing.save()
			# end of loop over to-production-types covered by this <airborne-spread[-exponential]-model> element
		# end of loop over from-production-types covered by this <airborne-spread[-exponential]-model> element
	# end of loop over <airborne-spread[-exponential]-model> elements

	for el in xml.findall( './/zone-model' ):
		name = ( el.find( './name' ).text )
		radius = float( el.find( './radius/value' ).text )

		zone = Zone( zone_description=name, zone_radius=radius )
		zone.save()
	# end of loop over <zone-model> elements

	for el in xml.findall( './/contact-spread-model' ):
		if 'zone' in el.attrib:
			continue
		fixedRate = (el.find( './fixed-movement-rate' ) != None)
		if fixedRate:
			contactRate = float( el.find( './fixed-movement-rate/value' ).text )
		else:
			contactRate = float( el.find( './movement-rate/value' ).text )
		distance = getPdf( el.find( './distance' ) )
		if el.find( './delay' ) != None:
			delay = getPdf( el.find( './delay' ) )
		else:
			delay = zeroDelay
		probInfect = float( el.find( './prob-infect' ).text )
		try:
			latentCanInfect = getBool( el.find( './latent-units-can-infect' ) )
		except AttributeError:
			latentCanInfect = True # default
		try:
			subclinicalCanInfect = getBool( el.find( './subclinical-units-can-infect' ) )
		except AttributeError:
			subclinicalCanInfect = True # default
		movementControl = getRelChart( el.find( './movement-control' ) )

		if el.attrib['contact-type'] == 'direct':
			contactSpreadModel = DirectSpread(
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
		elif el.attrib['contact-type'] == 'indirect':
			contactSpreadModel = IndirectSpread(
			  _disease = disease,
			  use_fixed_contact_rate = fixedRate,
			  contact_rate = contactRate,
			  movement_control = movementControl,
			  distance_distribution = distance,
			  transport_delay = delay,
			  infection_probability = probInfect,
			  subclinical_animals_can_infect_others = subclinicalCanInfect
			)
		else:
			assert False
		contactSpreadModel.save()

		for fromTypeName in getProductionTypes( el, 'from-production-type', productionTypeNames ):
			for toTypeName in getProductionTypes( el, 'to-production-type', productionTypeNames ):
				pairing, created = ProductionTypePairTransmission.objects.get_or_create(
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
		movementControl = getRelChart( el.find( './movement-control' ) )

		for fromTypeName in fromTypeNames:
			effect, created = ZoneEffectOnProductionType.objects.get_or_create(
			  zone = Zone.objects.get( zone_description=zoneName ),
			  production_type = ProductionType.objects.get( name=fromTypeName )
			)
			if contactType == 'direct' or contactType == 'both':
				effect.zone_direct_movement = movementControl
			if contactType == 'indirect' or contactType == 'both':
				effect.zone_indirect_movement = movementControl
			effect.save()
		# end of loop over from-production-types covered by this <contact-spread-model> element
	# end of loop over <contact-spread-model> elements with a "zone" attribute

	plan = None
	useDetection = (xml.find( './/detection-model' ) != None)
	useTracing = (
	  (xml.find( './/trace-model' ) != None)
	  or (xml.find( './/trace-back-destruction-model' ) != None)
	)
	useVaccination = (
	  (xml.find( './/vaccine-model' ) != None)
	  or (xml.find( './/ring-vaccination-model' ) != None)
	)
	useDestruction = (
	  (xml.find( './/basic-destruction-model' ) != None)
	  or (xml.find( './/trace-destruction-model' ) != None)
	  or (xml.find( './/trace-back-destruction-model' ) != None)
	  or (xml.find( './/ring-destruction-model' ) != None)
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
			multiplier = float( el.find( './zone-prob-multiplier' ).text )
		else:
			observing = getRelChart( el.find( './prob-report-vs-time-clinical' ) )
			reporting = getRelChart( el.find( './prob-report-vs-time-since-outbreak' ) )

		typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
		for typeName in typeNames:
			if 'zone' in el.attrib:
				zoneName = el.attrib['zone']
				effect, created = ZoneEffectOnProductionType.objects.get_or_create(
				  zone = Zone.objects.get( zone_description=zoneName ),
				  production_type = ProductionType.objects.get( name=typeName )
				)
				effect.zone_detection_multiplier = multiplier
				effect.save()
			else:
				protocol = ControlProtocol(
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
		if el.find( './trace-delay' ) != None:
			traceDelay = getPdf( el.find( './trace-delay' ) )
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
		delay = getPdf( el.find( './delay' ) )
		typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
		for typeName in typeNames:
			# If a ControlProtocol object has already been assigned to this
			# production type, retrieve it; otherwise, create a new one.
			try:
				assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
				protocol = assignment.control_protocol
			except ProtocolAssignment.DoesNotExist:
				protocol = ControlProtocol(
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
		immunityPeriod = getPdf( el.find( './immunity-period' ) )

		typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
		for typeName in typeNames:
			# If a ControlProtocol object has already been assigned to this
			# production type, retrieve it; otherwise, create a new one.
			try:
				assignment = ProtocolAssignment.objects.get( production_type__name=typeName )
				protocol = assignment.control_protocol
			except ProtocolAssignment.DoesNotExist:
				protocol = ControlProtocol(
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
			plan.destruction_capacity = getRelChart( el.find( './destruction-capacity' ) )
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
			plan.vaccination_capacity = getRelChart( el.find( './vaccination-capacity' ) )
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
				  test_delay = zeroDelay # placeholder for now, needed because of NOT NULL constraint
				)
				protocol.save()
				assignment = ProtocolAssignment(
				  production_type = ProductionType.objects.get( name=typeName ),
				  control_protocol = protocol
				)
				assignment.save()
			protocol.use_cost_accounting = True
			if vaccinationFixed != None:
				protocol.cost_of_vaccination_setup_per_unit = vaccinationFixed
			if vaccinationBase != None:
				protocol.cost_of_vaccination_baseline_per_animal = vaccinationBase
			if vaccinationExtra != None:
				protocol.cost_of_vaccination_additional_per_animal = vaccinationExtra
			if baselineCapacity != None:
				protocol.vaccination_demand_threshold = baselineCapacity
			if appraisal != None:
				protocol.cost_of_destruction_appraisal_per_unit = appraisal
			if euthanasia != None:
				protocol.cost_of_euthanasia_per_animal = euthanasia
			if indemnification != None:
				protocol.cost_of_indemnification_per_animal = indemnification
			if disposal != None:
				protocol.cost_of_carcass_disposal_per_animal = disposal
			if cleaning != None:
				protocol.cost_of_destruction_cleaning_per_unit = cleaning
			protocol.save()

			if 'zone' in el.attrib and surveillance != None:
				zoneName = el.attrib['zone']
				# If a ZoneEffectOnProductionType object has already been
				# assigned to this combination of production type and zone,
				# retrieve it; otherwise, create a new one.
				effect, created = ZoneEffectOnProductionType.objects.get_or_create(
				  zone = Zone.objects.get( zone_description=zoneName ),
				  production_type = ProductionType.objects.get( name=typeName )
				)
				effect.cost_of_surveillance_per_animal_day = surveillance
				effect.save()
		# end of loop over production types covered by this <economic-model> element
	# end of loop over <economic-model> elements



if __name__ == "__main__":
	# The reading of the database file name is done here instead of in main()
	# because "settings" must be filled in before models is imported, and
	# import statements are allowed only at the top level in Python, not inside
	# functions.
	dbName = sys.argv[1]
	settings.configure(
	  INSTALLED_APPS = ('ScenarioCreator',),
	  DATABASES = {
	    'default': {
	      'NAME': dbName,
	      'ENGINE': 'django.db.backends.sqlite3',
	      'USER': 'user',
	      'PASSWORD': '1',
	    }
	  }
	)
	from django.db import models
	from ScenarioCreator.models import *
	main()
