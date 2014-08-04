from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future.builtins import zip
from future.builtins import next
from future.builtins import open
from future.builtins import dict
from future import standard_library
import os

standard_library.install_hooks()
from future.builtins import object
import ScenarioCreator.models

__author__ = 'Josiah'
import xml.etree.ElementTree as ET


def gettext(elem):
    return ",".join(elem.itertext())


class PopulationParser(object):
    model_labels = ['user_notes', 'production_type', 'latitude', 'longitude', 'initial_state', 'initial_size']
    xml_fields   = ['id',             'production-type', 'latitude', 'longitude', 'status',        'size']
    text_fields = list(zip(model_labels, xml_fields))

    def __init__(self, filename):
        filepath = ScenarioCreator.models.workspace(filename)
        if not os.path.isfile(filepath):
            raise OSError("'" + filepath + "' is not a file.")

        try:
            contents = open(filepath, encoding="utf-8").read()
            contents.replace('encoding="UTF-16" ?', 'encoding="utf-8"?', 1)
            # print(contents[:500])
        except UnicodeDecodeError:
            contents = open(filepath, encoding="utf-16").read()
            contents.replace('encoding="UTF-16" ?', 'encoding="utf-8"?', 1)
            # print(contents[:500])
            contents.encode("utf-8", errors='xmlcharrefreplace')
        if contents:
            tree = ET.ElementTree(ET.fromstring(contents))
            self.top_level = tree.getroot()
            self.population = []
        else:
            raise EOFError("File Read returned a blank string.")

    def parse_to_dictionary(self):
        self.parse_text_fields(self.text_fields)
        return self.population

    def parse_text_fields(self, text_fields):
        for herd in self.top_level.iter('herd'):
            self.population.append( dict() ) #empty
            for t in text_fields:
                if isinstance(t, tuple):
                    self.populate_text_field(herd, *t)
                else:
                    self.populate_text_field(herd, t)

    def populate_text_field(self, herd, field_name, xml_name=''):
        if not xml_name:
            xml_name = field_name
        try:
            element = next(herd.iter(xml_name))
            text = gettext(element)
        except:
            raise IOError("Couldn't find '%s' label in xml" % xml_name)
        self.population[-1][field_name] = text
