import os
import xml.etree.ElementTree as ET


def gettext(elem):
    return ",".join(elem.itertext())


class PopulationParser(object):
    model_labels = ['user_notes', 'production_type', 'latitude', 'longitude', 'initial_state', 'initial_size']
    xml_fields   = ['id',             'production-type', 'latitude', 'longitude', 'status',        'size']
    text_fields = list(zip(model_labels, xml_fields))

    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise OSError("'" + filename + "' is not a file.")

        if not os.path.getsize(filename):
            raise EOFError("File Read returned a blank string.")

        tree = ET.ElementTree(file=filename)
        self.top_level = tree.getroot()
        self.population = []

    def parse_to_dictionary(self):
        self.__parse_text_fields(self.text_fields)
        return self.population

    def __parse_text_fields(self, text_fields):
        for herd in self.top_level.iter('herd'):
            self.population.append( dict() ) #empty
            for t in text_fields:
                if isinstance(t, tuple):
                    self.__populate_text_field(herd, *t)
                else:
                    self.__populate_text_field(herd, t)

    def __populate_text_field(self, herd, field_name, xml_name=''):
        if not xml_name:
            xml_name = field_name
        try:
            element = next(herd.iter(xml_name))
            text = gettext(element)
        except:
            raise IOError("Couldn't find '%s' label in xml" % xml_name)
        self.population[-1][field_name] = text
