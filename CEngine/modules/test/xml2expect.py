#!/usr/bin/env python
"""This script converts an XML description of test cases into an Expect
script.

Copyright (C) University of Guelph, 2003-2008

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version."""

__author__ = "Neil Harvey <nharve01@uoguelph.ca>"
__date__ = "December 2003"

import sys
import xml.dom.minidom

OUTPUT_ENCODING = "iso-8859-1" # to match output from the simulator



def getText (element):
	"""Returns the contents of all text children of the given element,
	concatenated, as a string."""
	text = ""
	for node in element.childNodes:
		if node.nodeType == node.TEXT_NODE:
			text += node.data
	return text.strip()



def main ():
	doc = xml.dom.minidom.parse (sys.stdin)
	# Boilerplate at the top of the file.
	print r"""set timeout 3
#
# expectations that clean up in case of error. Note that `$test' is
# a purely local variable.
#
# The first of these is used to match any bad responses, and resynchronise
# things by finding a prompt. The second is a timeout error, and shouldn't
# ever be triggered.
#
expect_after {
	-re "\[^\n\r\]*$prompt$" {
		fail "$test (bad match)"
		if { $verbose > 0 } {
			regexp ".*\r\n(\[^\r\n\]+)(\[\r\n\])+$prompt$" \
						$expect_out(buffer) "" output
			send_user "\tUnmatched output: \"$output\"\n"
		}
	}
	timeout {
		fail "$test (timeout)"
	}
}"""

	state_code = {
	  'S': 'Susceptible',
	  'L': 'Latent',
	  'B': 'InfectiousSubclinical',
	  'C': 'InfectiousClinical',
	  'N': 'NaturallyImmune',
	  'V': 'VaccineImmune',
	  'D': 'Destroyed'
	}

	# Print the deterministic herd-state tests.
	tests = doc.getElementsByTagName ("deterministic-test")
	for test in tests:
		description = getText (test.getElementsByTagName ("description")[0])
		print '\n\n\n#'
		for line in description.split('\n'):
			print '# %s' % line.strip().encode(OUTPUT_ENCODING, "replace")
		print '#'

		parameters = getText (test.getElementsByTagName ("parameter-description")[0])
		for line in parameters.split('\n'):
			print '# %s' % line.strip().encode(OUTPUT_ENCODING, "replace")
		print '#'

		category = getText (test.getElementsByTagName ("category")[0])
		parameterFileName = getText (test.getElementsByTagName ("parameter-file")[0])
		populationFileName = getText (test.getElementsByTagName ("population-file")[0])
		print 'set params "test/module.%s/%s.xml"' % (category, parameterFileName)
		print 'set herds "test/%s.xml"' % (populationFileName)

		table = test.getElementsByTagName ("output")[0]
		print 'set states {'
		for row in table.getElementsByTagName ("tr"):
			print '  {',
			for cell in row.getElementsByTagName ("td"):
				state = getText (cell)
				if state_code.has_key(state):
					state = state_code[state]
				print state,
			print '}'
		print '}'

		shortName = getText (test.getElementsByTagName ("short-name")[0])
		print 'progress_test $params $herds $states "%s"' % shortName

	# Print the stochastic herd-state tests.
	tests = doc.getElementsByTagName ("stochastic-test")
	for test in tests:
		description = getText (test.getElementsByTagName ("description")[0])
		print '\n\n\n#'
		for line in description.split('\n'):
			print '# %s' % line.strip().encode(OUTPUT_ENCODING, "replace")
		print '#'

		parameters = getText (test.getElementsByTagName ("parameter-description")[0])
		for line in parameters.split('\n'):
			print '# %s' % line.strip().encode(OUTPUT_ENCODING, "replace")
		print '#'

		category = getText (test.getElementsByTagName ("category")[0])
		parameterFileName = getText (test.getElementsByTagName ("parameter-file")[0])
		populationFileName = getText (test.getElementsByTagName ("population-file")[0])
		print 'set params "test/module.%s/%s.xml"' % (category, parameterFileName)
		print 'set herds "test/%s.xml"' % (populationFileName)

		tables = test.getElementsByTagName ("output")
		print 'set states {'
		for table in tables:
			print '  {', table.getAttribute ("probability")
			for row in table.getElementsByTagName ("tr"):
				print '    {',
				for cell in row.getElementsByTagName ("td"):
					state = getText (cell)
					if state_code.has_key(state):
						state = state_code[state]
					print state,
				print '}'
			print '  }'
		print '}'

		shortName = getText (test.getElementsByTagName ("short-name")[0])
		print 'stochastic_progress_test $params $herds $states "%s"' % shortName

	# Print the deterministic output variable tests.
	tests = doc.getElementsByTagName ("variable-test")
	for test in tests:
		description = getText (test.getElementsByTagName ("description")[0])
		print '\n\n\n#'
		for line in description.split('\n'):
			print '# %s' % line.strip().encode(OUTPUT_ENCODING, "replace")
		print '#'

		parameters = getText (test.getElementsByTagName ("parameter-description")[0])
		for line in parameters.split('\n'):
			print '# %s' % line.strip().encode(OUTPUT_ENCODING, "replace")
		print '#'

		category = getText (test.getElementsByTagName ("category")[0])
		parameterFileName = getText (test.getElementsByTagName ("parameter-file")[0])
		populationFileName = getText (test.getElementsByTagName ("population-file")[0])
		print 'set params "test/module.%s/%s.xml"' % (category, parameterFileName)
		print 'set herds "test/%s.xml"' % (populationFileName)

		table = test.getElementsByTagName ("output")[0]
		rows = table.getElementsByTagName ("tr")
		varnames = [getText (cell) for cell in rows[0].getElementsByTagName ("td")]
		del rows[0]
		print 'set values {'
		for i in range (len (varnames)):
			print ('  { "%s"' % varnames[i].encode(OUTPUT_ENCODING, "replace")),
			for row in rows:
				cell = row.getElementsByTagName ("td")[i]
				print getText (cell) or '""',
			print '}'
		print '}'

		shortName = getText (test.getElementsByTagName ("short-name")[0])
		print 'variable_test $params $herds $values "%s"' % shortName

	# Print the stochastic output variable tests.
	tests = doc.getElementsByTagName ("stochastic-variable-test")
	for test in tests:
		description = getText (test.getElementsByTagName ("description")[0])
		print '\n\n\n#'
		for line in description.split('\n'):
			print '# %s' % line.strip().encode(OUTPUT_ENCODING, "replace")
		print '#'

		parameters = getText (test.getElementsByTagName ("parameter-description")[0])
		for line in parameters.split('\n'):
			print '# %s' % line.strip().encode(OUTPUT_ENCODING, "replace")
		print '#'

		category = getText (test.getElementsByTagName ("category")[0])
		parameterFileName = getText (test.getElementsByTagName ("parameter-file")[0])
		populationFileName = getText (test.getElementsByTagName ("population-file")[0])
		print 'set params "test/module.%s/%s.xml"' % (category, parameterFileName)
		print 'set herds "test/%s.xml"' % (populationFileName)
		tables = test.getElementsByTagName ("output")

		print 'set values {'
		for table in tables:
			print '  {', table.getAttribute ("probability")
			rows = table.getElementsByTagName ("tr")
			varnames = [getText (cell) for cell in rows[0].getElementsByTagName ("td")]
			del rows[0]
			for i in range (len (varnames)):
				print ('    { "%s"' % varnames[i]),
				for row in rows:
					cell = row.getElementsByTagName ("td")[i]
					print getText (cell) or '""',
				print '}'
			print '  }'
		print '}'

		shortName = getText (test.getElementsByTagName ("short-name")[0])
		print 'stochastic_variable_test $params $herds $values "%s"' % shortName



if __name__ == "__main__":
	main()
