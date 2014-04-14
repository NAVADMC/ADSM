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



def main():
	# Make sure the database has all the correct tables.
	call_command('syncdb', verbosity=0)

	xml = ET.parse( sys.stdin ).getroot()

	scenario = Scenario(
	  description = xml.find( './description' ).text,
	  include_airborne_spread = (xml.find( './/airborne-spread-model' ) != None or xml.find( './/airborne-spread-exponential-model' ) != None),
	  use_airborne_exponential_decay = (xml.find( './/airborne-spread-exponential-model' ) != None),
	  use_within_unit_prevalence = (xml.find( './/disease-model/prevalence' ) != None)
	)
	scenario.save()

	if xml.find( './/state-table-writer' ) != None:
		statesFile = '"-"'
	else:
		statesFile = 'NULL'
	outputSettings = OutputSettings(
      iterations = int( xml.find( './num-runs' ).text ),
      days = int( xml.find( './num-days' ).text ),
      daily_states_filename = statesFile
    )
	outputSettings.save()

	# Gather the production type names into a set.
	names = set( [el.attrib['production-type'] for el in xml.findall( './/*[@production-type]' )] )
	names.update( set( [el.attrib['to-production-type'] for el in xml.findall( './/*[@to-production-type]' )] ) )
	names.update( set( [el.attrib['from-production-type'] for el in xml.findall( './/*[@from-production-type]' )] ) )
	# If an empty production type attribute appeared anywhere in the XML,
	# ignore that.
	names.remove( '' )
	for name in names:
		productionType = ProductionType( name=name )
		productionType.save()

	disease = Disease( name='' )
	disease.save()



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
