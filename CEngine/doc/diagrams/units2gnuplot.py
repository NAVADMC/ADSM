#!/usr/bin/env python
"""This script turns a population file in XML format into gnuplot commands that
will plot a diagram of the units.

Susceptible units are represented by white dots, sized to indicate the number
of animals.  Incubating (source) units are yellow.
"""

__author__ = "Neil Harvey <nharve01@uoguelph.ca>"
__date__ = "December 2003"

import re
import sys
from math import pi, ceil, floor
from xml.dom.minidom import parse
import codecs

EARTH_RADIUS = 6378.137
DEG2KM = EARTH_RADIUS * pi / 180
EPSILON = 0.001



class Unit:
	def __init__ (self, size, x, y, state, unit_id):
		self.size = size
		self.x = x
		self.y = y
		self.state = state
		self.id = unit_id


		
def unique (l):
	set = []
	for item in l:
		if item not in set:
			set.append (item)
	return set



def getText (node):
	text = ""
	for child in node.childNodes:
		if child.nodeType == child.TEXT_NODE or child.nodeType == child.CDATA_SECTION_NODE:
			text += child.data
	return text.strip()



def main ():
	units = []

	doc = parse (sys.stdin)
	statepats = [
	  re.compile (r"0|S|Susceptible", re.I),
	  re.compile (r"1|L|Latent", re.I),
	  re.compile (r"2|B|Infectious ?Subclinical", re.I),
	  re.compile (r"3|C|Infectious ?Clinical", re.I),
	  re.compile (r"4|N|Naturally ?Immune", re.I),
	  re.compile (r"5|V|Vaccine ?Immune", re.I),
	  re.compile (r"6|D|Destroyed", re.I)
	]

	# Read the units.
	count = 0
	for unit in doc.getElementsByTagName ("herd"):
		idtags = unit.getElementsByTagName ("id")
		if len (idtags) > 0:
			unit_id = getText (idtags[0])
		else:
			unit_id = str (count)
		size = int (getText (unit.getElementsByTagName ("size")[0]))
		# Read either lat-lon or x-y (assumed to be in km).
		lat_elements = unit.getElementsByTagName ("latitude")
		if lat_elements:
			lat = float (getText (lat_elements[0]))
			lon = float (getText (unit.getElementsByTagName ("longitude")[0]))
			x = lon * DEG2KM
			y = lat * DEG2KM
		else:
			x = float (getText (unit.getElementsByTagName ("x")[0]))
			y = float (getText (unit.getElementsByTagName ("y")[0]))
		state = getText (unit.getElementsByTagName ("status")[0])
		for i in range (len(statepats)):
			match = statepats[i].match (state)
			if match:
				state = i
				break		
		units.append (Unit (size, x, y, state, unit_id))
		count += 1

	bbox = [
	  min ([unit.x for unit in units]),
	  min ([unit.y for unit in units]),
	  max ([unit.x for unit in units]),
	  max ([unit.y for unit in units])
	]

	# Set an encoding that can handle letters with accents.  Gnuplot does not
	# offer Unicode encodings.
	sys.stdout = codecs.getwriter('iso-8859-1')(sys.stdout.detach())
	print("set encoding iso_8859_1")

	# Set the x and y ranges.  First expand the bounding box to provide some
	# space around the points.  Then force the plot to be a square.
	bbox = [
	  floor (bbox[0] - 0.5),
	  floor (bbox[1] - 0.5),
	  ceil (bbox[2] + 0.5),
	  ceil (bbox[3] + 0.5)
	]
	xrange = bbox[2] - bbox[0]
	yrange = bbox[3] - bbox[1]
	diff = xrange - yrange
	if diff > 0: # box is wider than it is tall, increase height
		diff = diff / 2.0
		bbox[1] -= diff
		bbox[3] += diff
	elif diff < 0: # box is taller than it is wide, increase the width
		diff = diff / -2.0
		bbox[0] -= diff
		bbox[2] += diff
	print("set xrange [%g:%g]" % (bbox[0], bbox[2]))
	print("set yrange [%g:%g]" % (bbox[1], bbox[3]))
	print("""\
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"\
""")

	# Draw equator and prime meridian.
	print("set arrow from %g,%g to %g,%g nohead lt 0"
	  % (bbox[0], 0, bbox[2], 0))
	print("set arrow from %g,%g to %g,%g nohead lt 0"
	  % (0, bbox[1], 0, bbox[3]))

	# Get the number of animals in the smallest and largest units.  If units
	# have different sizes, the size range will be linearly mapped into
	# [1.0,3.0] to get gnuplot point sizes.
	minsize = min ([unit.size for unit in units])
	maxsize = max ([unit.size for unit in units])
	sizerange = abs (maxsize - minsize)
	if sizerange < EPSILON:
		sizerange = 0

	# Write unit IDs near the points.
	offset = min (bbox[2] - bbox[0], bbox[3] - bbox[1]) / 30.0
	for unit in units:
		sys.stdout.write('set label "')
		sys.stdout.write(unit.id)
		print('" at %g,%g left' % (unit.x + offset, unit.y - offset))

	# Colour comes from the line type in gnuplot.  Create an array of line
	# types for the colours in the unit state-transition diagram.
	linetype = [7,6,8,1,2,3,7,7]

	# Create an array of point types for dot shapes.
	pointtype = [71,7,7,7,7,7,7,7]

	# Create array of text description for states.
	statename = ["Susceptible", "Incubating", "Infectious Subclinical",
	  "Infectious Clinical", "Naturally immune", "Vaccine Immune", "Destroyed"]

	# Create commands to plot the units.
	command = []
	for unit in units:
		if sizerange == 0:
			pointsize = 2.0
		else:
			pointsize = 2.0 * (unit.size - minsize) / sizerange + 1.0
		command.append ("'-' notitle w p lt %i pt %i ps %g"
		  % (linetype[unit.state], pointtype[unit.state], pointsize))

	# Add commands to draw (off-screen) lines just to get a legend.
	#for state in unique ([state for size, x, y, state, unit_id in units]):
	#	command.append ("""%g title "%s" w l lt %i"""
	#	  % (bbox[1] - 1, statename[state], linetype[state]))

	command = "plot " + ", \\\n".join(command)
	print(command)
	for unit in units:
		print("%g %g\ne" % (unit.x, unit.y))



if __name__ == "__main__":
	main()
