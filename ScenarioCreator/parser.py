__author__ = 'Josiah'
from xml.etree.ElementTree import ElementTree



def getText(elem):
    return ",".join(elem.itertext())

class PopulationParser:
    model_labels = ['production_type', 'latitude', 'longitude', 'initial_state', 'initial_size']
    xml_fields   = ['production-type', 'latitude', 'longitude', 'status',        'size']
    text_fields = list(zip(model_labels, xml_fields))

    def __init__(self, filename):
        tree = ElementTree(file='' + filename)
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

    def populate_text_field(self, herd, field_name, anathema_name = ''):
        if not anathema_name:
            anathema_name = field_name
        text = ''
        try:
            element = next(herd.iter(anathema_name))
            text = getText(element)
        except:
            raise IOError("Couldn't find '%s' label in xml" % anathema_name)
        self.population[-1][field_name] = text