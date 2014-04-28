import ScenarioCreator.models

__author__ = 'Josiah'
import xml.etree.ElementTree as ET


def gettext(elem):
    return ",".join(elem.itertext())


class PopulationParser:
    model_labels = ['user_defined_1', 'production_type', 'latitude', 'longitude', 'initial_state', 'initial_size']
    xml_fields   = ['id',             'production-type', 'latitude', 'longitude', 'status',        'size']
    text_fields = list(zip(model_labels, xml_fields))

    def __init__(self, filename):
        filepath = ScenarioCreator.models.workspace(filename)
        try:
            contents = open(filepath, encoding="utf-8").read()
            contents.replace('encoding="UTF-16" ?', 'encoding="utf-8"?', 1)
            # print(contents[:500])
        except UnicodeDecodeError:
            contents = open(filepath, encoding="utf-16").read()
            contents.replace('encoding="UTF-16" ?', 'encoding="utf-8"?', 1)
            # print(contents[:500])
            contents.encode("utf-8", errors='xmlcharrefreplace')
        tree = ET.ElementTree(ET.fromstring(contents))
        self.top_level = tree.getroot()
        self.population = []

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
