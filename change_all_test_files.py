#!/usr/bin/python
"""This script turns all of the automated test suite files (in XML format) into
the new SQLite3 format.

Call it as:
python3.3 change_all_test_files.py CEngine/modules/test/"""



import sys
import os
import glob
import io
import xml.etree.ElementTree as ET
import subprocess



def main():
	args = sys.argv[1:]
	assert len( args) >= 1	
	dir = args.pop()
	for subdir in glob.glob( os.path.join( dir, 'module.*' ) ):
		print( subdir )

		testDefinitionFile = os.path.join( subdir, 'all.xml' )
		# The xml files in the various directories of tests lack an XML
		# declaration at the top and a closing tag at the bottom. This is
		# because they are intended to be concatenated. So we need to add the
		# XML declaration and closing tag here in order to make the file parse
		# as valid XML.
		xml = io.StringIO()
		xml.write( '<?xml version="1.0" ?>\n' )
		xml.write( '<tests>\n' )
		xml.write( open( testDefinitionFile ).read() )
		xml.write( '</tests>\n' )

		xml.seek (0 )
		doc = ET.parse( xml ).getroot()

		for el in doc.findall( './/deterministic-test' ) \
		  + doc.findall( './/variable-test' ) \
		  + doc.findall( './/stochastic-test' ) \
		  + doc.findall( './/stochastic-variable-test' ):
			populationFileName = el.find( './population-file' ).text
			parameterFileName = el.find( './parameter-file' ).text
			dbFileName = parameterFileName + '_' + populationFileName + os.extsep + 'sqlite3'

			populationFilePath = os.path.join( dir, populationFileName + os.extsep + 'xml' )
			parameterFilePath = os.path.join( subdir, parameterFileName + os.extsep + 'xml' )
			dbFilePath = os.path.join( subdir, dbFileName )

			# Newer tests (created after the change from XML format to SQLite
			# format) will just have a .sqlite3 file, and no .xml files. For
			# those, we don't have to do anything.
			if os.path.isfile( populationFilePath ) and os.path.isfile( parameterFilePath ):
				# Remove any existing .sqlite3 file which may have been created
				# by a previous version of this script.
				if os.path.isfile( dbFilePath ):
					os.remove( dbFilePath )

				cmd = ['python3.4', 'xml2sqlite.py', populationFilePath,
				  parameterFilePath, dbFilePath ]
				print( ' '.join(cmd) )
				subprocess.check_call(cmd)
			# end of case where XML files need to be converted to SQLite
		# end of loop over tests in the test description file
	# end of loop over directories containing tests



if __name__ == "__main__":
	main()
