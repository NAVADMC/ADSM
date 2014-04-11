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

	if pdfType == 'point':
		args['mode'] = float( firstChild.text )
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

	xml = ET.parse( sys.stdin ).getroot()

	usePrevalence = (xml.find( './/disease-model/prevalence' ) != None)
	useAirborneExponentialDecay = (xml.find( './/airborne-spread-exponential-model' ) != None)
	scenario = Scenario(
	  description = xml.find( './description' ).text,
	  include_airborne_spread = (xml.find( './/airborne-spread-model' ) != None or xml.find( './/airborne-spread-exponential-model' ) != None),
	  use_airborne_exponential_decay = useAirborneExponentialDecay,
	  use_within_unit_prevalence = usePrevalence
	)
	scenario.save()

	if xml.find( './/state-table-writer' ) != None:
		statesFile = '-'
	else:
		statesFile = None
	outputSettings = OutputSettings(
      iterations = int( xml.find( './num-runs' ).text ),
      days = int( xml.find( './num-days' ).text ),
      daily_states_filename = statesFile
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

	disease = Disease( name='' )
	disease.save()

	for el in xml.findall( './/disease-model' ):
		latentPeriod = getPdf( el.find( './latent-period' ) )
		subclinicalPeriod = getPdf( el.find( './infectious-subclinical-period' ) )
		clinicalPeriod = getPdf( el.find( './infectious-clinical-period' ) )
		immunePeriod = getPdf( el.find( './immunity-period' ) )
		if usePrevalence:
			prevalence = getRelChart( el.find( './prevalence' ) )
		else:
			prevalence = None
		diseaseReaction = DiseaseReaction(
		  _disease = disease,
		  disease_latent_period = latentPeriod,
		  disease_subclinical_period = subclinicalPeriod,
		  disease_clinical_period = clinicalPeriod,
		  disease_immune_period = immunePeriod,
		  disease_prevalence = prevalence
		)
		diseaseReaction.save()

		typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
		for typeName in typeNames:
			diseaseReactionAssignment = DiseaseReactionAssignment(
			  production_type = ProductionType.objects.get( name=typeName ),
			  reaction = diseaseReaction
			)
			diseaseReactionAssignment.save()
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
		airborneSpreadModel = AirborneSpreadModel(
		  _disease = disease,
		  max_distance = maxDistance,
		  spread_1km_probability = float( el.find( './prob-spread-1km' ).text ),
		  wind_direction_start = float( el.find( './wind-direction-start/value' ).text ),
		  wind_direction_end = float( el.find( './wind-direction-end/value' ).text ),
		  transport_delay = delay
		)
		airborneSpreadModel.save()

		for fromTypeName in getProductionTypes( el, 'from-production-type', productionTypeNames ):
			for toTypeName in getProductionTypes( el, 'to-production-type', productionTypeNames ):
				pairing = ProductionTypePairTransmission(
				  source_production_type = ProductionType.objects.get( name=fromTypeName ),
				  destination_production_type = ProductionType.objects.get( name=toTypeName ),
				  airborne_contact_spread_model = airborneSpreadModel
				)
				pairing.save()
			# end of loop over to-production-types covered by this <airborne-spread[-exponential]-model> element
		# end of loop over from-production-types covered by this <airborne-spread[-exponential]-model> element
	# end of loop over <airborne-spread[-exponential]-model> elements

	for el in xml.findall( './/contact-spread-model' ):
		if 'zone' in el.attrib:
			continue
		fixedRate = (el.find( './fixed-movement-rate' ) != None)
		if fixedRate:
			contactRate = float( el.find( './fixed-movement-rate/value' ).text )
		else:
			contactRate = float( el.find( './movement-rate/value' ).text )
		distance = getPdf( el.find( './distance' ) )
		delay = getPdf( el.find( './delay' ) )
		probInfect = float( el.find( './prob-infect' ).text )
		try:
			subclinicalCanInfect = getBool( el.find( './subclinical-units-can-infect' ) )
		except AttributeError:
			subclinicalCanInfect = True # default
		movementControl = getRelChart( el.find( './movement-control' ) )

		if el.attrib['contact-type'] == 'direct':
			contactSpreadModel = DirectSpreadModel(
			  _disease = disease,
			  use_fixed_contact_rate = fixedRate,
			  contact_rate = contactRate,
			  movement_control = movementControl,
			  distance_distribution = distance,
			  transport_delay = delay,
			  infection_probability = probInfect,
			  latent_animals_can_infect_others = getBool( el.find( './latent-units-can-infect' ) ),
			  subclinical_animals_can_infect_others = subclinicalCanInfect
			)
		elif el.attrib['contact-type'] == 'indirect':
			contactSpreadModel = IndirectSpreadModel(
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
				# If a ProductionTypePairTransmission object has already been
				# assigned to this from/to pairing of production types,
				# retrieve it; otherwise, create a new one.
				try:
					pairing = ProductionTypePairTransmission.objects.get(
					  source_production_type__name=fromTypeName,
					  destination_production_type__name=toTypeName
					)
				except ProductionTypePairTransmission.DoesNotExist:
					pairing = ProductionTypePairTransmission(
					  source_production_type = ProductionType.objects.get( name=fromTypeName ),
					  destination_production_type = ProductionType.objects.get( name=toTypeName )
					)
					pairing.save()
				if el.attrib['contact-type'] == 'direct':
					pairing.direct_contact_spread_model = contactSpreadModel
				else:
					pairing.indirect_contact_spread_model = contactSpreadModel
				pairing.save()
			# end of loop over to-production-types covered by this <contact-spread-model> element
		# end of loop over from-production-types covered by this <contact-spread-model> element		
	# end of loop over <contact-spread-model> elements

	plan = None
	useDetection = (xml.find( './/detection-model' ) != None)
	useTracing = (
	  (xml.find( './/trace-model' ) != None)
	  or (xml.find( './/trace-back-destruction-model' ) != None)
	)
	useVaccination = (xml.find( './/ring-vaccination-model' ) != None)
	useDestruction = (
	  (xml.find( './/basic-destruction-model' ) != None)
	  or (xml.find( './/trace-destruction-model' ) != None)
	  or (xml.find( './/trace-back-destruction-model' ) != None)
	  or (xml.find( './/ring-destruction-model' ) != None)
	)

	if useDetection or useTracing or useDestruction:
		plan = ControlMasterPlan(
		  _include_detection = useDetection,
		  _include_tracing = useTracing,
		  _include_vaccination = useVaccination,
		  _include_destruction = useDestruction
		)
		plan.save()

	for el in xml.findall( './/detection-model' ):
		observing = getRelChart( el.find( './prob-report-vs-time-clinical' ) )
		reporting = getRelChart( el.find( './prob-report-vs-time-since-outbreak' ) )

		typeNames = getProductionTypes( el, 'production-type', productionTypeNames )
		for typeName in typeNames:
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
			protocol.trace_result_delay = zeroDelay
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
			protocol.save()
			vaccinationProductionTypeOrder.append( (priority, toTypeName) )
			productionTypesThatAreVaccinated.add( toTypeName )
		# end of loop over to-production-types covered by this <ring-vaccination-model> element
	# end of loop over <ring-vaccination-model> elements

	if productionTypesThatAreVaccinated != productionTypesWithVaccineEffectsDefined:
		raise Exception( 'mismatch between production types that are vaccinated and production types with vaccine effects defined' )
		sys.exit()

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
				protocoo.indirect_trace_period = tracePeriod
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
