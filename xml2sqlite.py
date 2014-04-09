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



def getProductionTypes( text, allowedNames ):
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
	productionTypeNames = set( [el.attrib['production-type'] for el in xml.findall( './/*[@production-type]' )] )
	productionTypeNames.update( set( [el.attrib['to-production-type'] for el in xml.findall( './/*[@to-production-type]' )] ) )
	productionTypeNames.update( set( [el.attrib['from-production-type'] for el in xml.findall( './/*[@from-production-type]' )] ) )
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

		for productionTypeName in getProductionTypes( el.attrib['production-type'], productionTypeNames ):
			diseaseReactionAssignment = DiseaseReactionAssignment(
			  production_type = ProductionType.objects.get( name=productionTypeName ),
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

		for fromTypeName in getProductionTypes( el.attrib['from-production-type'], productionTypeNames ):
			for toTypeName in getProductionTypes( el.attrib['to-production-type'], productionTypeNames ):
				pairing = ProductionTypePairTransmission(
				  source_production_type = ProductionType.objects.get( name=fromTypeName ),
				  destination_production_type = ProductionType.objects.get( name=toTypeName ),
				  airborne_contact_spread_model = airborneSpreadModel
				)
				pairing.save()
			# end of loop over to-production-types covered by this <airborne-spread[-exponential]-model> element
		# end of loop over from-production-types covered by this <airborne-spread[-exponential]-model> element
	# end of loop over <airborne-spread[-exponential]-model> elements



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
