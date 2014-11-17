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



def main():
	args = sys.argv[1:]
	assert len( args) >= 1	
	dir = args.pop()
	for subdir in glob.glob( os.path.join( dir, 'module.*' ) ):
		print( subdir )
		# Remove all .sqlite3 files currently in the directory of tests.
		for oldSqliteFile in glob.glob( os.path.join( subdir, '*.sqlite3' ) ):
			os.remove( oldSqliteFile )

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
			cmd = 'python3.3 xml2sqlite.py ' \
			  + os.path.join( dir, populationFileName + '.xml' ) \
			  + ' ' + os.path.join( subdir, parameterFileName + '.xml' ) \
			  + ' ' + os.path.join( os.path.pardir, subdir, parameterFileName + '_' + populationFileName + '.sqlite3' )
			print( cmd )
			os.system( cmd )
		# end of loop over tests in the test description file
	# end of loop over directories containing tests



if __name__ == "__main__":
	main()
